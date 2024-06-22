import os  
import string  
from transformers import pipeline  
import nltk  
from nltk.corpus import stopwords  

nltk.download('stopwords')

def load_words_from_file(file_path):
    # Open the file and read all lines
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.read().splitlines()  # Split the file content into lines
    return words

def preprocess_words(words):
    # Get the set of Italian stopwords
    stop_words = set(stopwords.words('italian'))
    # Create a translation table to remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    # Remove punctuation, convert to lowercase, filter out stopwords, and remove duplicates while maintaining order
    clean_words = [word.translate(translator).lower() for word in words if word.translate(translator).lower() not in stop_words and word.translate(translator).lower()]
    return list(dict.fromkeys(clean_words))  # Convert to a dictionary and back to a list to remove duplicates

def classify_words(words):
    # Initialize the zero-shot classification pipeline with roberta model
    classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")
    categories = ["Positivo", "Negativo", "Neutro"]  # Define the categories for classification
    threshold = 0.5  # Set the threshold for considering a category as valid
    classified_words = {word: ["", "", ""] for word in words}  # Initialize a dictionary to store classified words
    
    for word in words:
        # Classify each word with the specified categories and hypothesis template
        result = classifier(word, candidate_labels=categories, hypothesis_template="Questo concetto è {}.")
        
        # Find the category with the highest score
        max_score = max(result['scores'])
        max_label = result['labels'][result['scores'].index(max_score)]
        
        # If the highest score exceeds the threshold, assign that category
        if max_score > threshold:
            classified_words[word][categories.index(max_label)] = "X"
        else:
            # Otherwise, assign "Neutro"
            classified_words[word][categories.index("Neutro")] = "X"
    
    return classified_words, categories

def save_dictionary(file_path, classified_words, categories):
    # Open the output file in write mode
    with open(file_path, 'w', encoding='utf-8') as output_file:
        # Write the header
        output_file.write(f"DicTerm,{','.join(categories)}\n")
        # Write the words and their categories
        for word, cats in classified_words.items():
            output_file.write(f"{word},{','.join(cats)}\n")

# File paths
input_file_path = '/home/yolan00/Desktop/risultati/dictionary.dicx'  
output_file_path = '/home/yolan00/Desktop/risultati/dictionary_filled.dicx'  

# Load, preprocess, and classify the words
words = load_words_from_file(input_file_path)
clean_words = preprocess_words(words)
classified_words, categories = classify_words(clean_words)

# Save the filled dictionary
save_dictionary(output_file_path, classified_words, categories)

print(f"Dictionary saved in: {output_file_path}")

