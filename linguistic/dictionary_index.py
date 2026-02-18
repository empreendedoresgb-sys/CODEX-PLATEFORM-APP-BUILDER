class DictionaryIndex:
    def __init__(self) -> None:
        self._entries: dict[str, str] = {}

    def lookup(self, term: str) -> str | None:
        return self._entries.get(term.lower())
