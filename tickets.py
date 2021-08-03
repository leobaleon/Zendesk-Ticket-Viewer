from requests import get
import os
import math

class TicketViewer:
    # class member variables
    originalUrl = 'https://zccsonmac.zendesk.com/api/v2/tickets'
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

    # this function will attempt a GET request and return the payload as JSON data.
    # if the connection fails, this function will return -1 to set jsonData as a flag
    # that indicaties this failure
    def getJSON(self, url) -> str:
        try:
            # GET request with authorization info
            payload = get(url, auth=(self.username, self.password))

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

    # this function must be called after creating an object of this class. this function
    # will start the program by prompting the user to either view the menu or quit the program
    def solution(self) -> int:
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

    # the main menu of the program, simply displays options for the user and then
    # navigates the program to the coresponding function
    def menu(self, userInput) -> None:
        # keep displaying the menu until the user decides to quit
        while userInput != 'quit':
            userInput = input("\n\tSelect view options:\n" \
                            "\t* Press 1 to view all tickets\n" \
                            "\t* Press 2 to view a ticket\n" \
                            "\t* Type \'quit\' to exit\n")

            # different menu options or error
            if userInput == '1':
                self.allTickets()
            elif userInput == '2':
                self.singleTicket()
            elif userInput != 'quit':
                print("Invalid entry")

    # this function will display all of the tickets available to the user
    # 25 at a time. the user will be prompted to view the next page or stop early
    def allTickets(self) -> None:
        # add the required string to get the correct page
        pageURL = self.originalUrl + '.json?page[size]=25'

        # update the jsonData variable with the new page data
        self.jsonData = self.getJSON(pageURL)

        # current page
        page = 1

        # total pages
        total = len(self.jsonData) + 1

        # print every ticket on this page
        for i in range(len(self.jsonData['tickets'])):
            print(self.ticketFormat(i))

        # print the current page and total page count
        print("Page " + str(page) + " of " + str(total))

        # while there are more pages with tickets
        while self.jsonData['meta']['has_more']:
            # get the url of the next page
            pageURL = self.jsonData['links']['next']

            # update the jsonData variable with the new page data
            self.jsonData = self.getJSON(pageURL)

            # print every ticket on this page
            for i in range(len(self.jsonData['tickets'])):
                print(self.ticketFormat(i))

            # print the current page and total page count
            print("Page " + str(page) + " of " + str(total))

            # if there are more pages and we haven't reached the last page
            if self.jsonData['meta']['has_more'] and page != total:
                # check if the user wants to load the next page
                userInput = input("\nPress 1 to view the next page, anything else to return to the previous menu:\n")

            # end the loop if user is done or if we reached the last page
            if userInput != '1' or page == total:
                break
            # otherwise increment the page for next iteration
            else:
                page += 1

    # this function allows the user to pick a single ticket to view. this function will
    # attempt to find the correct ticket and display only that one.
    def singleTicket(self) -> None:        
        # prompt the user for a number
        ticketNumber = input("Enter a ticket number:\n")

        # ensure that the user enters a number
        while ticketNumber.isnumeric() == False:
            ticketNumber = input("That is not a number\nEnter a ticket number:\n")

        # use the user input to get the correct url for the GET request
        ticketURL = self.originalUrl + '/' + str(ticketNumber) + '.json'

        # update the JSON data with the correct ticket
        self.jsonData = self.getJSON(ticketURL)

        # if the correct ticket was returned by the API
        if self.jsonData != '-1':
            print(self.ticketFormat(-1))
        # if unsuccessful, print an error message
        else:
            print("Reason: ticket does not exist!")

    # this function handles the pagination of 25 tickets a time. it also keeps track
    # of how many tickets have been displayed in the case where there are less than
    # 25 tickets remaining. this helps allTickets() know when to stop making calls to
    # this function to display more tickets
    def displayTickets(self, start, num) -> int:
        # to return the number of tickets displayed in this function call
        count = 0

        # for each ticket in the specifed number of tickets to display
        for i in range(start, start+num):
            print(self.ticketFormat(i))

            # keep count
            count += 1

        return count

    # simple accessory function that combines the necessary information together for
    # printing each ticket
    def ticketFormat(self, ticketNumber):
        # for the single ticket requests
        if ticketNumber == -1:
            return ("Ticket with subject \'" + \
                self.jsonData['ticket']['subject'] + \
                "\' opened by " + \
                str(self.jsonData['ticket']['requester_id']) + \
                " on " + \
                self.jsonData['ticket']['created_at'])
        # for page of tickets requests
        else:
            return ("Ticket with subject \'" + \
                self.jsonData['tickets'][ticketNumber]['subject'] + \
                "\' opened by " + \
                str(self.jsonData['tickets'][ticketNumber]['requester_id']) + \
                " on " + \
                self.jsonData['tickets'][ticketNumber]['created_at'])