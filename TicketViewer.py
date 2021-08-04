from requests import get
import os

class TicketViewer:
    # class member variables
    original_url = 'https://zccsonmac.zendesk.com/api/v2/tickets'
    username = ''
    password = ''
    json_data = ''

    # constructor attempts to retrieve environment variables for username and 
    # password for GET request from Zendesk API, also makes the call to get_json()
    # to initialize json_data
    def __init__(self) -> None:
        try:
            # read username and password from environment variables
            self.username = os.environ['USERNAME']
            self.password = os.environ['PASSWORD']
        except KeyError:
            print("Could not retrieve appropriate values for username and password...\n" + \
                "Did you export the required environment variables correctly?")
        else:
            print("Environment variables loaded successfully!")

    # this function will attempt a GET request and return the payload as JSON data.
    # if the connection fails, this function will return -1 to set json_data as a flag
    # that indicaties this failure
    def get_json(self, url) -> str:
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
        if self.json_data == '-1':
            return -1

        # prompt and get user input
        user_input = input("Welcome to the ticket viewer\n" \
                        "Type \'menu\' to view options or \'quit\' to exit\n")
        
        # validate user input?
        while user_input != "menu" and user_input != "quit":
            user_input = input("Invalid entry\n" \
                            "Type \'menu\' to view options or \'quit\' to exit\n")

        if user_input == "menu":
            self.menu(user_input)

        print("Thanks for using the viewer. Goodbye.")
        return 0

    # the main menu of the program, simply displays options for the user and then
    # navigates the program to the coresponding function
    def menu(self, user_input) -> None:
        # keep displaying the menu until the user decides to quit
        while user_input != 'quit':
            user_input = input("\n\tSelect view options:\n" \
                            "\t* Press 1 to view all tickets\n" \
                            "\t* Press 2 to view a ticket\n" \
                            "\t* Type \'quit\' to exit\n")

            # different menu options or error
            if user_input == '1':
                self.all_tickets()
            elif user_input == '2':
                self.single_ticket()
            elif user_input != 'quit':
                print("Invalid entry")

    # this function will display all of the tickets available to the user
    # 25 at a time. the user will be prompted to view the next page or stop early
    def all_tickets(self) -> None:
        # add the required string to get the correct page
        page_url = f'{self.original_url}.json?page[size]=25'

        # update the json_data variable with the new page data
        self.json_data = self.get_json(page_url)

        # current page
        page = 1

        # total pages
        total = len(self.json_data) + 1

        # print every ticket on this page
        for i in range(len(self.json_data['tickets'])):
            print(self.ticket_format(i))

        # print the current page and total page count
        print(f'Page {str(page)} of {str(total)}')

        # while there are more pages with tickets
        while self.json_data['meta']['has_more']:
            # get the url of the next page
            page_url = self.json_data['links']['next']

            # update the json_data variable with the new page data
            self.json_data = self.get_json(page_url)

            # print every ticket on this page
            for i in range(len(self.json_data['tickets'])):
                print(self.ticket_format(i))

            # print the current page and total page count
            print(f'Page {str(page)} of {str(total)}')

            # if there are more pages and we haven't reached the last page
            if self.json_data['meta']['has_more'] and page != total:
                # check if the user wants to load the next page
                user_input = input("\nPress 1 to view the next page, anything else to return to the previous menu:\n")

            # end the loop if user is done or if we reached the last page
            if user_input != '1' or page == total:
                break
            # otherwise increment the page for next iteration
            else:
                page += 1

    # this function allows the user to pick a single ticket to view. this function will
    # attempt to find the correct ticket and display only that one.
    def single_ticket(self) -> None:        
        # prompt the user for a number
        ticket_number = input("Enter a ticket number:\n")

        # ensure that the user enters a number
        while ticket_number.isnumeric() == False:
            ticket_number = input("That is not a number\nEnter a ticket number:\n")

        # use the user input to get the correct url for the GET request
        ticket_url = f'{self.original_url}/{str(ticket_number)}.json'

        # update the JSON data with the correct ticket
        self.json_data = self.get_json(ticket_url)

        # if the correct ticket was returned by the API
        if self.json_data != '-1':
            print(self.ticket_format(-1))
        # if unsuccessful, print an error message
        else:
            print("Reason: ticket does not exist!")

    # simple accessory function that combines the necessary information together for
    # printing each ticket
    def ticket_format(self, ticket_number) -> None:
        # for the single ticket requests
        if ticket_number == -1:
            return ("Ticket with subject \'" + \
                self.json_data['ticket']['subject'] + \
                "\' opened by " + \
                str(self.json_data['ticket']['requester_id']) + \
                " on " + \
                self.json_data['ticket']['created_at'])
        # for page of tickets requests
        else:
            return ("Ticket with subject \'" + \
                self.json_data['tickets'][ticket_number]['subject'] + \
                "\' opened by " + \
                str(self.json_data['tickets'][ticket_number]['requester_id']) + \
                " on " + \
                self.json_data['tickets'][ticket_number]['created_at'])