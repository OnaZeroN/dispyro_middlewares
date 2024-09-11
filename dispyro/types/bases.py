from typing import Any, Awaitable, Callable, Dict, TypeVar, Union

from pyrogram import Client

from dispyro.types.packed_raw_update import Update
from dispyro.middlewares.base import BaseMiddleware

MiddlewareEventType = TypeVar("MiddlewareEventType", bound=Update)
NextMiddlewareType = Callable[[Client, MiddlewareEventType, Dict[str, Any]], Awaitable[Any]]
MiddlewareType = Union[
    BaseMiddleware,
    Callable[
        [NextMiddlewareType[MiddlewareEventType], MiddlewareEventType, Dict[str, Any]],
        Awaitable[Any],
    ],
]
