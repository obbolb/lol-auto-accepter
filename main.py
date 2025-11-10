import requests 
import os
import base64 
import time

default_path = r"C:\Riot Games\League of Legends"
cert_path = r"cert/riotgames.pem" #certification for riot self signed cerification

class client():
    def __init__(self, path=default_path):
        self.path = path
        self.key = None
        self.url = None

    def _load_lockfile(self,path) ->tuple[str,str]:
        """
        Reads the client 'lockfile' and assign the port and password used by the league client 
        lockfile format-> (Process Name : Process ID : Port : Password : Protocol)
        """
        try: 
            with open(os.path.join(path,'lockfile')) as f:
                _, _, port, password, _ = f.read().split(':') #_ is a placeholder
                return port, password
        except OSError:
            return None
        
    

    def _build_url(self, port) ->str:
        """
        Concatenate the port League Client API is currently using to the local host IP.
        """
        return f"https://127.0.0.1:{port}"
    
    def connect(self) ->bool:
        """
        Assign parameters neccessary for an HTTP request to the class
        """
        if not (data := self._load_lockfile(self.path)): 
            print("Open the client pls")
            return False
        
        port, self.password = data
        self.url = self._build_url(port)
        print("Succesfully connected")
        return True

    def reconnect(self):
        print("trying to reconnect")
        while not client.connect():
            time.sleep(10)
        
    def get(self,api_dir) ->requests.Response | None:
        """
        get response wrapper pass api_dir with a slash in front 
        """
        try:
            response=requests.get(f"{self.url}{api_dir}", auth=('riot',self.password), verify=cert_path)
        except requests.exceptions.RequestException:
            print("Client not opened")
            client.reconnect()
            return None

        return response
    
    def post(self, api_dir, **data:dict) ->requests.Response | None:
        try:
            response=requests.post(f"{self.url}{api_dir}", auth=('riot',self.password), verify=cert_path, data=data)
        except requests.exceptions.RequestException:
            print("Client not opened")
            client.reconnect()
            return None

        return response

    def client_opened(self) ->bool:
        """
        check if client is currently opened
        """
        response=client.get('/riotclient/ux-state')
        return response is not None

    def accept_queue(self)->bool:
        in_queue=False
        wait = False
        while True:
            response=client.post('/lol-matchmaking/v1/ready-check/accept')
            
            match(response.status_code):
                case 203:
                    print("accepted match")
                    break
                case 500:
                    if in_queue==False:
                        print("In queue ...")
                        in_queue=True
                    if wait == True:
                        wait=False    
                case _:
                    if wait==False:
                        print("waiting for queue start...")
                        wait=True
                    if in_queue==True:
                        in_queue=False
            time.sleep(5)

        
        


    
if __name__ == "__main__":
    client=client()
    client.connect()
    while client.client_opened():
        client.accept_queue()
    print("exit program succesfully")    

            
        




