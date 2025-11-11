import requests
import os
import time
from client.ChampSelect import ChampSelect

default_path = r"C:\Riot Games\League of Legends"
cert_path = r"cert/riotgames.pem"  # certification for riot self signed cerification


class LeagueClient:
    def __init__(self, path=default_path, **ban_pick_data):
        self.path:str = path
        self.key:str = None
        self.url:str = None
        self.port:str = None
        self.password:str = None
        self.champ_select = ChampSelect(self,**ban_pick_data)

    def _load_lockfile(self) -> tuple[str, str]:
        """
        Reads the client 'lockfile' and assign the port and password used by the league client
        lockfile format-> (Process Name : Process ID : Port : Password : Protocol)
        """
        try:
            with open(os.path.join(self.path, "lockfile")) as f:
                _, _, port, password, _ = f.read().split(":")  # _ is a placeholder
                return port, password
        except OSError:
            return None

    def _build_url(self, port) -> str:
        """
        Concatenate the port League Client API is currently using to the local host IP.
        """
        return f"https://127.0.0.1:{port}"

    def connect(self, *, reconnect=False) -> bool:
        """
        Assign parameters neccessary for an HTTP request to the class
        """
        if not (data := self._load_lockfile()):
            if reconnect:
                print("Client not opened")
                return False
            else:
                return False
        

        self.port, self.password = data
        self.url = self._build_url(self.port)
        print("Succesfully connected")
        return True

    def _reconnect(self) -> bool:
        """
        wait for the game to be opened again
        used instead of connect after initial connection
        if not connected after 20 tries close the program
        """
        max_retry = 20
        i = 0
        print("trying to reconnect")
        while not self.connect(reconnect=True):
            if i > max_retry:
                raise Exception("terminated program because league not opened")
            time.sleep(10)
            i += 1
        return True

    def requests(self, request, api_dir, **data) -> requests.Response | None:
        for _ in range(2):
            try:
                match request:
                    case "GET":
                        return requests.get(
                            f"{self.url}{api_dir}",
                            auth=("riot", self.password),
                            verify=cert_path,
                        )
                    case "POST":
                        return requests.post(
                            f"{self.url}{api_dir}",
                            auth=("riot", self.password),
                            verify=cert_path,
                            data=data,
                        )
                    case _:
                        raise ValueError("Invalid Method")
            # error handling if game not opened
            except requests.exceptions.RequestException:
                print("Client not opened")
                self._reconnect()

    def queue(self) -> None:
        """
        the post request returns 3 codes
        203: match found
        500: in queue
        404: not in queue
        in_queue,wait is a flag to track the state of queue
        to prevent printing status message multiple times
        """
        in_queue = False
        wait = False
        while True:
            response = self.requests("POST", "/lol-matchmaking/v1/ready-check/accept")

            match (response.status_code):
                case 203:
                    print("accepted match")
                    break
                case 500:
                    if in_queue == False:
                        print("In queue ...")
                        in_queue = True
                    if wait == True:
                        wait = False
                case _:
                    if wait == False:
                        print("waiting for queue start...")
                        wait = True
                    if in_queue == True:
                        in_queue = False
            time.sleep(5)
