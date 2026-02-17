class SessionManager:
    """Simple in-memory session tracker placeholder."""

    def __init__(self) -> None:
        self._sessions: dict[str, dict] = {}

    def save(self, session_id: str, state: dict) -> None:
        self._sessions[session_id] = state

    def load(self, session_id: str) -> dict | None:
        return self._sessions.get(session_id)
