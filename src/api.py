import json

import urequests


class ApiInterface:
    __HEADERS = {
        "accept": "application/json"
    }

    __BASE_URL = "http://185.185.71.49:8000"
    __HEALTH_URL = __BASE_URL + "/health"
    __DEVICE_URL = __BASE_URL + "/device"
    __NEXT_DEVICE_URL = __DEVICE_URL + "/next"
    __PREVIOUS_DEVICE_URL = __DEVICE_URL + "/previous"
    __PLAY_URL = __BASE_URL + "/play"

    def request(self, method: str, url: str, data=None) -> urequests.Response:
        if data is None:
            data = {}

        if method == "GET":
            resp = urequests.request(method, url, headers=self.__HEADERS)
        else:
            resp = urequests.request(method, url, headers=self.__HEADERS, data=json.dumps(data))

        print(resp.status_code)
        print(resp.text)
        return resp

    def check_health(self) -> bool:
        try:
            return self.request("GET", self.__HEALTH_URL).status_code == 200
        except:
            return False

    def get_current_device(self) -> dict:
        return self.request("GET", self.__DEVICE_URL).json()

    def next_device(self) -> dict:
        return self.request("POST", self.__NEXT_DEVICE_URL).json()

    def previous_device(self) -> dict:
        return self.request("POST", self.__PREVIOUS_DEVICE_URL).json()

    def play(self, track: str) -> dict:
        return self.request("POST", self.__PLAY_URL, {"id": track}).json()
