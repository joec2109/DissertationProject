
# Here are the libraries imported:
import tkinter as tk
from tkinter import messagebox, ttk
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
from PIL import Image, ImageTk
from io import BytesIO
import emoji
import numpy as np
import cv2
from moviepy.editor import ImageSequenceClip
from tkVideoPlayer import TkinterVideo
import pandas as pd

import operator

'''
tkinter is used to add the generated wordclouds to the GUI;
collections is used to count the number of times each word appears in tweets (word frequency);
wordcloud is imported to generate the wordclouds, and to prevent stopwords from being within them;
PIL is used to read image files, and save them;
io is used to convert images into bytes;
emoji is used to prevent emojis from appearing in the wordcloud;
numpy is used to handle the arrays that store the bytes of images;
datetime is used to handle the time intervals that the data is collected within for each wordcloud;
moviepy is used to generate an mp4 video that includes each wordcloud generated, to show the change in trends over time;
tkVideoPlayer is used to then display the generated mp4 video to the user in a Tkinter GUI.
pandas is used for further data analysis & the reading of data on the static dataset alongside cv2.
'''
# set the stopwords variable to the STOPWORDS from wordclouds library.
stopwords = set(STOPWORDS)

# For use with a static dataset included in this project (football_tweets.csv)
def generate_Wordcloud_StaticData(hashtag_entry, hashtag_frame, chosen_mask, chosen_start_date, chosen_end_date, chosen_mwordclouds):
    # The static dataset revolves around football, so the hashtag inputted is set to 'team'.
    team = hashtag_entry.get().lower()
    # If a hashtag is inputted, continue, else, show an error.
    if team:

        # Check if a generating_label label already exists
        if hasattr(hashtag_frame, 'generating_label'):
            # Destroy the previous label widget
            hashtag_frame.generating_label.destroy()

        # Let the user know the wordclouds are being generated
        hashtag_frame.generating_label = ttk.Label(hashtag_frame, text='Generating wordcloud(s)...')
        hashtag_frame.generating_label.pack(side='top')

        # Update the widget layout
        hashtag_frame.update_idletasks()

        # Calculate the number of word clouds to produce based on chosen_mwordclouds boolean value
        if chosen_mwordclouds.get():
            num_wordclouds = 3  # Set the desired number of word clouds
        else:
            num_wordclouds = 1  # Set the number of word clouds to 1

        # Read the data from the csv file using pandas
        data = pd.read_csv('football_tweets.csv', dtype='str')

        # Create the intervals that the data will be collected within
        time_delta = chosen_end_date - chosen_start_date
        time_interval = time_delta / num_wordclouds

        # For each number in num_wordclouds, generate a wordcloud
        for i in range(num_wordclouds):
            # Select the current interval start & end date
            interval_start_date = (chosen_start_date + i * time_interval).strftime('%Y-%m-%d')
            interval_end_date = (chosen_start_date + (i + 1) * time_interval).strftime('%Y-%m-%d')

            # Output which wordcloud is currently being generated
            print("Generating wordcloud " + str(i + 1) + "...")

            # Extract the 'text' field of each tweet and the corresponding 'file_name' field
            tweet_texts = \
            data[(data['file_name'].str.lower() == team) & (data['created_at'].between(interval_start_date, interval_end_date))][
                'text']

            # Set words to an empty array
            words = []
            # For each tweet, split the words and add them to the words array.
            for tweet in tweet_texts:
                for word in tweet.split():
                    ''' If the word is not a stopword, does not contain an ampersand, https, hashtag, at symbol, an emoji 
                    and is not less than 4 characters, add it to the words array. '''
                    if word.lower() not in stopwords and not word.startswith('&') and not word.startswith(
                            'https') and not word.startswith(
                        '#') and not word.startswith('@') and word.__len__() > 4 and not any(
                        char in emoji.EMOJI_DATA for char in word):
                        words.append(word.lower())
            # Count the number of times each word appears in the words array
            word_count = Counter(words)


            ''' Generate the wordcloud, giving it an initial height and width of 400 pixels, a white background,
             the shape of the mask selected in settings, and create it based on the frequencies of words held within 
             the word_count variable '''
            wordcloud = WordCloud(width=400, height=400, background_color='white',
                                  mask=np.array(Image.open('masks/' + chosen_mask + '.png'))).generate_from_frequencies(
                word_count)

            # Save the wordcloud as a PNG file
            wordcloud_path = 'wordcloud_' + str(i + 1) + '.png'  # Update the file name with a counter
            wordcloud.to_file(wordcloud_path)

            # Read the PNG file as bytes
            with open(wordcloud_path, 'rb') as f:
                wordcloud_bytes = f.read()

            # Destroy the message telling the user that the wordclouds are being generated in the GUI
            hashtag_frame.generating_label.destroy()

            # Check if a wordcloud label already exists
            if hasattr(hashtag_frame, 'wordcloud_label'):
                # Destroy the previous label widget
                hashtag_frame.wordcloud_label.destroy()

            # Check if a video label already exists
            if hasattr(hashtag_frame, 'video_player'):
                # Destroy the previous label widget
                hashtag_frame.video_player.destroy()

            '''Store the wordcloud image within wordcloud_photo. This is done by storing it within an ImageTk element,
            which is collected by converting the bytes of the wordcloud image into the image. '''
            wordcloud_photo = ImageTk.PhotoImage(Image.open(BytesIO(wordcloud_bytes)))
            hashtag_frame.wordcloud_label = tk.Label(hashtag_frame, image=wordcloud_photo)
            hashtag_frame.wordcloud_label.image = wordcloud_photo
            hashtag_frame.wordcloud_label.pack()

            word_count_list = list(word_count.items())

            sorted_words = sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)
            print("Wordcloud "+str(i+1)+": ", sorted_words[:20])

        # Create a video from the wordcloud images
        if chosen_mwordclouds.get() and num_wordclouds > 1:

            # Check if a wordcloud label already exists
            if hasattr(hashtag_frame, 'wordcloud_label'):
                # Destroy the previous label widget
                hashtag_frame.wordcloud_label.destroy()

            # Let the user know the video is being generated
            print("Generating video of wordclouds changing...")

            video_path = 'wordcloud_video.mp4'  # Set the video file path

            # Create a list of image paths for the wordclouds
            image_paths = ['wordcloud_' + str(x + 1) + '.png' for x in range(num_wordclouds)]

            # Create a list of images from the image paths
            images = 36 * [cv2.imread(image_path) for image_path in image_paths]

            # Create a video clip from the list of images
            clip = ImageSequenceClip(images, fps=1)

            # Save the video clip as a video file
            clip.write_videofile(video_path)

            # Check if a video label already exists
            if hasattr(hashtag_frame, 'video_player'):
                # Destroy the previous label widget
                hashtag_frame.video_player.destroy()

            # Set the video_player within the homepage of the GUI to the mp4 created within a TkinterVideo widget.
            hashtag_frame.video_player = TkinterVideo(hashtag_frame, width=463, height=321)
            hashtag_frame.video_player.load("wordcloud_video.mp4")
            hashtag_frame.video_player.pack()
            hashtag_frame.video_player.play()

            # Function to play the video once it has ended
            def loopVideo(event):
                hashtag_frame.video_player.play()

            '''Bind the '<<Ended>>' event to the loopVideo function to ensure it repeats once it ends every time.
            Bind the '<<Loaded>>' event to a lambda function that ensures the video is set to the default size of the
            wordclouds, which is the size of the mask used when generating the wordclouds. '''
            hashtag_frame.video_player.bind('<<Ended>>', loopVideo)
            hashtag_frame.video_player.bind("<<Loaded>>", lambda e: e.widget.config(width=463, height=321))


    # if no hashtag is inputted, let the user know they must enter one to proceed
    else:
        messagebox.showerror('Error', 'Please enter a hashtag')