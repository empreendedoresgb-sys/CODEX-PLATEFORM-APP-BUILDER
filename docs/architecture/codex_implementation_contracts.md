# Codex Implementation Contracts (Starter Skeleton + Exact Signatures)

This document defines explicit starter skeleton contracts for the new APBUILDER modules so implementation can proceed with minimal ambiguity.

## 1) Orchestrator Agents

### `orchestrator/agents/base.py`

```python
class IntentParserAgent(Protocol):
    def run(self, prompt: str) -> AgentArtifact: ...

class ArchitectAgent(Protocol):
    def run(self, target: str, mode: str) -> AgentArtifact: ...

class GeneratorAgent(Protocol):
    def run(self) -> list[AgentArtifact]: ...

class ValidatorAgent(Protocol):
    def run(self, prompt: str) -> list[str]: ...
```

### Concrete module signatures

```python
# orchestrator/agents/intent_parser.py

def run(prompt: str) -> AgentArtifact: ...

# orchestrator/agents/architect.py

def run(target: str, mode: str) -> AgentArtifact: ...

# orchestrator/agents/generator.py

def run() -> list[AgentArtifact]: ...

# orchestrator/agents/validator.py

def run(prompt: str) -> list[str]: ...
```

## 2) Orchestrator Core

### `orchestrator/master.py`

```python
def run_orchestrator(req: OrchestratorRunRequest) -> OrchestratorRunResult: ...

def deploy_run(run_id: str) -> OrchestratorRunResult: ...

def get_orchestrator_run(run_id: str) -> OrchestratorRunResult: ...
```

### `orchestrator/repository.py`

```python
def create_run(prompt: str, target: str, mode: str, language_id: str) -> OrchestratorRunResult: ...

def save_run(run: OrchestratorRunResult) -> None: ...

def get_run(run_id: str) -> OrchestratorRunResult: ...

def add_event(run_id: str, stage: RunStage, message: str) -> None: ...

def get_events(run_id: str) -> list[RunEvent]: ...
```

## 3) Language Runtime Registry

### `core/languages/base.py`

```python
class LanguageRuntime(Protocol):
    language_id: str
    display_name: str
    language_type: str

    def normalize(self, text: str) -> str: ...
    def validate_lexicon(self, text: str) -> bool: ...
    def validate_grammar(self, text: str) -> bool: ...
    def validate_phonetic_mode(self, phonetic_mode: str) -> None: ...
    def prompt_conditioning(self, prompt: str) -> str: ...
    def validate_text(self, text: str) -> None: ...
```

### `core/languages/registry.py`

```python
def register_runtime(runtime: LanguageRuntime) -> None: ...

def list_languages() -> list[dict[str, str]]: ...

def get_language(language_id: str) -> LanguageRegistration: ...

def get_runtime(language_id: str) -> LanguageRuntime: ...
```

## 4) API Surface

### `api/rest_endpoints.py`

```python
@app.post("/v1/orchestrator/run")
def orchestrator_run(req: OrchestratorRunRequest) -> dict: ...

@app.get("/v1/orchestrator/runs/{run_id}")
def orchestrator_get_run(run_id: str) -> dict: ...

@app.post("/v1/orchestrator/runs/{run_id}/deploy")
def orchestrator_deploy_run(run_id: str) -> dict: ...
```

## 5) Implementation Notes

- Keep contracts stable and additive for backward compatibility.
- Use typed datamodels (`pydantic.BaseModel`) for API/request boundaries.
- Maintain deterministic state transitions through `orchestrator/state_machine.py`.
