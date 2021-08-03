# This file only contains a driver main function that creates the
# required class object and then calls the function to start the program

import tickets as tk

def main():
    tickets = tk.TicketViewer()
    tickets.solution()

    return 0

if __name__ == '__main__': 
    main()