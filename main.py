# This file only contains a driver main function that creates the
# required class object and then calls the function to start the program

import TicketViewer as tv

def main():
    tickets = tv.TicketViewer()
    return_value = tickets.solution()

    return return_value

if __name__ == '__main__': 
    main()