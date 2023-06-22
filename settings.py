
'''Function to set the user input in the settings tab to variables for use when creating the wordclouds and collecting
data'''
def setSettings(cloud_mask, start_date, end_date, multiple_wclouds):
    # Import main to have access to the variables there to change them
    import main
    from tkinter import messagebox
    from datetime import datetime
    ''' Tkinter is used to collect the values of the input set by the user and to edit the GUI. Datetime is used to
    convert the date inputted within the start_date and end_date input fields on the settings page to a format
     that can be used for when creating the wordclouds '''
    main.chosen_mask = cloud_mask
    main.chosen_mwordclouds = multiple_wclouds


    # Collect the number of days between the start date and end dates selected
    date_difference = (end_date - start_date).days

    # If the user has selected a start and end date that have at least 3 days between them, then update the settings.
    if date_difference >= 3:
        main.chosen_start_date = start_date
        main.chosen_end_date = end_date
        messagebox.showinfo('Success!', 'Settings updated successfully')
    # Else, if the user selects a start and end date less than 3 days between them, output an error messagebox.
    else:
        messagebox.showerror('Error', 'End date must be at least 3 days ahead of the start date!')
