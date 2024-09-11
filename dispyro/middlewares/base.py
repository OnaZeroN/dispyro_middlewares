from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Dict, TypeVar

from pyrogram import Client
from dispyro.types import Update

T = TypeVar("T")


class BaseMiddleware(ABC):
    """
    Generic middleware class
    """

    @abstractmethod
    async def __call__(
        self,
        handler: Callable[[Client, Update, Dict[str, Any]], Awaitable[Any]],
        client: Client,
        update: Update,
        data: Dict[str, Any],
    ) -> Any:  # pragma: no cover
        """
        Execute middleware

        :param handler: Wrapped handler in middlewares chain
        :param update: Incoming update
        :param data: Contextual data. Will be mapped to handler arguments
        :return: :class:`Any`
        """
        pass
