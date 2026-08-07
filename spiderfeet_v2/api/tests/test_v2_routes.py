"""AN2 / R10-24 / R10-25 — v2 route contract tests (in-memory stores)."""

from __future__ import annotations

from spiderfeet_v2.api.temporary_ids import strip_temporary_ids


def test_health_still_ok(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_targets_crud(client):
    body = {
        "target_id": "target--example-com",
        "target_value": "example.com",
        "target_description": "lab",
    }
    r = client.post("/api/v1/targets", json=body)
    assert r.status_code == 201, r.text
    assert r.json()["target_value"] == "example.com"

    r = client.get("/api/v1/targets")
    assert r.status_code == 200
    assert any(t["target_id"] == "target--example-com" for t in r.json())

    r = client.patch(
        "/api/v1/targets/target--example-com",
        json={"target_value": "updated.example"},
    )
    assert r.status_code == 200
    assert r.json()["target_value"] == "updated.example"

    r = client.delete("/api/v1/targets/target--example-com")
    assert r.status_code == 204
    assert client.get("/api/v1/targets/target--example-com").status_code == 404


def test_workflows_and_projects_crud(client):
    assert (
        client.post(
            "/api/v1/targets",
            json={"target_id": "target--a", "target_value": "a.example"},
        ).status_code
        == 201
    )
    r = client.post(
        "/api/v1/workflows",
        json={
            "workflow_id": "workflow--a",
            "name": "recon",
            "target_id": "target--a",
            "workflow_yaml": "apiVersion: spiderfeet.workflow/v1\n",
        },
    )
    assert r.status_code == 201, r.text

    r = client.get("/api/v1/workflows/workflow--a?projection=true")
    assert r.status_code == 200
    assert r.json()["target"] == "target--a"
    assert "workflow_yaml" in r.json()

    r = client.post(
        "/api/v1/projects",
        json={
            "project_id": "project--a",
            "stix_incident_id": "incident--a",
            "workflow_ids": ["workflow--a"],
        },
    )
    assert r.status_code == 201, r.text

    r = client.get("/api/v1/projects")
    assert r.status_code == 200
    assert any(p["project_id"] == "project--a" for p in r.json())

    r = client.get("/api/v1/projects/project--a")
    assert r.status_code == 200
    body = r.json()
    assert body["project_id"] == "project--a"
    assert "workflow--a" in body["workflows"]
    assert body["stix_incident_id"] == "incident--a"

    r = client.delete("/api/v1/projects/project--a")
    assert r.status_code == 204


def test_scan_step_four_forms(client, fake_stores):
    crud, _ = fake_stores
    crud.scan_steps["scan_step--1"] = {
        "scan_instance_id": "scan_step--1",
        "step_module_id": "sfp_cli_subfinder",
        "scan_status": "FINISHED",
        "scan_ui_cli_command": "subfinder -d example.com -oJ",
        "scan_ui_text_form": "example.com\n",
        "scan_ui_structured_form": '{"host":"example.com"}',
        "scan_ui_structured_form_type": "json",
        "scan_ui_graph_form": '{"nodes":[],"edges":[]}',
        "scan_ui_markdown_narrative_form": "# Report\n",
        "consumed_ids": ["DOMAIN_NAME--example-com"],
        "produced_ids": ["INTERNET_NAME--www-example-com"],
        "scan_result_graph_ids": ["scan-result--1"],
    }
    r = client.get("/api/v1/scan-steps/scan_step--1")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["cli_command"].startswith("subfinder")
    assert body["text_form"]
    assert body["structured_form"]
    assert body["graph_form"]
    assert body["markdown_narrative_form"].startswith("#")
    assert body["consumed"] == ["DOMAIN_NAME--example-com"]
    assert body["produced"] == ["INTERNET_NAME--www-example-com"]
    assert body["scan_status"] == "FINISHED"


def test_strip_temporary_ids_unit():
    cleaned = strip_temporary_ids(
        {
            "nodes": [
                {
                    "id": "DOMAIN_NAME--x",
                    "nugget_instance_id": "DOMAIN_NAME--x",
                    "temporary_id": "temporary--aaa",
                },
                {
                    "id": "IPV4_ADDRESS--1",
                    "nugget_instance_id": "IPV4_ADDRESS--1",
                    "temporary_id": "temporary--bbb",
                },
            ],
            "edges": [
                {
                    "source": "temporary--aaa",
                    "target": "temporary--bbb",
                    "relation": "resolves-to",
                }
            ],
        }
    )
    assert all("temporary_id" not in n for n in cleaned["nodes"])
    assert cleaned["edges"][0]["source"] == "DOMAIN_NAME--x"
    assert cleaned["edges"][0]["target"] == "IPV4_ADDRESS--1"


def test_temporary_context_update_strips_ids(client):
    client.post(
        "/api/v1/targets",
        json={"target_id": "target--ctx", "target_value": "ctx.example"},
    )
    client.post(
        "/api/v1/workflows",
        json={"workflow_id": "workflow--ctx", "target_id": "target--ctx"},
    )
    client.post(
        "/api/v1/projects",
        json={"project_id": "project--ctx", "workflow_ids": ["workflow--ctx"]},
    )

    payload = {
        "temporary_subgraph_id": "temporary-subgraph--ctx",
        "nodes": [
            {
                "id": "DOMAIN_NAME--ctx",
                "nugget_instance_id": "DOMAIN_NAME--ctx",
                "nugget_id": "DOMAIN_NAME",
                "nugget_data": "ctx.example",
                "temporary_id": "temporary--11111111-1111-4111-8111-111111111111",
            },
            {
                "id": "IPV4_ADDRESS--1-2-3-4",
                "nugget_instance_id": "IPV4_ADDRESS--1-2-3-4",
                "nugget_id": "IPV4_ADDRESS",
                "nugget_data": "1.2.3.4",
                "temporary_id": "temporary--22222222-2222-4222-8222-222222222222",
            },
        ],
        "edges": [
            {
                "source": "temporary--11111111-1111-4111-8111-111111111111",
                "target": "temporary--22222222-2222-4222-8222-222222222222",
                "relation": "resolves-to",
            }
        ],
    }
    r = client.put("/api/v1/projects/project--ctx/contexts/temporary", json=payload)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["kind"] == "temporary_subgraph"
    assert body["subgraph_id"] == "temporary-subgraph--ctx"
    assert all("temporary_id" not in n for n in body["nodes"])
    assert body["edges"][0]["source"] == "DOMAIN_NAME--ctx"
    assert body["edges"][0]["target"] == "IPV4_ADDRESS--1-2-3-4"

    r = client.get("/api/v1/projects/project--ctx/contexts/temporary")
    assert r.status_code == 200
    assert r.json()["subgraph_id"] == "temporary-subgraph--ctx"
    assert len(r.json()["nodes"]) == 2


def test_project_context_empty(client):
    client.post(
        "/api/v1/targets",
        json={"target_id": "target--pc", "target_value": "pc.example"},
    )
    client.post(
        "/api/v1/workflows",
        json={"workflow_id": "workflow--pc", "target_id": "target--pc"},
    )
    client.post(
        "/api/v1/projects",
        json={"project_id": "project--pc", "workflow_ids": ["workflow--pc"]},
    )
    r = client.get("/api/v1/projects/project--pc/contexts/project")
    assert r.status_code == 200
    assert r.json()["nodes"] == []
    assert r.json()["edges"] == []


def test_execute_workflow_and_step_dry_run(client):
    yaml_doc = """apiVersion: spiderfeet.workflow/v1
kind: Workflow
id: workflow--ex
info:
  name: ao2-ex
inputs:
  targets:
    type: string_list
    values:
      - https://example.com
steps:
  - id: sfp_cli_subfinder
    uses: tool.subfinder
    needs: []
    input:
      type: string_list
      from: $workflow.inputs.targets
      normalize: hostname_from_url
    config:
      argv:
        - "-d"
        - "$step.input.values[0]"
        - "-oJ"
        - "-silent"
    output:
      vars:
        all_domains:
          type: string_list
          select:
            source: $step.scan_graph
            nodes:
              nugget_id: DOMAIN_NAME
            project: nugget_data
            distinct: true
    context:
      export: scan_graph
  - id: sfp_cli_httpx
    uses: tool.httpx
    needs: [sfp_cli_subfinder]
    input:
      type: string_list
      from: $steps.sfp_cli_subfinder.vars.all_domains
      empty: skip_step
    config:
      argv:
        - "-l"
        - "$step.files.input"
        - "-json"
        - "-silent"
    context:
      export: none
"""
    client.post(
        "/api/v1/targets",
        json={"target_id": "target--ex", "target_value": "ex.example"},
    )
    client.post(
        "/api/v1/workflows",
        json={
            "workflow_id": "workflow--ex",
            "target_id": "target--ex",
            "workflow_yaml": yaml_doc,
        },
    )
    client.post(
        "/api/v1/projects",
        json={"project_id": "project--ex", "workflow_ids": ["workflow--ex"]},
    )

    r = client.post(
        "/api/v1/workflows/workflow--ex/execute",
        json={"project_id": "project--ex", "dry_run": True},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["status"] == "DRY_RUN"
    assert body["orchestrator"] == "ao2"
    assert body["waves"] == [["sfp_cli_subfinder"], ["sfp_cli_httpx"]]
    assert body["step_count"] == 2
    assert body["steps"][0]["input_values"] == ["example.com"]

    r = client.post(
        "/api/v1/workflows/workflow--ex/steps/sfp_cli_subfinder/execute",
        json={"project_id": "project--ex", "dry_run": True},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["status"] == "DRY_RUN"
    assert body["orchestrator"] == "ao1"
    assert body["step_id"] == "sfp_cli_subfinder"
    assert body["module_id"] == "sfp_cli_subfinder"
    assert body["input_values"] == ["example.com"]
    assert body["scan_instance_id"]

    assert (
        client.post(
            "/api/v1/workflows/missing/execute",
            json={},
        ).status_code
        == 404
    )


def test_openapi_includes_v2_paths_and_examples(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    paths = r.json()["paths"]
    for path in (
        "/api/v1/projects",
        "/api/v1/workflows",
        "/api/v1/targets",
        "/api/v1/scan-steps/{scan_instance_id}",
        "/api/v1/projects/{project_id}/contexts/temporary",
        "/api/v1/workflows/{workflow_id}/execute",
    ):
        assert path in paths, path

    project_post = paths["/api/v1/projects"]["post"]
    content = project_post["requestBody"]["content"]["application/json"]
    assert "example" in content or "examples" in content

    temp_put = paths["/api/v1/projects/{project_id}/contexts/temporary"]["put"]
    temp_content = temp_put["requestBody"]["content"]["application/json"]
    assert "example" in temp_content or "examples" in temp_content
