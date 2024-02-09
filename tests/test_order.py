from tests.conftest import client
import tempfile
import os
import pytest


def read_file(filepath):
    with open(filepath, 'rb') as f:
        return f.read().decode()


class TestOrder:
    url = "/api/v1/order/load_files/"
    expected_file = "./tests/fixtures/pass.txt"
    order_file = "./tests/fixtures/example_order.json"
    payment_file = "./tests/fixtures/example_payment.json"
    origins = ("5 ноября 2022 г", "05.11.2022", "2022_12_1_5")

    replaced = [
        ((origins[0], "5 ноября 2023 г"), ((origins[1], "05.11.2023"), (origins[2], "2023_12_1_5"))),
        ((origins[0], "5 ноября 1999 года"), ((origins[1], "05.11.1999"), (origins[2], "1999_12_1_5"))),
        ((origins[0], "05 ноября 2023 г"), ((origins[1], "05.11.2023"), (origins[2], "2023_12_1_5"))),
        ((origins[0], "5.11.2023 г"), ((origins[1], "05.11.2023"), (origins[2], "2023_12_1_5"))),
        ((origins[0], "05.11.2023 г"), ((origins[1], "05.11.2023"), (origins[2], "2023_12_1_5"))),
        ((origins[0], "5 нбр 2023 г"), ((origins[1], "05.11.2023"), (origins[2], "2023_12_1_5"))),
        # BOOOOOOO000000000000000ooooooooMММММММММММ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ((origins[0], "5 ноября 23 г"), ((origins[1], "05.11.2023"), (origins[2], "2023_12_1_5"))),
        ((origins[0], "5 ноября 2023 г"), ((origins[1], "05.11.2023"), (origins[2], "2023_12_1_5"))),
    ]


    @pytest.mark.parametrize("source_sub,output_subs", replaced)
    def test_order(self, source_sub, output_subs):

        order_data = read_file(self.order_file)
        payment_data = read_file(self.payment_file)

        with tempfile.TemporaryDirectory() as tempdir:
            tempfile_order_path = os.path.join(tempdir, 'order.json')
            tempfile_payment_path = os.path.join(tempdir, 'payment.json')

            with open(tempfile_order_path, 'w') as temp_f1, open(tempfile_payment_path, 'w') as temp_f2:

                temp_f1.write(order_data.replace(source_sub[0], source_sub[1]))
                temp_f2.write(payment_data)

            files = {
                "order": (tempfile_order_path,
                          open(tempfile_order_path, "rb")),
                "payment": (tempfile_payment_path,
                            open(tempfile_payment_path, "rb")),
            }
            response = client.post(self.url, files=files)
            assert response.status_code == 200

            with open(self.expected_file, 'r') as f:
                expected = f.read()
                expected = expected.replace(output_subs[0][0], output_subs[0][1])
                expected = expected.replace(output_subs[1][0], output_subs[1][1])
                assert response.content.decode() == expected
