class StateManager:
    def __init__(self) -> None:
        self.cache: dict[str, str] = {}

    def put(self, key: str, value: str) -> None:
        self.cache[key] = value

    def get(self, key: str) -> str | None:
        return self.cache.get(key)
