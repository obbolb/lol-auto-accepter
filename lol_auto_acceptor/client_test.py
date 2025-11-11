from client.LeagueClient import LeagueClient
import sys

'''
wanna test:
/lol-champ-select/v1/session/my-selection -> หลังกดล้อคตัว
/lol-champ-select/v1/session -> กดทั้งช่วงเเบน พิ้ค หลังกดตัว หลังช่วงเลือกรูน


'''
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
