import sys
import tkinter as tk
import os
import datetime
import re

def update_after_gui(file):
    global gui_added_events
    global gui_deleted_events
    if gui_added_events != []:
        for event in gui_added_events:
            file.write(event)
        return 0
    if gui_deleted_events != []:
        # Remove duplicates (would exist if user entered the same event twice.)
        gui_deleted_events = list(set(gui_deleted_events))
        ## TODO
        file.seek(0)
        events = []
        for line in file:
            events.append(line[:-1])
        # Remove events user requested to delete
        for event in gui_deleted_events:
            events.remove(event)
        # Rewrite the file
        file.truncate(0)
        for event in events:
            file.write('{}\n'.format(event))
        return 0

def get_argument():
    # Get the argument passed in the command line. Exit if there is more than 1 argument.
    if len(sys.argv) == 1:
        # no argument
        return None
    elif len(sys.argv) == 2:
        return sys.argv[1]
    else:
        sys.exit('Too many arguments! There should be 0 or 1 arguments (no argument or -g for GUI, -t for text mode)')

def get_mode(argument):
    # Open the text or GUI interface depending on user's argument (no argument/double clicking opens the GUI interface. Exit if incorrect argument.
    if argument == '-g' or argument == None:
        return 'gui'
    elif argument == '-t':
        return 'text'
    else:
        sys.exit('Incorrect arguments. Use -t for text mode and no arguments or -g for GUI mode')

def sort_file(file):
        # Get file content in a new_list. remove \n.
        file.seek(0)
        file_content = file.readlines()
        cleaned_list = []
        for line in file_content:
            cleaned_list.append(line[0:-1])
        # Split the new list into dates and event names.
        split_list = []
        for line in cleaned_list:
            split_list.append(line.split(': '))
        # Make a new list which includes the above list and also the date in YYYY/MM/DD to allow for easy sorting.
        new_list = []
        for line in split_list:
            year = (line[0][6:])
            month = (line[0][3:5])
            day = (line[0][0:2])
            date = year + '/' + month + '/' + day
            temp_list = line
            temp_list.append(date)
            new_list.append(temp_list)
        # Sort the new_list using the new date added.
        new_list.sort(key = lambda event: event[2])
        # Remove the dates added for use in sort in new_list
        for line in new_list:
            del line[-1]
        # Restore the original format of the lines ( date: event )
        final_list = []
        for line in new_list:
            new_line = line[0] + ': ' + line[1]
            final_list.append(new_line)
        # Clear the file and then wirte the dates and events with the program's format
        file.truncate(0)
        for line in final_list:
            file.write('{}\n'.format(line))
        return file

