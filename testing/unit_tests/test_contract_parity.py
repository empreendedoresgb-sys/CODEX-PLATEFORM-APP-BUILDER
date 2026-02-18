import json
from pathlib import Path

import pytest


def test_blueprint_runtime_parity() -> None:
    pytest.importorskip("fastapi")
    from fastapi.routing import APIRoute
    from api.rest_endpoints import app

    blueprint = json.loads(Path("api/contracts/rest_api_blueprint.json").read_text())

    blueprint_paths = {f"/v1{path}" for path in blueprint["paths"].keys()}
    runtime_paths = {route.path for route in app.routes if isinstance(route, APIRoute)}

    missing = blueprint_paths - runtime_paths
    assert not missing, f"Missing runtime endpoints: {sorted(missing)}"
