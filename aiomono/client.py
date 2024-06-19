import logging
from datetime import datetime, timezone, timedelta
from typing import List, Union, Dict, Optional, Any

import aiohttp
from aiohttp import ClientResponse

from aiomono.exceptions import (
    MonoException,
    SyncContextManagerException,
    ToManyRequests,
)
from aiomono.types import Currency, ClientInfo, StatementItem, Webhook
from aiomono.utils import validate_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aiomono")

API_ENDPOINT = "https://api.monobank.ua"


class MonoClient:
    def __init__(self):
        self.__session: Optional[aiohttp.ClientSession] = None

    async def get_currency(self) -> List[Currency]:
        """Returns list of courses"""
        currency_list = await self.get("/bank/currency")
        return [Currency(**currency) for currency in currency_list]

    async def __check_response(self, response: ClientResponse) -> Union[List, Dict]:
        if not response.ok:
            if response.status == 249:
                raise ToManyRequests(await response.text())
            raise MonoException(await response.text())
        return await response.json()

    async def request(self, method, endpoint, **kwargs) -> Any:
        return await self.__check_response(
            await self.__session.request(method, API_ENDPOINT + endpoint, **kwargs)
        )

    async def get(self, endpoint: str, **kwargs) -> Union[List, Dict]:
        return await self.request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> Union[List, Dict]:
        return await self.request("POST", endpoint, **kwargs)

    @property
    def session(self) -> aiohttp.ClientSession:
        if not self.__session or self.__session.closed:
            self.__session = aiohttp.ClientSession()
        return self.__session
    
    @session.setter
    def session(self, value: aiohttp.ClientSession) -> None:
        if not isinstance(value, aiohttp.ClientSession):
            raise ValueError("Session must be aiohttp.ClientSession instance")
        self.__session = value

    async def close(self) -> None:
        if self.__session and not self.__session.closed:
            await self.__session.close()
            logger.info("Session closed")

    async def __aenter__(self):
        if not self.__session or self.__session.closed:
            self.__session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        await self.close()

    def __enter__(self):
        raise SyncContextManagerException(
            "Use async context manager instead of sync context manager"
        )

    def __exit__(self):
        raise SyncContextManagerException(
            "Use async context manager instead of sync context manager"
        )


class PersonalMonoClient(MonoClient):
    def __init__(self, token: str):
        super().__init__()

        self.token = token
        self.headers = {"X-Token": self.token}

        validate_token(self.token)

    async def client_info(self) -> ClientInfo:
        """Returns client info"""
        client_info = await self._get("/personal/client-info", headers=self.__headers)
        return ClientInfo(**client_info)

    async def set_webhook(self, webhook_url: str) -> Webhook:
        """Setting new webhook url"""
        payload = {"webHookUrl": webhook_url}
        await self.post("/personal/webhook", json=payload, headers=self.__headers)
        return {"web_hook_url": webhook_url}

    async def get_statement(
        self,
        account_id: str,
        date_from: datetime = datetime.now(timezone.utc) - timedelta(weeks=4),
        date_to: datetime = datetime.now(timezone.utc),
    ):
        """Returns list of statement items"""
        date_from = int(date_from.replace(tzinfo=timezone.utc).timestamp())
        date_to = int(date_to.replace(tzinfo=timezone.utc).timestamp())
        endpoint = f"/personal/statement/{account_id}/{date_from}/{date_to}"
        statement_items = await self.get(endpoint, headers=self.__headers)
        return [StatementItem(**statement_item) for statement_item in statement_items]


class CorporateMonoClient(MonoClient): ...
