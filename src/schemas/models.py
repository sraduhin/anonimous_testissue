from typing import List, Dict
from pydantic import BaseModel
from utils.normalize import (
    get_date,
    get_deadline_date,
)


class Payment(BaseModel):
    val: str
    decimal: str
    currency: str

    def dump(self):
        return {
            "Сумма": f"{self.val},{self.decimal} {self.currency}",
        }


class Sellers:
    # for json
    @classmethod
    def from_dict(cls, coll: Dict[str, str]):
        return [
            value["name"] for key, value in coll.items() if key != "@attributes"
        ]

    # for xml
    @classmethod
    def from_list(cls, coll: list):
        return [item.string for item in coll]


class Order(BaseModel):
    order_date: str
    sellers: List[str]
    payment: Payment

    def dump(self, deadline: dict):
        order_date = get_date(self.order_date)
        dd_date = get_deadline_date(order_date, deadline["СрокОплаты"])
        payment = self.payment.dump()
        payment.update({
            "СрокОплаты": f"{dd_date.year}_{dd_date.month}_{(dd_date.day - 1) // 7 + 1}_{dd_date.day}"
        })
        return {
            "ДатаДокумента": order_date.strftime("%d.%m.%Y"),
            "Продавец": self.sellers,
            "Оплата": payment,
        }
