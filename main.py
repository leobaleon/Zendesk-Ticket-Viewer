# To-Do List:
# ● Connect to the Zendesk API
# ● Request all the tickets for your account
# ● Display them in a list
# ● Display individual ticket details
# ● Page through tickets when more than 25 are returned

from requests import get
import os

# original url for making GET request
ORIGINALURL = 'https://zccsonmac.zendesk.com/api/v2/tickets.json'

# read username and password from environment variables
USERNAME = os.environ['USER']
PASSWORD = os.environ['PASS']

def main():
    payload = get(ORIGINALURL, auth=(USERNAME, PASSWORD))
    jsonResponse = payload.json()
    # print(payload.content)
    print("The first ticket info:")

    # this form of indexing filters the JSON data to the desired values
    print(jsonResponse["tickets"][0]["url"])

    # print(USERNAME, PASSWORD)


if __name__ == "__main__": main()