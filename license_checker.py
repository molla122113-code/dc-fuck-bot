import requests

from datetime import datetime

from config import (
    CLIENT_ID,
    LICENSE_SERVER
)


def check_license():

    try:

        r = requests.get(
            f"{LICENSE_SERVER}/api/{CLIENT_ID}",
            timeout=10
        )

        data = r.json()

        if data["status"] != "active":

            return False, data

        expire = datetime.strptime(
            data["expires"],
            "%Y-%m-%d"
        )

        if datetime.utcnow() > expire:

            return False, data

        return True, data

    except:

        return False, {
            "status": "error"
        }