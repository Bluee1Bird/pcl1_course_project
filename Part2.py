"""
PCL 1 Fall Semester 2023 - Course Project
Part 0: Book Selection
Students: <person 1>, <person 2>
"""
# --- Imports ---
import os
import re
from statistics import mean
import json

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# --- You may add other imports here ---


# Feel free to add more functions as needed!


# Function to perform sentiment analysis
def analyze_sentiment(text, analyzer):
    # TODO: Apply the sentiment analysis tool to the text and return the results
    pass


# Function to save sentiment analysis results to a JSON file
def save_sentiment_results(results, filename):
    # TODO: Save the sentiment analysis results in a structured JSON format
    pass


def save_to_json(character_dicts):
    with open(".\\pride_and_prejudice\\pride_and_prejudice_sentiment.json", "w", encoding="UTF8") as jsonfile:
        json.dump(character_dicts, jsonfile, indent=3)


# Main function
def main():
    analyzer = SentimentIntensityAnalyzer()

    # Load the JSON file
    file_path = '.\\pride_and_prejudice\\pride_and_prejudice_MainCharacters_NER.json'

    with open(file_path, 'r') as file:
        character_dicts = json.load(file)

    # Iterate over each character and access the 'sentence' property
    for character in character_dicts:
        compound_entire_book = []
        compound_per_chapter = {}
        for occurrence in character['occurrences']:
            sentence = occurrence["sentence"]

            # add the sentiment score to the dictionary
            sentiments = analyzer.polarity_scores(sentence)
            occurrence["sentiment"] = sentiments

            compound = sentiments["compound"]
            compound_entire_book.append(compound)

            # add the value to the compound per chapter dict
            try:
                compound_per_chapter[occurrence["chapter"]].append(compound)
            except:
                compound_per_chapter[occurrence["chapter"]] = [compound]

        #average per chapter
        for chapter in compound_per_chapter:
            compound_per_chapter[chapter] = mean(compound_per_chapter[chapter])
        character["compound_average_per_chapter"] = dict(sorted(compound_per_chapter.items(), key=lambda item: int(item[0])))

        #average entire book
        compound_average_entire_book = mean(compound_entire_book)
        character["compound_average_entire_book"] = compound_average_entire_book



    save_to_json(character_dicts)

    # TODO: Load or define the text for analysis
    text = "Your text for sentiment analysis."

    # TODO: Perform sentiment analysis on the text using your chosen tool
    # For example, analyze each sentence or paragraph where entities are identified

    # Save the results to a JSON file
    # Example filename: 'BookTitle_Sentiment.json'


# Run the main function
if __name__ == "__main__":
    main()
