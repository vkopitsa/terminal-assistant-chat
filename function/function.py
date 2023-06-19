from typing import Any, Protocol, Dict, AnyStr, Union


class Function(Protocol):
    specification: Dict

    def get_name(self) -> AnyStr:
        pass

    def func(self, data: Union[str, Dict], **kwargs: dict) -> Any:
        pass
