import json

import urequests


class ApiInterface:
    __HEADERS = {
        "accept": "application/json"
    }

    def __init__(self, base_url: str):
        if "https" in base_url:
            raise ValueError("Base URL must not contain https://")
        if "http://" not in base_url:
            base_url = "http://" + base_url

        self.__base_url = base_url
        self.__health_url = base_url + "/health"
        self.__play_url = base_url + "/play"
        self.__device_url = base_url + "/device"
        self.__next_device_url = self.__device_url + "/next"
        self.__previous_device_url = self.__device_url + "/previous"

    def request(self, method: str, url: str, data=None, params=None) -> urequests.Response:
        if data is None:
            data = {}
        if params is None:
            params = {}

        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        if query_string:
            url = f"{url}?{query_string}"

        print(f"Requesting {method} {url} {'with data' if data else ''}...")

        if method == "GET":
            if data:
                raise ValueError("GET requests cannot have data, use params instead")

            resp = urequests.request(method, url, headers=self.__HEADERS)
        else:
            resp = urequests.request(method, url, headers=self.__HEADERS, data=json.dumps(data))

        print(f"Response ({resp.status_code}): {resp.text}")

        return resp

    def check_health(self) -> bool:
        try:
            return self.request("GET", self.__health_url).status_code == 200
        except:
            return False

    def get_current_device(self, reset: bool = False) -> dict:
        return self.request("GET", self.__device_url, params={"reset": reset}).json()

    def next_device(self) -> dict:
        return self.request("POST", self.__next_device_url).json()

    def previous_device(self) -> dict:
        return self.request("POST", self.__previous_device_url).json()

    def play(self, track: str) -> dict:
        return self.request("POST", self.__play_url, {"id": track}).json()
