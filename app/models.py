from dataclasses import dataclass


@dataclass
class Item:
    title: str
    link: str
    price: int
    old_price: int
    img: str
    description: str


@dataclass
class Card:
    price: str
    old_price: str
    description: str
    title: str
