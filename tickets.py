from requests import get
import os
import math

class TicketViewer:
    # class member variables
    url = 'https://zccsonmac.zendesk.com/api/v2/tickets.json'
    username = ''
    password = ''
    jsonData = ''

    # constructor attempts to retrieve environment variables for username and 
    # password for GET request from Zendesk API, also makes the call to getJSON()
    # to initialize jsonData
    def __init__(self) -> None:
        try:
            # read username and password from environment variables
            self.username = os.environ['USER']
            self.password = os.environ['PASS']
        except KeyError:
            print("Could not retrieve appropriate values for username and password...\n" + \
                "Did you export the required environment variables correctly?")
        else:
            print("Environment variables loaded successfully!")

        # get JSON data from Zendesk API
        self.jsonData = self.getJSON()

    # this function will attempt a GET request and return the payload as JSON data.
    # if the connection fails, this function will return -1 to set jsonData as a flag
    # that indicaties this failure
    def getJSON(self) -> str:
        try:
            # GET request with authorization info
            payload = get(self.url, auth=(self.username, self.password))

            # make sure the connection was successful, otherwise exception
            if payload.status_code != 200:
                raise "Connection Failed"
        except:
            print("Could not connect..!")
            # set failure flag
            return '-1'
        else:
            # return JSON data
            return payload.json()

    def solution(self):
        # if the GET request was unsuccessful, end the program
        if self.jsonData == '-1':
            return 0

        # prompt and get user input
        userInput = input("Welcome to the ticket viewer\n" \
                        "Type \'menu\' to view options or \'quit\' to exit\n")
        
        # validate user input?
        while userInput != "menu" and userInput != "quit":
            userInput = input("Invalid entry\n" \
                            "Type \'menu\' to view options or \'quit\' to exit\n")

        if userInput == "menu":
            self.menu(userInput)

        print("Thanks for using the viewer. Goodbye.")
        return 0

    def menu(self, userInput) -> None:
        while userInput != 'quit':
            userInput = input("\n\tSelect view options:\n" \
                            "\t* Press 1 to view all tickets\n" \
                            "\t* Press 2 to view a ticket\n" \
                            "\t* Type \'quit\' to exit\n")

            # view all tickets
            if userInput == '1':
                self.allTickets()
            elif userInput == '2':
                self.singleTicket()
            elif userInput != 'quit':
                print("Invalid entry")

    def allTickets(self):
        # max tickets per page
        max = 25

        # total tickets
        total = len(self.jsonData['tickets'])

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
                count = self.displayTickets(start, max if remaining > max else remaining)

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
            self.displayTickets(start, remaining)

    def singleTicket(self):
        # total tickets
        total = len(self.jsonData['tickets'])

        ticketNumber = int(input("Enter a ticket number:\n"))

        # WARNING: might need to verify that user input is a number before converting to int,
        # otherwise this may cause the program to crash

        # validate ticket number
        while ticketNumber >= total or ticketNumber < 0:
            ticketNumber = int(input("Invalid ticket number\nEnter a ticket number:\n"))

        print(self.ticketFormat(ticketNumber))

    def displayTickets(self, start, num):
        # to return the number of tickets displayed in this function call
        count = 0

        # for each ticket in the specifed number of tickets to display
        for i in range(start, start+num):
            print(self.ticketFormat(i))

            # keep count
            count += 1

        return count

    def ticketFormat(self, ticketNumber):
        return ("Ticket with subject \'" + \
                self.jsonData['tickets'][ticketNumber]['subject'] + \
                "\' opened by " + \
                str(self.jsonData['tickets'][ticketNumber]['requester_id']) + \
                " on " + \
                self.jsonData['tickets'][ticketNumber]['created_at'])