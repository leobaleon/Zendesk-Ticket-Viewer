# To-Do List:
# ● Connect to the Zendesk API
# ● Request all the tickets for your account
# ● Display them in a list
# ● Display individual ticket details
# ● Page through tickets when more than 25 are returned

from requests import get
import os
import math

# original url for making GET request
ORIGINALURL = 'https://zccsonmac.zendesk.com/api/v2/tickets.json'

# read username and password from environment variables
USERNAME = os.environ['USER']
PASSWORD = os.environ['PASS']

# makes the GET request to the Zendesk API and parses the JSON data
payload = get(ORIGINALURL, auth=(USERNAME, PASSWORD))
jsonResponse = payload.json()

def display(ticketNumber):
    print("Ticket with subject \'" + \
            jsonResponse['tickets'][ticketNumber]['subject'] + \
            "\' opened by " + \
            str(jsonResponse['tickets'][ticketNumber]['requester_id']) + \
            " on " + \
            jsonResponse['tickets'][ticketNumber]['created_at'])

def displayTickets(start, num):
    # to return the number of tickets displayed in this function call
    count = 0

    # for each ticket in the specifed number of tickets to display
    for i in range(start, start+num):
        display(i)

        # keep count
        count += 1

    return count

def allTickets():
    # max tickets per page
    max = 25

    # total tickets
    total = jsonResponse['count']

    # remaining number of tickets to display
    remaining = total

    # current page
    page = 1

    # starting ticket
    start = 0

    # count returned
    count = 0

    # check if there are more than 25 tickets (for pagination)
    if remaining > max:
        # to keep getting more pages as long as the user desires
        while remaining > 0:
            # display up to 25 tickets at a time. the ternary operator will check
            # if the remaining tickets is greater than 25, and will set a max of 25
            # if true, or simply send in the remaining tickets otherwise
            count = displayTickets(start, max if remaining > max else remaining)

            # update values after each call
            remaining -= count
            start += count
            
            # print the current page and total page count
            print("Page " + str(page) + " of " + str(math.ceil(total / 25)))

            if remaining > 0:
                userInput = input("\nPress 1 to view the next page, anything else to return to the previous menu:\n")

            if userInput != '1' or remaining == 0:
                break
            else:
                page += 1
                
    else:
        displayTickets(start, remaining)

def singleTicket():
    # total tickets
    total = jsonResponse['count']

    ticketNumber = int(input("Enter a ticket number:\n"))

    # validate ticket number
    while ticketNumber >= total or ticketNumber < 0:
        ticketNumber = int(input("Invalid ticket number\nEnter a ticket number:\n"))

    display(ticketNumber)


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

    print("Thanks for using the viewer. Goodbye.")
    return 0

if __name__ == "__main__": main()

# Things to test for:
# 1) Couldn't connect to the API
# 2) No tickets were returned
# 3) The requested ticket was not found
# 4) User types in invalid input