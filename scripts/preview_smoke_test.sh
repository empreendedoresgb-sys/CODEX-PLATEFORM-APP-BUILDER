#!/usr/bin/env bash
set -euo pipefail

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"
BASE="http://${HOST}:${PORT}"

echo "[1/5] Checking language registry"
curl -fsS "${BASE}/v1/languages" >/tmp/apbuilder_languages.json
python -c 'import json; d=json.load(open("/tmp/apbuilder_languages.json")); assert d["status"]=="ok"; print("languages:", [x["id"] for x in d["languages"]])'

echo "[2/5] Creating orchestrator run"
RUN_PAYLOAD='{"prompt":"Build a production-ready CRM with auth, billing, and analytics","target":"web","mode":"prototype","language_id":"en"}'
RUN_JSON="$(curl -fsS -X POST "${BASE}/v1/orchestrator/run" -H 'content-type: application/json' -d "${RUN_PAYLOAD}")"
RUN_ID="$(python -c 'import json,sys; print(json.loads(sys.argv[1])["run"]["run_id"])' "${RUN_JSON}")"
echo "run_id=${RUN_ID}"

echo "[3/5] Verifying run retrieval"
GET_JSON="$(curl -fsS "${BASE}/v1/orchestrator/runs/${RUN_ID}")"
python -c 'import json,sys; d=json.loads(sys.argv[1]); assert d["status"]=="ok"; assert d["run"]["stage"]=="DEPLOY_READY"; print("stage:", d["run"]["stage"])' "${GET_JSON}"

echo "[4/5] Deploying run"
DEPLOY_JSON="$(curl -fsS -X POST "${BASE}/v1/orchestrator/runs/${RUN_ID}/deploy")"
python -c 'import json,sys; d=json.loads(sys.argv[1]); assert d["status"]=="ok"; assert d["run"]["stage"]=="RELEASED"; print("deploy_url:", d["run"]["deploy_url"])' "${DEPLOY_JSON}"

echo "[5/5] Smoke test completed successfully"
