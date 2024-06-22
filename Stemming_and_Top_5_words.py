import os  
import re  
import string  
import nltk  
from nltk.corpus import stopwords  
from nltk.stem.snowball import SnowballStemmer  # SnowballStemmer for stemming
from collections import Counter  # Counter from the collections module for counting word frequencies
import pandas as pd  # Pandas for handling data in DataFrame format

nltk.download('stopwords')

# Initialize the Italian stemmer
stemmer = SnowballStemmer("italian")

# Function to clean text by removing non-alphanumeric characters
def clean_text(text):
    return re.sub(r'[^A-Za-z0-9\s]', '', text)  # Remove all characters that are not letters, numbers, or whitespace

# Function to preprocess words by removing stop words and performing stemming
def preprocess_words(words):
    stop_words = set(stopwords.words('italian'))  # Get the set of Italian stopwords
    cleaned_words = [stemmer.stem(word.lower()) for word in words 
                     if word.lower() not in stop_words]  # Stem each word and filter out stopwords
    return cleaned_words

# Function to process a single file
def process_file(file_path, output_folder):
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Clean the text
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    
    # Preprocess words
    stemmed_words = preprocess_words(words)
    
    # Save the stemmed text to a new file
    file_name = os.path.basename(file_path)  # Get the base name of the file
    new_file_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_stem.txt")  # Create the new file path
    with open(new_file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(' '.join(stemmed_words))  # Write the stemmed words to the new file
    
    return stemmed_words, file_name

# Function to find the top 5 words and their frequencies
def find_top_words(words):
    word_counts = Counter(words)  # Count the frequencies of each word
    total_words = sum(word_counts.values())  # Get the total number of words
    top_words = word_counts.most_common(5)  # Get the top 5 most common words
    top_words_percentage = [(word, count / total_words) for word, count in top_words]  # Calculate the percentage of each top word
    return top_words_percentage

# Directories
input_folder = '/home/yolan00/Desktop/output'  
output_folder = '/home/yolan00/Desktop/stemming'  
csv_output_file = '/home/yolan00/Desktop/stemming.csv' 

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each file in the input folder
all_top_words = []
for file_name in os.listdir(input_folder):
    if file_name.endswith('.txt'):  # Only process .txt files
        file_path = os.path.join(input_folder, file_name)
        stemmed_words, original_file_name = process_file(file_path, output_folder)
        top_words_percentage = find_top_words(stemmed_words)
        
        # Prepare a row for the CSV
        row = [original_file_name]
        for word, percentage in top_words_percentage:
            row.extend([word, percentage])
        
        # Append to the results list
        all_top_words.append(row)

# Define the column headers
headers = ['File']
for i in range(1, 6):
    headers.extend([f'Top_{i}_Word', f'Top_{i}_Percentage'])

# Create a DataFrame and save it to a CSV file
df = pd.DataFrame(all_top_words, columns=headers)
df.to_csv(csv_output_file, index=False)

print(f"CSV file saved in: {csv_output_file}")
