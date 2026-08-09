"""AN3 / R10-26 — expanded coverage for all v2 routes (CRUD edges + errors)."""

from __future__ import annotations


def _seed_project(client, suffix: str = "cov"):
    assert (
        client.post(
            "/api/v1/targets",
            json={
                "target_id": f"target--{suffix}",
                "target_value": f"{suffix}.example",
            },
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/api/v1/workflows",
            json={
                "workflow_id": f"workflow--{suffix}",
                "target_id": f"target--{suffix}",
                "name": f"wf-{suffix}",
            },
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/api/v1/projects",
            json={
                "project_id": f"project--{suffix}",
                "project_name": f"Project {suffix}",
                "project_description": f"Coverage project {suffix}",
                "workflow_ids": [f"workflow--{suffix}"],
                "stix_incident_id": f"incident--{suffix}",
            },
        ).status_code
        == 201
    )


def test_targets_get_put_and_errors(client):
    body = {
        "target_id": "target--get",
        "target_value": "get.example",
        "target_description": "d",
    }
    assert client.post("/api/v1/targets", json=body).status_code == 201

    r = client.get("/api/v1/targets/target--get")
    assert r.status_code == 200
    assert r.json()["target_value"] == "get.example"

    r = client.put(
        "/api/v1/targets/target--get",
        json={"target_description": "updated-desc"},
    )
    assert r.status_code == 200
    assert r.json()["target_description"] == "updated-desc"

    assert client.get("/api/v1/targets/missing").status_code == 404
    assert client.patch("/api/v1/targets/missing", json={"target_value": "x"}).status_code == 404
    assert client.delete("/api/v1/targets/missing").status_code == 404

    # duplicate create → 400
    r = client.post("/api/v1/targets", json=body)
    assert r.status_code == 400


def test_workflows_update_delete_list_and_crud_get(client):
    _seed_project(client, "wf")

    r = client.get("/api/v1/workflows")
    assert r.status_code == 200
    assert any(w["workflow_id"] == "workflow--wf" for w in r.json())

    r = client.get("/api/v1/workflows/workflow--wf")
    assert r.status_code == 200
    assert r.json()["target_id"] == "target--wf"

    r = client.patch(
        "/api/v1/workflows/workflow--wf",
        json={"name": "renamed", "workflow_yaml": "apiVersion: spiderfeet.workflow/v1\n"},
    )
    assert r.status_code == 200
    assert r.json()["name"] == "renamed"

    r = client.put(
        "/api/v1/workflows/workflow--wf",
        json={"name": "put-name"},
    )
    assert r.status_code == 200
    assert r.json()["name"] == "put-name"

    assert client.get("/api/v1/workflows/missing").status_code == 404
    assert client.get("/api/v1/workflows/missing?projection=true").status_code == 404
    assert client.patch("/api/v1/workflows/missing", json={"name": "x"}).status_code == 404

    # create without player → 400
    r = client.post("/api/v1/workflows", json={"workflow_id": "workflow--orphan"})
    assert r.status_code == 400

    r = client.delete("/api/v1/workflows/workflow--wf")
    assert r.status_code == 204
    assert client.get("/api/v1/workflows/workflow--wf").status_code == 404
    assert client.delete("/api/v1/workflows/missing").status_code == 404


