from typing import Any, Protocol, Dict, AnyStr, Optional


class Function(Protocol):
    specification: Dict

    def get_name(self) -> AnyStr:
        pass

    def func(self, **kwargs: Optional[Any]) -> Any:
        pass
