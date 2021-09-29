from typing import TypedDict


class Description(TypedDict):
    type: str
    value: str


class Action(TypedDict):
    name: str
    link: str


class MarketAction(TypedDict):
    name: str
    link: str


class Tag(TypedDict):
    internal_name: str
    name: str
    category: str
    category_name: str
