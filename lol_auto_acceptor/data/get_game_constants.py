import json
from pprint import pprint
import requests
import os


def check_current_version() -> str:
    data = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()
    return data[0]


def get_champ_id():
    current_version = check_current_version()
    if os.path.exists("data/champ_id.json"):
        with open("data/champ_id.json", "r") as f:
            json_data = json.load(f)

            if current_version == json_data["version"]:
                return json_data

    new_json_data = requests.get(
        f"https://ddragon.leagueoflegends.com/cdn/{current_version}/data/en_US/champion.json"
    ).json()

    champ_id = {"version": current_version}  
    champ_id.update({champ: info["key"] for champ, info in new_json_data["data"].items()}) #appending the champ id values

    with open("data/champ_id.json", "w") as f:
        json.dump(champ_id, f, indent=4)
    return champ_id

if __name__ =="__main__":
    get_champ_id()