def textmode(file): 

    def get_exit():
        while True:
            confirmation= input("\nIf you would like to exit the program, please enter 'exit'. If you would like to continue, please type 'continue'.\n")
            if confirmation == 'exit':
                return True
            elif confirmation == 'continue':
                return False

    def add_get_event(date):
        while True:
            event = input("Please enter the event's name:\n")
            if event.strip() == '':
                print('Error. Event cannot be empty!\n')
            else:
                break
        while True:
            # Return true if a date was added, and false otherwise.
            confirmation = input("Please confirm the event details (y/n):\nDate:\t{}\nEvent:\t{}\n".format(date, event))
            if confirmation == 'y':
                print('Event added to file.')
                file.write('{}: {}\n'.format(date, event))
                return True
            elif confirmation == 'n':
                print('Event discarded.')
                return False
    
    def get_action():
        # This function returns a date if the user added a date. Otherwise, it exits the program.
        while True:
            # Prompt user to enter view1d, view7d, or view30d, view365d, viewall, or add
            # to view next 1 day, 7 days, 30 days, 365 days, all events or add a new event
            action = input('\nWelcome to Diarex! Please enter the required action:\n\nview1d\t: View the diary for tomorrow.\nview7d\t: View the diary for next 7 days.\nview30d\t: View the diary for next 30 days.\nview365d: View the diary for the next 365 days (year).\nviewall\t: View all events in your diary.\nadd\t: Add a new event to your diary.\ndelete\t: Delete an existing event.\nexit\t: Exit the program.\n\n')
            accepted_actions = ['view1d', 'view7d', 'view30d', 'view365d','viewall', 'add', 'exit', 'delete']
            while True:
                # Loop until user gives a correct action.
                if action not in accepted_actions:
                    action = input('Invalid action, please type in a valid action: view1d / view7d / view30d / view365d / viewall / add:\n')
                    continue
                else:
                    return action
    def do_action(action):
        if action == 'add':
            while True:
                # Loop until a correct date is given.
                date = input('\nPlease enter the date of the event in the format DD/MM/YYYY or DD-MM-YYYY:\n')
                # Check if the date has proper format and only has numbers (without checking the validity of the date itself)
                # if using 2 slashes, try and match using '/'
                try:
                    if date.count('/') == 2:
                        date = re.match(r'^[0-9]{2}/[0-9]{2}/[0-9]{4}$', date).group()
                        separator = '/'
                    # If using hyphens instead of the above.
                    elif date.count('-') == 2:
                        date = re.match(r'^[0-9]{2}-[0-9]{2}-[0-9]{4}$', date).group()
                        separator = '-'
                    else:
                        print('\nError. Are you sure you used two slashes (/) or two hyphens (-)?')
                        continue
                    # Date format is correct. Check if date is valid!
                    date_list = date.split(separator)
                    day = int(date_list[0])
                    month = int(date_list[1])
                    year = int(date_list[2])
                    try:
                        # The below will return ValueError if the date is not possible
                        datetime.date(year,month,day)
                        # Date exists.
                        # Convert the inputted string to datetime type, so it can be compared by today's date.
                        # If user's date is before today, confirm with user that this was done on purpose.
                        input_formatted_date = '{}-{}-{}'.format(date_list[2],date_list[1],date_list[0])
                        input_datetime_date = datetime.datetime.strptime(input_formatted_date, '%Y-%m-%d')
                        today_date = datetime.datetime.today()

                        if input_datetime_date < today_date:
                            while True:
                                response = input('The date that you entered is before today. Are you sure you want to add this to your diary? (y/n)\n')
                                if response == 'y':
                                    add_get_event(date)
                                    return 1
                                elif response == 'n':
                                    break
                                else:
                                    print('Please enter y to add the date and n to discard the date.\n')
                        else:
                            add_get_event(date)
                            return 1
                    except ValueError:
                        print('Error. The date you have entered does not exist, please enter a valid date.')
                        
                except AttributeError:
                    print('Error. Did you make sure to use / or - and the format DD/MM/YYYY or DD-MM-YYYY? (You cannot enter dates before year 1000!)')
        elif action == 'exit':
            sort_file(file)
            sys.exit('Exiting..')
        elif action == 'viewall':
            print()
            sort_file(file)
            file.seek(0)
            for line in file:
                print(line, end = '')
        elif action[0:4] == 'view':
            # Get number of days from the view action (action is not viewall).
            view_days = int(action[4:-1])
            # Add all events (with dates) in file to events list.
            events = []
            file.seek(0)
            for line in file:
                    events.append(line[:-1])
            today_date = datetime.date.today()
            # Get day, month, year from each event. Then, compare the string with today's date, and add to required_events then finally print that out after going through all events.
            required_events = []
            for event in events:
                event_day = int(event[0:2])
                event_month = int(event[3:5])
                event_year = int(event[6:10])
                current_event_date = datetime.date(event_year, event_month, event_day)
                difference = (current_event_date - datetime.date.today()).days
                if difference >= 0 and difference <= view_days:
                    required_events.append(event)
            # Print out the events requested by the user.
            print()
            for event in required_events:
                print(event)
         
        elif action == 'delete':
            print()
            events = []
            file.seek(0)
            for line in file:
                events.append(line[0:-1])
            while True:
                delete_date = input('Please enter the required delete date in the foram DD/MM/YYYY or DD-MM-YYYY:\n')
                # Convert - to / in delete_date to be able to search the file
                if '-' in delete_date:
                    delete_date = delete_date.replace('-','/')
                # Note: No error checking is made for user input since if user entered something incorrectly there will be no results anyway.
                # Get the events in the date give by user (if they exist).
                potenial_delete_list = []
                for event in events:
                    if delete_date == event[0:10]:
                        potenial_delete_list.append(event)
                if potenial_delete_list == []:
                    response = input("No events were found with this date. type 'continue' to search again or 'exit' to leave deleteing mode.\n")
                    if response == 'exit':
                        return 'exit'
                else:
                    # Events were found that need to be deleted.
                    for event in potenial_delete_list:
                        while True:
                            confirm_delete = input("Would you like to delete this event? {} (y/n)\n".format(event))
                            if confirm_delete == 'y':
                                events.remove(event)
                                break
                            elif confirm_delete == 'n':
                                break
                            else:
                                print('Error. Please enter a correct response.')

                # Clear the file and then write it again with the updated events.
                file.truncate(0)
                for event in events:
                    file.write('{}\n'.format(event))
                return 1
                
    while True:    
        action = get_action()
        do_action(action)
        # Only proceeds to get_exit() if action was not exit.
        confirm_exit = get_exit()
        if confirm_exit == True:
            # Sort file before exiting.
            sort_file(file)
            break

