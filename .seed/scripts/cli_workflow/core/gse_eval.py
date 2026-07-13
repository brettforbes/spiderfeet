"""Graph Select Language (GSE) v1 evaluator — see .seed/12C_Graph_Select_Language.md."""

from __future__ import annotations

import itertools
import re
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set

from .graph_index import GraphIndex


class GseError(ValueError):
    pass


def _project(node: Mapping[str, Any], field: str) -> str:
    val = node.get(field)
    if val is None and field == "nugget_data":
        val = node.get("data")
    return "" if val is None else str(val)


def _finalize(values: Iterable[str], distinct: bool = True) -> List[str]:
    out = [v for v in values if v != ""]
    if distinct:
        out = sorted(set(out))
    return out


def _ids_match(node: Mapping[str, Any], match: Mapping[str, Any]) -> bool:
    nid = node.get("nugget_id")
    if "nugget_id" in match and nid != match["nugget_id"]:
        return False
    if "nugget_id_in" in match and nid not in match["nugget_id_in"]:
        return False
    if "nugget_data_equals" in match:
        if _project(node, "nugget_data") != match["nugget_data_equals"]:
            return False
    if "nugget_data_regex" in match:
        if re.search(match["nugget_data_regex"], _project(node, "nugget_data")) is None:
            return False
    return True


def _has_related(
    index: GraphIndex,
    node_id: str,
    pred: Mapping[str, Any],
) -> bool:
    direction = pred.get("direction", "out")
    relation = pred["relation"]
    transitive = bool(pred.get("transitive", False))
    candidates = index.reachable(node_id, relation, transitive=transitive, direction=direction)
    want_id = pred.get("nugget_id")
    want_in = pred.get("nugget_id_in")
    for cid in candidates:
        n = index.nodes.get(cid)
        if not n:
            continue
        nid = n.get("nugget_id")
        if want_id and nid == want_id:
            return True
        if want_in and nid in want_in:
            return True
        if not want_id and not want_in:
            return True
    return False


def _where_ok(index: GraphIndex, node: Mapping[str, Any], where: Sequence[Mapping[str, Any]]) -> bool:
    node_id = node.get("id") or node.get("nugget_instance_id")
    if not node_id:
        return False
    for pred in where or []:
        if "related" in pred:
            if not _has_related(index, node_id, pred["related"]):
                return False
        elif "not" in pred:
            inner = pred["not"]
            if "related" in inner and _has_related(index, node_id, inner["related"]):
                return False
        elif "attr" in pred:
            attr = pred["attr"]
            field = attr["field"]
            op = attr["op"]
            value = attr["value"]
            actual = _project(node, field) if field == "nugget_data" else str(node.get(field, ""))
            if op == "eq" and actual != value:
                return False
            if op == "regex" and re.search(value, actual) is None:
                return False
        else:
            raise GseError(f"unknown where predicate: {pred}")
    return True


def match_nodes(
    index: GraphIndex,
    match: Mapping[str, Any],
    candidate_ids: Optional[Set[str]] = None,
) -> List[Dict[str, Any]]:
    if candidate_ids is None:
        nodes = list(index.nodes.values())
    else:
        nodes = [index.nodes[i] for i in candidate_ids if i in index.nodes]
    out: List[Dict[str, Any]] = []
    where = match.get("where") or []
    for node in nodes:
        if not _ids_match(node, match):
            continue
        if where and not _where_ok(index, node, where):
            continue
        out.append(dict(node))
    return out


def _emit_product(emit: Mapping[str, Any], binds: Mapping[str, List[str]]) -> List[str]:
    if "values" in emit:
        key = emit["values"]
        return list(binds.get(key, []))
    product_keys = emit.get("product") or []
    if not product_keys:
        return []
    lists = [binds.get(k, []) for k in product_keys]
    if any(len(lst) == 0 for lst in lists):
        return []
    fmt = emit.get("format")
    join = emit.get("join", "")
    rows: List[str] = []
    for combo in itertools.product(*lists):
        mapping = dict(zip(product_keys, combo))
        if fmt:
            try:
                rows.append(fmt.format(**mapping))
            except KeyError as exc:
                raise GseError(f"emit.format missing key: {exc}") from exc
        else:
            rows.append(join.join(combo))
    return rows


def _eval_for_each(
    fe: Mapping[str, Any],
    index: GraphIndex,
    scope_ids: Optional[Set[str]] = None,
) -> List[str]:
    roots = match_nodes(index, fe.get("nodes") or {}, scope_ids)
    out: List[str] = []
    for root in roots:
        root_id = root.get("id") or root.get("nugget_instance_id")
        if not root_id:
            continue
        if "for_each" in fe:
            # nested: restrict candidates to reachable from root if along provided on nested — v1 nested uses full match under root via collect only
            out.extend(_eval_for_each(fe["for_each"], index, scope_ids=None))
            continue
        binds: Dict[str, List[str]] = {}
        # expose root projected value under its bind name for format use
        binds[fe["as"]] = [_project(root, "nugget_data")]
        for collect in fe.get("collect") or []:
            if collect.get("reachable_from") != fe["as"]:
                raise GseError(
                    f"collect.reachable_from '{collect.get('reachable_from')}' "
                    f"must match for_each.as '{fe['as']}' in v1"
                )
            along = collect["along"]
            reachable = index.reachable(
                root_id,
                along["relation"],
                transitive=bool(along.get("transitive", False)),
                direction=along.get("direction", "out"),
            )
            matched = match_nodes(index, collect.get("nodes") or {}, reachable)
            project = collect.get("project", "nugget_data")
            binds[collect["as"]] = [_project(n, project) for n in matched]
        emit = fe.get("emit") or {}
        out.extend(_emit_product(emit, binds))
    return out


def eval_select(select: Mapping[str, Any], graph: Mapping[str, Any]) -> List[str]:
    index = GraphIndex(dict(graph))
    distinct = bool(select.get("distinct", True))
    if "for_each" in select:
        return _finalize(_eval_for_each(select["for_each"], index), distinct)
    match = select.get("nodes") or {}
    project = select.get("project", "nugget_data")
    nodes = match_nodes(index, match)
    return _finalize((_project(n, project) for n in nodes), distinct)


def eval_binding(
    binding: Mapping[str, Any],
    *,
    graph: Optional[Mapping[str, Any]] = None,
    env_lists: Optional[Mapping[str, List[str]]] = None,
) -> List[str]:
    """Evaluate a GSE variable binding.

    ``env_lists`` maps absolute var refs or short names already resolved to lists
    (used for ``union`` / ``from_var``).
    """
    env_lists = env_lists or {}
    btype = binding.get("type")
    if btype != "string_list":
        raise GseError(f"unsupported binding type: {btype}")

    if "select" in binding:
        if graph is None:
            raise GseError("select binding requires a graph")
        return eval_select(binding["select"], graph)

    if "union" in binding:
        values: List[str] = []
        for ref in binding["union"]:
            if ref not in env_lists:
                raise GseError(f"union ref not in env: {ref}")
            values.extend(env_lists[ref])
        return _finalize(values, bool(binding.get("distinct", True)))

    if "from_var" in binding:
        ref = binding["from_var"]
        if ref not in env_lists:
            raise GseError(f"from_var not in env: {ref}")
        return list(env_lists[ref])

    if "literal" in binding:
        return _finalize(binding.get("literal") or [], distinct=True)

    raise GseError(f"binding must be select|union|from_var|literal: {binding.keys()}")
