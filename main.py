
# Here are the libraries imported:
import tkinter as tk
from tkinter import ttk
from PIL import Image
from tkcalendar import *
import numpy as np
from datetime import date, datetime

'''
Tkinter used for the creation of a GUI;
PIL used for the reading of images;
tkcalendar for the use of creating a calendar widget in the GUI
numpy for use with multi-dimensional arrays & matrices
datetime to create intervals to create wordclouds within, to ultimately create a wordcloud timeline.
'''

# Import the settings .py file
from settings import setSettings

# Import TkinterVideo to allow the mp4 generated of the wordclouds to be displayed in the GUI
from tkVideoPlayer import TkinterVideo

# For use with sncscrape (if it works)
import generateWordcloud

# For use with the static dataset (will be used if the scraper is broken)
import generateWordcloudStaticData

# Once the generate wordcloud button is clicked, this function will execute
# The input within the hashtag_entry field is passed into it, as well as the frame that contains the GUI elements
def on_generate_wordcloud_button_click(hashtag_entry, hashtag_frame):

    # Firstly, set each 'chosen' variable to the values held within the settings tab.
    chosen_mask = selected_option.get()
    chosen_start_date = start_date.get_date()
    chosen_end_date = end_date.get_date()
    chosen_mwordclouds = var

    # Try using the scraper, if it doesn't work, use the static dataset.
    try:
        generateWordcloud.generate_wordcloud(hashtag_entry, hashtag_frame, chosen_mask,
                                                                  chosen_start_date, chosen_end_date,
                                                                  chosen_mwordclouds)
    # If scraper hasn't worked, use static dataset.
    except Exception as e:
        '''
        Call the 'generate_Wordcloud_StaticData' function held within 'generateWordcloudStaticData.py'. Pass in the
        chosen fields from the settings tab, as well as the hashtag inputted, and the homepage frame, so that the
        generated wordclouds can be displayed on it.
        '''
        generateWordcloudStaticData.generate_Wordcloud_StaticData(hashtag_entry, hashtag_frame, chosen_mask,
                                                                  chosen_start_date, chosen_end_date,
                                                                  chosen_mwordclouds)

''' Once the update settings button is clicked, call the 'setSettings' function within the settings.py file. Pass in the
data that is held within the fields in the settings tab '''
def on_settings_button_click(cloud_mask, start_date, end_date, multiple_wclouds):
    setSettings(cloud_mask, start_date, end_date, multiple_wclouds)

'''Once a video is created, load the video (which will be named 'wordcloud_video.mp4', and display it within a
TkinterVideo element. Ensure this element is displayed within the homepage frame.'''
def play_video(hashtag_frame):
    video_player = TkinterVideo(hashtag_frame)
    video_player.load("wordcloud_video.mp4")
    video_player.pack()
    video_player.play()

