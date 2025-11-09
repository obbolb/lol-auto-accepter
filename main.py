import requests 
import os
import base64 

def get_client_data(path: str = r"C:\Riot Games\League of Legends") ->tuple[int,str] | None:
    """
    Reads the client 'lockfile' and returns the port and password used by the league client
    lockfile format-> (Process Name : Process ID : Port : Password : Protocol)
    """
    try: 
        with open(os.path.join(path,'lockfile')) as f:
            contents = f.read().split(':')
            node,password = contents[2],contents[3]
            return node,password

    except OSError:
        print("Please open the client before using this")
        return None
    
def get_auth_key(password: str) ->str:
    """
    Generate a Base64-encoded authentication key for an HTTP Basic Auth header.
    The returned string is the Base64 encoding of "riot:<password>".
    This value can be used as the value for the "Authorization: Basic ..." header.
    read more at https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Authorization
    """
    raw = f"riot:{password}".encode("utf-8")
    key = base64.b64encode(raw).decode("utf-8") 
    return key

def check_match_found() ->bool:
    """
    check if match found 
    """
    pass
    
    
            




