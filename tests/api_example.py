import requests

class API:

    def get_stuff(self):
        response = requests.get("https://home.openweathermap.org/users/sign_up")
        return response
