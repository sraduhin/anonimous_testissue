from abc import abstractmethod
from bs4 import BeautifulSoup
from schemas.models import Payment, Order, Sellers
import json


class BaseFileValidator:
    @abstractmethod
    async def parse_file():
        raise NotImplementedError


class JSONPaymentValidator(BaseFileValidator):
    async def parse_file(self, filedata):
        json_ = json.loads(filedata)
        return {"СрокОплаты": json_["payment"]["deadline"]["text"]}


class JSONOrderValidator(BaseFileValidator):
    async def parse_file(self, filedata):
        json_ = json.loads(filedata)
        order = json_["order"]
        sellers = order["sellers"]
        payment = Payment(**order["payment"])
        return Order(
            order_date=order["@attributes"]["order_date"],
            sellers=Sellers.from_dict(sellers),
            payment=payment,
        )


class XMLPaymentValidator(BaseFileValidator):
    async def parse_file(self, filedata):
        soup = BeautifulSoup(filedata, "html.parser")
        return {"СрокОплаты": soup.deadline.time.string}


class XMLOrderValidator(BaseFileValidator):
    async def parse_file(self, filedata):
        soup = BeautifulSoup(filedata, "html.parser")
        sellers = soup.order.sellers.find_all("name")
        payment = Payment(
            val=soup.order.payment.val.string,
            decimal=soup.order.payment.decimal.string,
            currency=soup.order.payment.currency.string,
        )
        return Order(
            order_date=soup.order["orderdate"],
            sellers=Sellers.from_list(sellers),
            payment=payment,
        )