# This code runs first only if the main.py is called directly
if __name__ == '__main__':

    # Sets each 'chosen' variable to a default value.
    chosen_mask = np.array(Image.open('masks/cloud.png'))
    chosen_start_date = (datetime.strptime('2020-7-12', '%Y-%m-%d').date())
    chosen_end_date = (datetime.strptime('2020-9-19', '%Y-%m-%d').date())
    chosen_mwordclouds = False

    # Used to determine whether the user wants to create a timeline of word clouds
    time_series_analysis = False

    # Create the main window
    root = tk.Tk()
    generateWordcloud.root = root
    root.title('Social Media Trend Analysis Tool')

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the coordinates to center the window
    x = int((screen_width - 600) / 2)
    y = int((screen_height - 600) / 2)

    # Set the window size and position
    root.geometry('600x600+{}+{}'.format(x, y))
    # Make the window unresizable
    root.resizable(False, False)

    # Create a Notebook widget
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    ### HOME TAB ###

    # 1ST TAB
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text='Home')

    # Add widgets to the first tab
    label1 = tk.Label(tab1, text='Home')
    label1.pack(padx=20, pady=20)

    # Create a frame for the hashtag input and generate button
    hashtag_frame = ttk.Frame(tab1, padding=20)
    hashtag_frame.pack()

    # Create a label and entry widget for the hashtag input
    hashtag_label = ttk.Label(hashtag_frame, text='Enter a hashtag:')
    hashtag_label.pack(side='top')
    hashtag_entry = ttk.Entry(hashtag_frame)
    hashtag_entry.pack(side='top')

    # Create a button to generate the word cloud
    generate_button = ttk.Button(hashtag_frame, text='Generate Word Cloud(s)', command=lambda: on_generate_wordcloud_button_click(hashtag_entry, hashtag_frame))
    generate_button.pack(side='top')

    ################

    ### SETTINGS TAB ###

    # 2ND TAB
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text='Settings')

    # Add widgets to the second tab
    label2 = tk.Label(tab2, text='Settings')
    label2.pack(padx=20, pady=20)

    # Create a frame for the settings page
    settings_frame = ttk.Frame(tab2, padding=20)
    settings_frame.pack()

    ## CHOOSE WORD CLOUD SHAPE ##

    # Create a list of options for the drop-down list
    options = ['cloud', 'diamond', 'square', 'triangle']

    # Create a variable to store the selected option
    selected_option = tk.StringVar(root)
    selected_option.set(options[0])  # Set the default selected option

    drop_down_label = tk.Label(settings_frame, text='Select word cloud shape:')
    drop_down_label.pack(side='top')

    # Create the drop-down list widget
    drop_down_list = tk.OptionMenu(settings_frame, selected_option, *options)
    drop_down_list.pack(side='top')

    #############################

    ## CHOOSE START AND END DATE ##

    date_label = tk.Label(settings_frame, text='Select a start and end date:')
    date_label.pack(side='top')

    # Create two DateEntry widgets for start and end date
    mindate = date(2020,7,12)
    maxdate1 = date(2020,9,16)
    maxdate2 = date(2020,9,19)

    ''' Ensure the start date of the date widget is equal to 12th July 2020, which is when the first tweets within the
    static dataset were collected. Also ensure that the max date that the start date can be is 3 days before the 19th
    September 2020 to ensure 3 wordclouds can be made on each of the 3 days before it. '''
    start_date = DateEntry(settings_frame, width=12, background='darkblue', foreground='white', borderwidth=2, mindate=mindate, maxdate=maxdate1)
    start_date.set_date(datetime(2020,7,12).date())
    start_date.pack(padx=10, pady=10)

    ''' Ensure the end date can be at the maximum of 19th September 2020 as this is when the last tweets were collected in
    the static dataset. '''
    end_date = DateEntry(settings_frame, width=12, background='darkblue', foreground='white', borderwidth=2, maxdate=maxdate2, mindate=start_date.get_date())
    end_date.pack(padx=10, pady=10)

    # Ensure that the minimum date that the end date can be is the date selected within start_date
    def update_end_date(*args):
        end_date.config(mindate=start_date.get_date())

    # Ensure that the update_end_date function is called when the start_date has been changed by the user.
    start_date.bind("<<DateEntrySelected>>", update_end_date)

    ###############################

    ## CREATE MULTIPLE WORD CLOUDS? ##

    var = tk.BooleanVar(value=False)

    # Create a checkbutton label
    checkbutton_label = tk.Label(settings_frame, text='Create multiple wordclouds?')
    checkbutton_label.pack(side='top')

    # Create a Checkbutton with the text "Check me"
    checkbutton = tk.Checkbutton(settings_frame, variable=var)

    # Pack the Checkbutton
    checkbutton.pack(side='top')

    ##################################

    # Allows the user to update their settings.
    update_settings_button = ttk.Button(settings_frame, text='Update Settings', command=lambda: on_settings_button_click(selected_option.get(), start_date.get_date(), end_date.get_date(), var.get()))
    update_settings_button.pack(side='top')


    # Call the mainloop, which will allow changes to be made to the Tkinter GUI.
    root.mainloop()