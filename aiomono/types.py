from decimal import Decimal
from typing import TypedDict

from pydantic import BaseModel, Field


class Webhook(TypedDict):
    web_hook_url: str


class Currency(BaseModel):
    currency_code_a: int = Field(alias="currencyCodeA")
    currencyCodeB: int = Field(alias="currencyCodeB")
    date: int
    rate_sell: Decimal | None = Field(default=None, alias="rateSell")
    rate_buy: Decimal | None = Field(default=None, alias="rateBuy")
    rate_cross: Decimal | None = Field(default=None, alias="rateCross")


class Account(BaseModel):
    id: str
    send_id: str = Field(alias="sendId")
    balance: Decimal
    credit_limit: int = Field(alias="creditLimit")
    type: str
    currency_code: int = Field(alias="currencyCode")
    cashback_type: str = Field(alias="cashbackType")
    masked_pan: list[str] | None = Field(default=None, alias="maskedPan")
    iban: str | None = None


class Jar(BaseModel):
    id: str
    send_id: str = Field(alias="sendId")
    title: str
    description: str
    currency_code: int = Field(alias="currencyCode")
    balance: Decimal
    goal: Decimal


class ClientInfo(BaseModel):
    id: str
    name: str
    webhook_url: str
    accounts: list[Account] = Field(default_factory=lambda: list())
    jars: list[Jar] = Field(default_factory=lambda: list())

    # class Config:
    #     fields = {"id": "clientId", "webhook_url": "webHookUrl"}


class StatementItem(BaseModel):
    id: str
    time: int
    description: str
    mcc: int
    original_mcc: int = Field(alias="originalMcc")
    hold: bool
    amount: Decimal
    operation_amount: Decimal = Field(alias="operationAmount")
    currency_code: int = Field(alias="currencyCode")
    commission_rate: Decimal = Field(alias="commissionRate")
    cashback_amount: Decimal = Field(alias="cashbackAmount")
    balance: Decimal
    comment: str
    receipt_id: str = Field(alias="receiptId")
    invoice_id: str = Field(alias="invoiceId")
    counter_edrpou: str = Field(alias="counterEdrpou")
    counter_iban: str = Field(alias="counterIban")
    counter_name: str = Field(alias="counterName")
