import json
import uuid

import requests
from decouple import config
from fastapi import Depends, FastAPI, HTTPException, Request, status

from services import wise


#!WiseService
class WiseService:
    def __init__(self):
        self.main_url = f"{config('WiSE_URL')}"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}",
        }
        self.profile_id = self._get_profile_id()

    # get_response_data
    def get_response_data(self, url, data=None, http_method=None):
        response = (
            requests.get(url, headers=self.headers)
            if http_method == "GET"
            else (
                requests.post(url, headers=self.headers, data=json.dumps(data))
                if http_method == "POST"
                else "Not found method for this process"
            )
        )

        # print("Ne verir bas ", response.json())
        print("Statuc code is ", response)

        try:
            if response.status_code == 200:
                response = response.json()
            return response
        except:
            raise HTTPException(500, "Payment provider is not available at the moment")

    # get_profile_id
    def _get_profile_id(self):
        url = f"{config('WiSE_URL')}/v2/profiles"
        response = self.get_response_data(url, http_method="GET")
        return [el["id"] for el in response if el["type"] == "PERSONAL"]

    # create_quote
    def create_quote(self, amount):
        url = f"{config('WiSE_URL')}/v2/quotes"
        data = {
            "sourceCurrency": "EUR",
            "targetCurrency": "EUR",
            "sourceAmount": f"{amount}",
            "profile": f"{config('WISE_PROFILE_ID')}",
        }
        response = self.get_response_data(url, data, http_method="POST")
        print("Quoter createad ", response)
        return response["id"]

    # create_recipient_account
    def create_recipient_account(self, full_name, iban):
        print("Full Name Is", full_name)
        url = f"{config('WiSE_URL')}/v1/accounts"
        data = {
            "currency": "EUR",
            "type": "iban",
            "profile": f"{config('WISE_PROFILE_ID')}",
            "accountHolderName": f"{full_name}",
            "legalType": "PRIVATE",
            "details": {"iban": f"{iban}"},
        }
        response = self.get_response_data(url, data, http_method="POST")
        print("Response data ", response)
        return response["id"]

    # create_transfer
    def create_transfer(self, target_account_id, quote_id):
        customer_transaction_id = str(uuid.uuid4())
        url = f"{config('WiSE_URL')}/v1/transfers"
        data = {
            "targetAccount": f"{target_account_id}",
            "quoteUuid": f"{quote_id}",
            "customerTransactionId": f"{customer_transaction_id}",
            "details": {},
        }
        response = self.get_response_data(url, data, http_method="POST")
        return response["id"]

    def fund_transfer(self, transfer_id):
        url = f"{config('WiSE_URL')}/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments".replace(
            "[", ""
        ).replace(
            "]", ""
        )
        data = {"type": "BALANCE"}
        response = self.get_response_data(url, data, http_method="POST")
        return response

    def cancel_transfer(self, transfer_id):
        url = f"{config('WiSE_URL')}/v1/transfers/{transfer_id}/cancel"
        response = requests.put(url, headers=self.headers)
        if response.status_code == 200:
            response = response.json()
            return response["id"]
        else:
            print("Cancel response value is ", response)
            raise HTTPException(
                status_code=500,
                detail="Payment provider not is not available at the moment",
            )


# if __name__ == "__main__":
#     wise = WiseService()
#     profile_id = wise._get_profile_id()
#     quote_id = wise.create_quote(58)
#     recepient_id = wise.create_recipient_account(
#         "UsernameTest SurnameTest", ""
#     )
#     print("Profile  ", profile_id)
#     print("################################################################33")
#     print("Quote ", quote_id)
#     print("################################################################33")
#     print("Recepient", recepient_id)

#     transfer_id = wise.create_transfer(recepient_id, quote_id)

#     print(
#         "Transfer successfully released not yet confirm transaction but sending verivief ",
#         transfer_id,
#     )

#     transfer_money = wise.fund_transfer(transfer_id)

#     print("Pay transfer successfully ", transfer_money)
