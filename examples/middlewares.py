import asyncio
from typing import Any, Awaitable, Callable, Dict

from pyrogram import Client, filters, types
from dispyro import Dispatcher, Router
from dispyro.types import Update
from dispyro.middlewares.base import BaseMiddleware


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Client, Update, Dict[str, Any]], Awaitable[Any]],
            client: Client,
            update: Update,
            data: Dict[str, Any],
    ) -> Any:
        print(f"Logging: Received update of type {type(update).__name__}")
        result = await handler(client, update, data)
        print(f"Logging: Finished processing update")
        return result


class AuthMiddleware(BaseMiddleware):
    def __init__(self, password: str):
        self.password = password

    async def __call__(
            self,
            handler: Callable[[Client, Update, Dict[str, Any]], Awaitable[Any]],
            client: Client,
            update: Update,
            data: Dict[str, Any],
    ) -> Any:
        if update.text and self.password in update.text:
            return await handler(client, update, data)
        print(f"Auth: Incorrect password")
        return None


class TimingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Client, Update, Dict[str, Any]], Awaitable[Any]],
            client: Client,
            update: Update,
            data: Dict[str, Any],
    ) -> Any:
        start_time = asyncio.get_event_loop().time()
        result = await handler(client, update, data)
        end_time = asyncio.get_event_loop().time()
        print(f"Timing: Handler took {end_time - start_time:.2f} seconds")
        return result


class DataEnrichmentMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Client, Update, Dict[str, Any]], Awaitable[Any]],
            client: Client,
            update: Update,
            data: Dict[str, Any],
    ) -> Any:
        if isinstance(update, types.Message):
            data['enriched_data'] = f"Extra info for message {update.id}"
        return await handler(client, update, data)


router = Router()
router.message.filter(filters.me)

router.message.outer_middleware(LoggingMiddleware())
router.message.outer_middleware(AuthMiddleware(password="pass"))
router.message.middleware(TimingMiddleware())
router.message.middleware(DataEnrichmentMiddleware())


@router.message(filters.command("ping", prefixes="."))
async def ping_handler(client: Client, message: types.Message, enriched_data: str):
    await message.edit_text(text=f"🏓 Pong! {enriched_data}")
    return True


@router.message(filters.command("echo", prefixes="."))
async def echo_handler(client: Client, message: types.Message):
    await message.reply_text(text=message.text)


async def main():
    client = Client(
        name="dispyro",
        api_id=2040,  # TDesktop api_id, better to be replaced with your value
        api_hash="b18441a1ff607e10a989891a5462e627",  # TDesktop api_hash, better to be replaced with your value
    )
    dispatcher = Dispatcher(client)
    dispatcher.add_router(router)
    await dispatcher.start()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
