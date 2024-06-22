import os  
import string  
from nltk.corpus import stopwords 

import nltk
nltk.download('stopwords')

def compile_words_into_single_file(directory_path, output_file_path):
    words = []  # Initialize an empty list to store words
    stop_words = set(stopwords.words('italian'))  # Get the set of Italian stopwords
    translator = str.maketrans('', '', string.punctuation)  # Create a translation table to remove punctuation

    # Read all .txt files in the specified directory
    for filename in os.listdir(directory_path):  # Iterate through each file in the directory
        if filename.endswith(".txt"):  # Check if the file has a .txt extension
            file_path = os.path.join(directory_path, filename)  # Get the full path of the file
            with open(file_path, 'r', encoding='utf-8') as file:  # Open the file in read mode with UTF-8 encoding
                content = file.read()  # Read the entire content of the file
                # Remove punctuation, convert to lowercase, split into words, and filter out stopwords and empty strings
                words += [word.translate(translator).lower() for word in content.split() if word.translate(translator).lower() not in stop_words and word.translate(translator).lower()]

    # Remove duplicates while maintaining order
    unique_words = list(dict.fromkeys(words))  # Convert the list to a dictionary and back to a list to remove duplicates

    # Write the words to the output file, each on a new line
    with open(output_file_path, 'w', encoding='utf-8') as output_file:  # Open the output file in write mode with UTF-8 encoding
        for word in unique_words:  # Iterate through each unique word
            output_file.write(word + '\n')  # Write the word to the file followed by a newline character

# Specify the path of the directory containing the .txt files and the path of the output file
directory_path = "/home/yolan00/Desktop/testi"  # Replace with the path of the directory containing the .txt files
output_file_path = "/home/yolan00/Desktop/risultati/dictionary.txt"  # Replace with the path of the output file

compile_words_into_single_file(directory_path, output_file_path)  # Call the function with the specified paths

