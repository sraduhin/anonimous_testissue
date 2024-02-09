import json

from httpx import AsyncClient
from tests.conftest import client, ac
from src.main import app
import pytest
import tempfile
import os


def read_file(filepath):
    with open(filepath, 'rb') as f:
        return f.read().decode()

class TestOrder:
    url = "/api/v1/order/load_files/"
    order_file = "./tests/fixtures/example_order.json"
    payment_file = "./tests/fixtures/example_payment.json"

    # @pytest.mark.parametrize()
    def test_order(self):
        files = {
            "order": ("./tests/fixtures/example_order.json", open(self.order_file, "rb")),
            "payment": ("./tests/fixtures/example_payment.json", open(self.payment_file, "rb")),
        }
        response = client.post(self.url, files=files)
        assert response.status_code == 200

        order_data = read_file(self.order_file)
        payment_data = read_file(self.order_file)

        with tempfile.TemporaryDirectory() as tempdir:
            tempfile_order_path = os.path.join(tempdir, 'order.json')
            tempfile_payment_path = os.path.join(tempdir, 'payment.json')

            with open(tempfile_order_path, 'w') as temp_f1, open(tempfile_payment_path, 'w') as temp_f2:

                temp_f1.write(order_data)
                temp_f2.write(payment_data)


            with open(tempfile_order_path, 'r') as temp_f1, open(tempfile_payment_path, 'r') as temp_f2:

                check = temp_f1.write(order_data) #  тут у меня данные не записываются



            files = {
                "order": (tempfile_order_path,
                          open(tempfile_order_path, "rb")),
                "payment": (tempfile_payment_path,
                            open(tempfile_payment_path, "rb")),
            }
            response = client.post(self.url, files=files)
            assert response.status_code == 200



