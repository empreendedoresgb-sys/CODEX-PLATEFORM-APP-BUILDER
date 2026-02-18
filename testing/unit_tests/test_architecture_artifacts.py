import json
from pathlib import Path


def test_rest_api_blueprint_is_valid_json() -> None:
    path = Path('api/contracts/rest_api_blueprint.json')
    payload = json.loads(path.read_text())
    assert payload['openapi'] == '3.1.0'
    assert '/generate/voice' in payload['paths']
    assert '/transcription/analyze' in payload['paths']


def test_full_schema_contains_critical_tables() -> None:
    sql = Path('database/full_schema.sql').read_text().lower()
    for table in [
        'organizations',
        'users',
        'projects',
        'voice_profiles',
        'voice_clones',
        'generation_jobs',
        'transcripts',
        'linguistic_analyses',
        'invoices',
    ]:
        assert f'create table if not exists {table}' in sql
