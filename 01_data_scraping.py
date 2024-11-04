# %%

# Obtain audio data from youtube for further processing.

# %%

# Imports
import csv
import os
import re
import string

from pytubefix import YouTube
from pytubefix.cli import on_progress

# %%

# Define functions

def to_sentence_case(value: str) -> str:
    """Change camel case string to sentence case."""

    assert type(value) == str, 'value must be a string'
    
    # initialize a string to return
    out = ''

    # check if the string is empty
    if len(value) > 0:

        # split at the positions where lower is followed by upper case
        parts = re.sub(r'([a-z])([A-Z])', r'\1 \2', value).split()
    
        # join the parts with a space and convert to sentence case
        out = ' '.join(parts).lower()
        out = out[0].upper() + out[1:]

        # replace spaces with underscores
        out = out.replace(' ', '_')
    
    return out

def remove_special_chars(value: str) -> str:
    """Remove special characters from a string, keep only ASCII values."""

    assert type(value) == str, 'value must be a string'

    # replace underscores with spaces
    value = value.replace('_', ' ')

    # replace all double spaces with a single space
    while '  ' in value:
        value = value.replace('  ', ' ')

    # keep only non-punctuation values
    out = ''.join(x for x in value if x not in string.punctuation)

    return out

# %%

# Define paths
path_url_sources = 'data/urls/sources.csv'
path_audio_data = 'data/audio/'

# %%

# Initialize list to store the data
data = []

# Read in the url source file
with open(path_url_sources, mode='r') as url_file:
    # Initialize the reader
    csv_reader = csv.reader(url_file)

    # Read in all rows
    for row in csv_reader:
        data.append(row)

# For each record create artist folder if needed and download the file
for row in data:
    # Complete the artist directory path
    artist_path = os.path.join(path_audio_data, row[0])

    # Prepare file name
    file_name = remove_special_chars(row[1])
    file_name = to_sentence_case(file_name)

    # Create artist directory if needed
    if not os.path.exists(artist_path):
        os.makedirs(artist_path)

    # Connect to the song youtube url
    yt = YouTube(row[2], on_progress_callback = on_progress)

    # Get the audio from the file
    ys = yt.streams.get_audio_only()

    # Download the file as mp3
    ys.download(mp3=True, output_path=artist_path, filename=file_name)
