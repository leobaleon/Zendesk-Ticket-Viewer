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

# makes the GET request to the Zendesk API and parses the JSON data
payload = get(ORIGINALURL, auth=(USERNAME, PASSWORD))
jsonResponse = payload.json()

# this form of indexing filters the JSON data to the desired values
    # print(jsonResponse["tickets"][0]["url"])

def allTickets():
    print("Temporary")

def singleTicket():
    ticketNumber = input("Enter a ticket number:\n")

def menu(userInput):
    

    while userInput != 'quit':
        userInput = input("\n\tSelect view options:\n" \
                        "\t* Press 1 to view all tickets\n" \
                        "\t* Press 2 to view a ticket\n" \
                        "\t* Type \'quit\' to exit\n")

        # view all tickets
        if userInput == '1':
            allTickets()
        elif userInput == '2':
            singleTicket()
        elif userInput != 'quit':
            print("Invalid entry")

def main():
    # prompt and get user input
    userInput = input("Welcome to the ticket viewer\n" \
                    "Type \'menu\' to view options or \'quit\' to exit\n")
    
    # validate user input?
    while userInput != "menu" and userInput != "quit":
        userInput = input("Invalid entry\n" \
                        "Type \'menu\' to view options or \'quit\' to exit\n")

    if userInput == "menu":
        menu(userInput)
    else:
        return 0

if __name__ == "__main__": main()

# Things to test for:
# 1) Couldn't connect to the API
# 2) No tickets were returned
# 3) The requested ticket was not found
# 4) User types in invalid input