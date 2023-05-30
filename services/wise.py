import requests
from decouple import config
from fastapi import Depends, FastAPI, HTTPException, Request, status


#!WiseService
class WiseService:
    def __init__(self):
        self.main_url = ""
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}",
        }
        self.profile_id = self._get_profile_id()

    # get_profile_id
    def _get_profile_id(self):
        url = "https://api.sandbox.transferwise.tech/v2/profiles"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            response = response.json()
            return [el["id"] for el in response if el["type"] == "PERSONAL"]
        print("Response is ", response)
        raise HTTPException(500, "Payment provider is not available at the moment")
