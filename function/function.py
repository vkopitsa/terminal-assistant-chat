from typing import Any, List, Protocol, Dict, AnyStr


class Function(Protocol):
    specification: Dict

    def get_name(self) -> AnyStr:
        pass

    def func(self, quz: List[int]) -> Any:
        pass
