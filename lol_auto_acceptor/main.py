from client.LeagueClient import LeagueClient
import sys
import ssl
if __name__ == "__main__":
    try:
        while True:
            print("close program with ctrl-c")
            
            client = LeagueClient()
            client.connect()
            print(client.port)
            client.queue()
            print("exit program succesfully")
    except KeyboardInterrupt:
        print("closing program...")
        sys.exit(0)