def test_projects_update_crud_get_and_errors(client):
    _seed_project(client, "pj")

    r = client.get("/api/v1/projects/project--pj?projection=false")
    assert r.status_code == 200
    assert r.json()["project_id"] == "project--pj"
    assert r.json()["workflow_ids"] == ["workflow--pj"]

    r = client.patch(
        "/api/v1/projects/project--pj",
        json={"stix_incident_id": "incident--updated"},
    )
    assert r.status_code == 200
    assert r.json()["stix_incident_id"] == "incident--updated"

    r = client.put(
        "/api/v1/projects/project--pj",
        json={"stix_incident_id": "incident--put"},
    )
    assert r.status_code == 200

    assert client.get("/api/v1/projects/missing").status_code == 404
    assert client.patch("/api/v1/projects/missing", json={"stix_incident_id": "x"}).status_code == 404
    assert client.delete("/api/v1/projects/missing").status_code == 404

    # create without workflows → OK (standalone project entity, R13-03)
    r = client.post(
        "/api/v1/projects",
        json={
            "project_id": "project--empty",
            "project_name": "Empty",
            "project_description": "Standalone",
            "workflow_ids": [],
        },
    )
    assert r.status_code == 201, r.text
    assert r.json()["workflow_ids"] == []

    # duplicate → 400
    r = client.post(
        "/api/v1/projects",
        json={"project_id": "project--pj", "workflow_ids": ["workflow--pj"]},
    )
    assert r.status_code == 400


def test_scan_steps_list_and_404(client, fake_stores):
    crud, _ = fake_stores
    crud.scan_steps["scan_step--list"] = {
        "scan_instance_id": "scan_step--list",
        "step_module_id": "sfp_cli_nmap",
        "scan_status": "FINISHED",
        "scan_ui_cli_command": "nmap -oX -",
        "scan_ui_text_form": "text",
        "scan_ui_structured_form": "{}",
        "scan_ui_graph_form": '{"nodes":[],"edges":[]}',
        "scan_ui_markdown_narrative_form": "# md",
        "consumed_ids": [],
        "produced_ids": [],
        "scan_result_graph_ids": [],
    }
    r = client.get("/api/v1/scan-steps")
    assert r.status_code == 200
    assert any(s.get("scan_instance_id") == "scan_step--list" for s in r.json())

    assert client.get("/api/v1/scan-steps/missing").status_code == 404


def test_contexts_404_and_temporary_update_existing(client):
    assert client.get("/api/v1/projects/missing/contexts/temporary").status_code == 404
    assert client.get("/api/v1/projects/missing/contexts/project").status_code == 404
    assert (
        client.put(
            "/api/v1/projects/missing/contexts/temporary",
            json={"nodes": [], "edges": []},
        ).status_code
        == 404
    )

    _seed_project(client, "ctx2")
    payload = {
        "temporary_subgraph_id": "temporary-subgraph--ctx2",
        "nodes": [
            {
                "id": "DOMAIN_NAME--ctx2",
                "nugget_instance_id": "DOMAIN_NAME--ctx2",
                "nugget_id": "DOMAIN_NAME",
                "nugget_data": "ctx2.example",
                "temporary_id": "temporary--aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
            }
        ],
        "edges": [],
    }
    r = client.put("/api/v1/projects/project--ctx2/contexts/temporary", json=payload)
    assert r.status_code == 200, r.text

    # second put updates existing subgraph
    payload["nodes"].append(
        {
            "id": "IPV4_ADDRESS--9-9-9-9",
            "nugget_instance_id": "IPV4_ADDRESS--9-9-9-9",
            "nugget_id": "IPV4_ADDRESS",
            "nugget_data": "9.9.9.9",
            "temporary_id": "temporary--bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
        }
    )
    payload["edges"] = [
        {
            "source": "temporary--aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
            "target": "temporary--bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
            "relation": "resolves-to",
        }
    ]
    r = client.put("/api/v1/projects/project--ctx2/contexts/temporary", json=payload)
    assert r.status_code == 200, r.text
    body = r.json()
    assert len(body["nodes"]) == 2
    assert all("temporary_id" not in n for n in body["nodes"])
    assert body["edges"][0]["source"] == "DOMAIN_NAME--ctx2"


def test_execute_project_not_found(client):
    _seed_project(client, "ex2")
    r = client.post(
        "/api/v1/workflows/workflow--ex2/execute",
        json={"project_id": "project--missing"},
    )
    assert r.status_code == 404

    r = client.post(
        "/api/v1/workflows/workflow--ex2/steps/step1/execute",
        json={"project_id": "project--missing"},
    )
    assert r.status_code == 404