def guimode(file_content):

    def popup_window(previous_window, title, message):
        # Window setup and layout formation.
        popup_window = tk.Toplevel(previous_window)
        popup_window.grab_set()
        popup_window.title(title)
        popup_window_width = 300
        popup_window_height = 100
        popup_window.geometry('{}x{}'.format(popup_window_width, popup_window_height))
        popup_window.resizable(False, False)
        # Button and label creation.
        popup_label = tk.Label(popup_window, text=message)
        continue_button = tk.Button(popup_window, text='OK', command = popup_window.destroy)
        # Configure grid. Weight = 1 centers the buttons.
        popup_window.rowconfigure([0,1], minsize = 0, weight = 1)
        popup_window.columnconfigure([0,1,2], minsize = 0, weight = 1)
        # Grid everything.
        popup_label.grid(row = 0, column = 1, padx = 20)
        continue_button.grid(row = 1, column = 1, padx = 20)

    def add_window(main_window):
            
        def add_event_and_quit_window(entry_date,entry_event):
            # Give error if no entry_date was given
            entry_date = entry_date.get()
            entry_event = entry_event.get()
            if entry_date == '':
                popup_window(add_window, 'Error','You must enter a date of birth!')
            if entry_event == '':
                popup_window(add_window, 'Error','You must enter a name for the event!')
            # If this is sucessful date passes regex check.
            elif re.match(r'^[0-9]{2}/[0-9]{2}/[0-9]{4}$', entry_date):
                year = int(entry_date[6:])
                month = int(entry_date[3:5])
                day = int(entry_date[0:2])
                try:
                    datetime.date(year,month,day)
                    # If here, then the date is correct format wise and is a real date. There is also an event.
                    # IMPORTANT: extra space at the end on purpose because for some reason the last char doesn't get written to the file!
                    result = '{}: {} '.format(entry_date, entry_event)
                    gui_added_events.append(result)
                    popup_window(add_window, 'Confirmation','Event added. It will be visible once\nthe program is restarted.')
                except ValueError:
                    popup_window(add_window, 'Error','You must enter a real date!')
            else:
                popup_window(add_window, 'Error','You must enter a valid date of\n birth format! (DD/MM/YYYY)')
                
            
        add_window = tk.Toplevel(main_window)
        add_window.grab_set()
        add_window.title('Add an event')
        add_window.resizable(False, False)
        add_window_width = 300
        add_window_height = 200
        add_window.geometry('{}x{}'.format(add_window_width,add_window_height))
        add_window.columnconfigure([0,1], minsize = int(add_window_width/2))
        add_window.rowconfigure([0,1,2], minsize = int(add_window_height/3))
        
        # Set up labels, text fields, and buttons.
        dob_label = tk.Label(add_window, text='Date of event\n(DD/MM/YYYY)')
        event_name_label = tk.Label(add_window, text='Event name\n(Cannot be blank)')
        dob_text = tk.Entry(add_window, width = 10)
        event_text = tk.Entry(add_window, width = 10)
        # lambda added to avoid code execution before button is pressed.
        add_event_button = tk.Button(add_window, text='Add event to diary', command = lambda: add_event_and_quit_window(dob_text, event_text))
        add_event_button_exit = tk.Button(add_window, text='Go back', command = add_window.destroy)
        # Grid everything.
        dob_label.grid(row = 0, column = 0)
        event_name_label.grid(row = 1, column = 0)
        dob_text.grid(row = 0, column = 1, sticky = tk.E+tk.W, padx = (0,10))
        event_text.grid(row = 1, column = 1, sticky = tk.E+tk.W, padx = (0,10))
        add_event_button.grid(row = 2, column = 1)
        add_event_button_exit.grid(row = 2, column = 0, padx = (10,0))

 

    
    def delete_window(main_window, file_content):

        def search_and_delete_window(delete_window, file_content):

            # Get the events that match the date entered.
            # Make a state for delete_button to disable if there is no event found OR there is more than 1 event
            delete_button_state = True
            search_date = days_entry.get()
            matched_event = 'No event found'
            for event in file_content:
                if event[0:10] == search_date:
                    # Tell user if more than one event is found he/she will need to open the textmode to remove the event.
                    if matched_event != 'No event found':
                        # Extra space at the end to "hide" delete event button.
                        matched_event = 'More than one event found\n at this date. Please use text\nmode to remove this event.'
                        delete_button_state = False
                        break
                    matched_event = event
            if matched_event == 'No event found':
                delete_button_state = False
            if matched_event != 'No event found' and matched_event != 'More than one event found\n at this date. Please use text\nmode to remove this event.':
                popup_window(delete_window, 'Confirmation', 'Event ({}) deleted.\nThis will be reflected when you\nrestart the program.'.format(matched_event))
                gui_deleted_events.append(matched_event)
                return 0
                
            # Window setup and layout formation.
            search_and_delete_window = tk.Toplevel(delete_window)
            search_and_delete_window.title('Delete event')
            search_and_delete_window_width = 300
            search_and_delete_window_height = 100
            search_and_delete_window.geometry('{}x{}'.format(search_and_delete_window_width, search_and_delete_window_height))
            search_and_delete_window.resizable(False, False)
            # Button and label creation.
            text_label = tk.Label(search_and_delete_window, text ='Event found:')
            matched_event_label = tk.Label(search_and_delete_window, text=matched_event)
            delete_button = tk.Button(search_and_delete_window, text='Delete\nevent', command = lambda: delete_confirm_window(search_and_delete_window, file_content, event))
            goback_button = tk.Button(search_and_delete_window, text='Go back', command = search_and_delete_window.destroy)
            # Configure grid. Weight = 1 centers the buttons.
            search_and_delete_window.rowconfigure([0,1], minsize = 0)
            search_and_delete_window.columnconfigure([0,1,2], minsize = 0)
            # Grid everything.
            text_label.grid(row = 0, column = 0,pady = 10, padx = 3)
            goback_button.grid(row = 1, column = 0, pady = 10)
            matched_event_label.grid(row = 0, column = 1,padx = 15, columnspan = 2)
            if delete_button_state:
                delete_button.grid(row = 1, column = 2)
        
        delete_window = tk.Toplevel(main_window)
        delete_window.grab_set()
        delete_window.title('Deleting an event')
        delete_window_width = 300
        delete_window_height = 100
        delete_window.geometry('{}x{}'.format(delete_window_width,delete_window_height))
        delete_window.columnconfigure([0,1], minsize = int(delete_window_width/2))
        delete_window.rowconfigure([0,1], minsize = int(delete_window_height/2))

        # Setup the text fields, drop down menu, and buttons.
        info_text = tk.Label(delete_window, text ='Date of event you want\nto delete (DD/MM/YYYY)')
        days_entry = tk.Entry(delete_window, width = 10)
        exit_button = tk.Button(delete_window, text='Go back', command=delete_window.destroy)
        search_button = tk.Button(delete_window, text='Search', command=lambda: search_and_delete_window(delete_window, file_content))
        # Draw on grid.
        info_text.grid(row = 0, column = 0)
        days_entry.grid(row = 0, column = 1)
        exit_button.grid(row = 1, column = 0)
        search_button.grid(row = 1, column = 1)

    
    def view_window(main_window, file_content):

        def get_entry():
            requested_days = days_entry.get()
            # Check if user 'all'. Output everything if so then exit window.
            if requested_days == 'all':
                for event in file_content:
                    events_section.insert(tk.END, '{}\n'.format(event))
                return view_window.destroy()
            # Otherwise, check if the user entered a number less than 1,000,000.
            try:
                requested_days = int(requested_days)
                if requested_days >= 1000000:
                    popup_window(view_window, 'Error','You must enter a number < 1,000,000!')
                    return 0
                # If here, everything is good. Destroy the window to display the days.
                updated_events_list = []
                final_events_list = []
                today_date = datetime.date.today()
                for event in file_content:
                    day = int(event[0:2])
                    month = int(event[3:5])
                    year = int(event[6:10])
                    updated_events_list.append([event, day, month, year])
                for event in updated_events_list:
                    datetime_event_date = datetime.date(event[-1],event[-2],event[-3])
                    difference = datetime_event_date - today_date
                    if difference.days <= requested_days and difference.days >= 0:
                        final_events_list.append(event[0])
                for event in final_events_list:
                    events_section.insert(tk.END, '{}\n'.format(event))
                return view_window.destroy()
            except ValueError:
                popup_window(view_window, 'Error','You need to enter a number!')
                return 0
            # Check if user entered
            return view_window.destroy()

        # Setup the window.
        view_window = tk.Toplevel(main_window)
        view_window.grab_set()
        view_window.title('Viewing options')
        view_window_width = 300
        view_window_height = 100
        view_window.geometry('{}x{}'.format(view_window_width,view_window_height))
        view_window.columnconfigure([0,1], minsize = int(view_window_width/2))
        view_window.rowconfigure([0,1], minsize = int(view_window_height/2))

        # Setup the text fields, drop down menu, and buttons.
        info_text = tk.Label(view_window, text ='View events in the\nnext X days: ')
        days_entry = tk.Entry(view_window, width = 10)
        exit_button = tk.Button(view_window, text='Go back', command=view_window.destroy)
        accept_button = tk.Button(view_window, text='View', command=get_entry)
        # Draw on grid.
        info_text.grid(row = 0, column = 0)
        days_entry.grid(row = 0, column = 1)
        exit_button.grid(row = 1, column = 0)
        accept_button.grid(row = 1, column = 1)

        

    def gui_main(file_content):
        # Set up GUI
        if 'days_to_view' not in locals():
            days_to_view = 0
        main_window = tk.Tk()
        main_window.title('Diarex')
        # Get screen width and height and use it along with size of window (WidthxHeight: 700x400) to center the window when setting it later.
        screen_width = main_window.winfo_screenwidth()
        screen_height = main_window.winfo_screenheight()
        window_width = 400
        window_height = 400
        # Using int to remove decimals as they will not work when setting position.
        position_xaxis = int(screen_width/2 - window_width/2)
        position_yaxis = int(screen_height/2 - window_height/2)
        # Set size of window and location of window
        main_window.geometry('{}x{}+{}+{}'.format(window_width,window_height,position_xaxis,position_yaxis))

        # Set up the grid
        main_window.columnconfigure([0,1,2,3], minsize = int(window_width/4))
        main_window.rowconfigure([0,1,2,3,4,5], minsize = int(window_height/6))

        # Add events section and scrollbar - height and width are just for initilisation
        global events_section
        events_section = tk.Text(main_window, height = 5, width = 5)
        events_section_scrollbar = tk.Scrollbar(main_window, command = events_section.yview)
        # Add  action buttons
        add_button = tk.Button(main_window, text='Add event', command=lambda: add_window(main_window))
        delete_button = tk.Button(main_window, text='Delete event', command=lambda: delete_window(main_window, file_content))
        view_button = tk.Button(main_window, text='View events',command=lambda: view_window(main_window, file_content))
        exit_button = tk.Button(main_window, text='Exit', command=main_window.destroy)
        # Grid events section and scrollbar
        events_section.grid(row = 0, column = 0, rowspan = 4, columnspan = 3, sticky=tk.N+tk.E+tk.S+tk.W, padx=(10,0), pady=15)
        events_section_scrollbar.grid(row=0,column=3, rowspan = 4, sticky ='nsw', pady=15)
        events_section.configure(yscrollcommand=events_section_scrollbar.set)
        # Grid action buttons
        add_button.grid(row = 4, column = 0, sticky = tk.N+tk.E+tk.S+tk.W, padx = 10)
        delete_button.grid(row = 4, column = 1, sticky = tk.N+tk.E+tk.S+tk.W, padx = 10)
        view_button.grid(row = 4, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, padx = 10)
        exit_button.grid(row = 5, column = 2, sticky = tk.E+tk.W, padx = 30)
        main_window.mainloop()
        
    gui_main(file_content)
        

def main():
    argument = get_argument()
    mode = get_mode(argument)
    # Open the data file if it exists with ability to read and write.
    # If it does not exist, the below creates one automatically.
    file = open('ddata.txt','a+')

    # Use the program in text mode.
    if mode == 'text':
        textmode(file)
        
    elif mode == 'gui':
        # Cannot access the file inside Tkinter, so will pass the contents of the file.
        file_content = []
        file.seek(0)
        for line in file:
            file_content.append(line[:-1])
        global gui_added_events
        global gui_deleted_events
        gui_added_events = []
        gui_deleted_events = []
        guimode(file_content)
        update_after_gui(file)
        # REMOVE
    else:
        sys.exit('Error: Unexpected argument checking bypass, please contact me with the input you have written so I can investiage this.')

    sort_file(file)
    file.close()
    
if __name__ == '__main__':
    main()
