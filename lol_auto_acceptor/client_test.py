from client.LeagueClient import LeagueClient
import sys


try:
    client = LeagueClient()
    client.connect()
    while True:
        api_endpoint = input("endpoint: ")
        response=client.requests("GET", api_endpoint)
        print(response.json())

except KeyboardInterrupt:
    print("exit..")
    sys.exit()
