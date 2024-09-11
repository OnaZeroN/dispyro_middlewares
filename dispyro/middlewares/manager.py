import functools
from typing import Any, Callable, Dict, List, Optional, Sequence, Union, overload


from dispyro.handlers import Handler
from dispyro.types import Update
from dispyro.types.bases import MiddlewareType, NextMiddlewareType, MiddlewareEventType


class MiddlewareManager:
    def __init__(self) -> None:
        self.middlewares: List[MiddlewareType[Update]] = []

    def register(
        self,
        middleware: MiddlewareType[Update],
    ) -> MiddlewareType[Update]:
        self.middlewares.append(middleware)
        return middleware

    def unregister(self, middleware: MiddlewareType[Update]) -> None:
        self.middlewares.remove(middleware)

    def __call__(
        self,
        middleware: Optional[MiddlewareType[Update]] = None,
    ) -> Union[
        Callable[[MiddlewareType[Update]], MiddlewareType[Update]],
        MiddlewareType[Update],
    ]:
        if middleware is None:
            return self.register
        return self.register(middleware)

    @overload
    def __getitem__(self, item: int) -> MiddlewareType[Update]:
        pass

    @overload
    def __getitem__(self, item: slice) -> Sequence[MiddlewareType[Update]]:
        pass

    def __getitem__(
        self, item: Union[int, slice]
    ) -> Union[MiddlewareType[Update], Sequence[MiddlewareType[Update]]]:
        return self.middlewares[item]

    def __len__(self) -> int:
        return len(self.middlewares)

    @staticmethod
    def wrap_middlewares(
            middlewares: Sequence[MiddlewareType[MiddlewareEventType]], handler: Handler
    ) -> NextMiddlewareType[MiddlewareEventType]:
        @functools.wraps(handler)
        def handler_wrapper(client, event: MiddlewareEventType, kwargs: Dict[str, Any]) -> Any:
            return handler(client=client, update=event, **kwargs)

        middleware = handler_wrapper
        for m in reversed(middlewares):
            middleware = functools.partial(m, middleware)
        return middleware
