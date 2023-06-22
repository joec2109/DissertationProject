
# Here are the libraries imported:
import snscrape.modules.twitter as sntwitter
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

'''
snscrape is imported to attempt to use a scraper tool to collect tweets from Twitter;
tkinter is used to add the generated wordclouds to the GUI;
collections is used to count the number of times each word appears in tweets (word frequency);
wordcloud is imported to generate the wordclouds, and to prevent stopwords from being within them;
PIL is used to read image files, and save them;
io is used to convert images into bytes;
emoji is used to prevent emojis from appearing in the wordcloud;
numpy is used to handle the arrays that store the bytes of images;
datetime is used to handle the time intervals that the data is collected within for each wordcloud;
cv2 is used to read the large static dataset CSV file;
moviepy is used to generate an mp4 video that includes each wordcloud generated, to show the change in trends over time;
tkVideoPlayer is used to then display the generated mp4 video to the user in a Tkinter GUI.
'''

# Number of tweets to collect from the data and sets the stopwords variable to the STOPWORDS from wordclouds library.
num_tweets = 1000
stopwords = set(STOPWORDS)

# For use with snscrape, a scraper tool that can gather data from social media sites
def generate_wordcloud(hashtag_entry, hashtag_frame, chosen_mask, chosen_start_date, chosen_end_date, chosen_mwordclouds):
    # collect the hashtag inputted by the user
    hashtag = hashtag_entry.get()
    # If there is a hashtag, attempt to grab data & generated wordclouds.
    if hashtag:

        # Check if a generating_label label already exists
        if hasattr(hashtag_frame, 'generating_label'):
            # Destroy the previous label widget
            hashtag_frame.generating_label.destroy()
        # Let the user know that the wordclouds are being generated.
        hashtag_frame.generating_label = ttk.Label(hashtag_frame, text='Generating wordcloud(s)...')
        hashtag_frame.generating_label.pack(side='top')

        # Update the widget layout (pushes the message that lets the user know wordclouds are being generated)
        hashtag_frame.update_idletasks()

        # Calculate the number of word clouds and time interval based on chosen_mwordclouds boolean value
        if chosen_mwordclouds.get():
            num_wordclouds = 7  # Set the desired number of word clouds
        else:
            num_wordclouds = 1  # Set the number of word clouds to 1

        # Calculate the intervals from within the data will be collected.
        time_delta = chosen_end_date - chosen_start_date
        time_interval = time_delta / num_wordclouds

        # For each number in num_wordclouds, generate a new wordcloud.
        for i in range(num_wordclouds):
            # For the current interval, set the start and end date to the beginning and end of it.
            interval_start_date = (chosen_start_date + i * time_interval).strftime('%Y-%m-%d')
            interval_end_date = (chosen_start_date + (i + 1) * time_interval).strftime('%Y-%m-%d')

            # Output the wordcloud being generated
            print("Generating wordcloud " + str(i+1) + "...")

            # Initialise the tweets variable to store them within
            tweets = []
            # Try to use snscrape to collect data. If it is having issues, use the static dataset instead.
            try:
                ''' Keep on collecting tweets based on the hashtag inputted, start and end date of the interval, until
                the number of tweets collected is greater than 1000. '''
                for j, tweet in enumerate(sntwitter.TwitterSearchScraper(
                        hashtag + ' lang:en since:' + interval_start_date + ' until:' + interval_end_date).get_items()):
                    if j > num_tweets:
                        break
                    # Append the tweets 'rawContent', which is the text of the tweets, to the 'tweets' variable.
                    tweets.append(tweet.rawContent)
                ''' If snscrape is having problems, output this and call 'raise' which will prevent the rest of the code from
                executing. '''
            except Exception as e:
                print("Snscrape is currently having issues... Using static dataset instead")
                raise

            # Once tweets are collected, loop through each one and extract the words from them
            ''' If any of the words is a stopword, or contains a hashtag, ampersand, https, emoji, or is less than 4
            characters, then do not add them to the words list. Otherwise, add them to the words list. '''
            words = []
            for tweet in tweets:
                for word in tweet.split():
                    if word.lower() not in stopwords and not word.startswith('&') and not word.startswith('https') and not word.startswith(
                            '#') and word.__len__() > 4 and not any(char in emoji.EMOJI_DATA for char in word):
                        words.append(word.lower())
            # Use the counter to count the number of times each word appears.
            word_count = Counter(words)

            '''
            Create a wordcloud using the wordcloud library, giving it a height and width of 400 pixels, a white
            background, the mask that was chosen in settings (this determines the shape of the wordcloud), and generate
            the wordcloud based on the frequencies of the words held in the word_count variable.
            '''
            wordcloud = WordCloud(width=400, height=400, background_color='white', mask=np.array(Image.open('masks/'+chosen_mask+'.png'))).generate_from_frequencies(word_count)

            # Save the wordcloud as a PNG file
            wordcloud_path = 'wordcloud_'+str(i+1)+'.png'  # Update the file name with a counter
            wordcloud.to_file(wordcloud_path)

            # Read the PNG file as bytes
            with open(wordcloud_path, 'rb') as f:
                wordcloud_bytes = f.read()

            # Remove the 'generating wordclouds...' message from the GUI
            hashtag_frame.generating_label.destroy()

            # Check if a wordcloud label already exists
            if hasattr(hashtag_frame, 'wordcloud_label'):
                # Destroy the previous label widget
                hashtag_frame.wordcloud_label.destroy()

            # Check if a video label already exists
            if hasattr(hashtag_frame, 'video_player'):
                # Destroy the previous label widget
                hashtag_frame.video_player.destroy()

            ''' use ImageTk along with BytesIO to store the array of bytes that represent the wordcloud image to store
            it within the wordcloud_photo variable '''
            wordcloud_photo = ImageTk.PhotoImage(Image.open(BytesIO(wordcloud_bytes)))
            # Add the wordcloud photo to the homepage GUI frame.
            hashtag_frame.wordcloud_label = tk.Label(hashtag_frame, image=wordcloud_photo)
            hashtag_frame.wordcloud_label.image = wordcloud_photo
            hashtag_frame.wordcloud_label.pack()

        # Create a video from the wordcloud images if the number of wordclouds generated is greater than 1
        if chosen_mwordclouds.get() and num_wordclouds > 1:

            # Check if a wordcloud label already exists
            if hasattr(hashtag_frame, 'wordcloud_label'):
                # Destroy the previous label widget
                hashtag_frame.wordcloud_label.destroy()

            print("Generating video of wordclouds changing...")
            video_path = 'wordcloud_video.mp4'  # Set the video file path


            # Create a list of image paths for the wordclouds
            image_paths = ['wordcloud_' + str(x + 1) + '.png' for x in range(num_wordclouds)]

            # Create a list of images from the image paths
            images = 36*[cv2.imread(image_path) for image_path in image_paths]

            print(len(images))

            # Create a video clip from the list of images
            clip = ImageSequenceClip(images, fps=1)

            # Save the video clip as a video file
            clip.write_videofile(video_path)

            # Check if a video label already exists
            if hasattr(hashtag_frame, 'video_player'):
                # Destroy the previous label widget
                hashtag_frame.video_player.destroy()

            # Insert the video created into the homepage of the Tkinter GUI.
            hashtag_frame.video_player = TkinterVideo(hashtag_frame, width=463, height=321)
            hashtag_frame.video_player.load("wordcloud_video.mp4")
            hashtag_frame.video_player.pack()
            hashtag_frame.video_player.play()

            # A function that replays the video once it ends.
            def loopVideo(event):
                hashtag_frame.video_player.play()

            # Bind the '<<Ended>>' event to the loopVideo function to ensure the video is on an infinite loop.
            hashtag_frame.video_player.bind('<<Ended>>', loopVideo)
            ''' Bind a lamba function so that once the video is loaded, it is kept to the original size of the wordcloud
            images (which will be the size of the mask used) '''
            hashtag_frame.video_player.bind("<<Loaded>>", lambda e: e.widget.config(width=463, height=321))

    # If no hashtag entered, display this error
    else:
        messagebox.showerror('Error', 'Please enter a hashtag')