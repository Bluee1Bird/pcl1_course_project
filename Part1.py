"""
PCL 1 Fall Semester 2023 - Course Project
Part 0: Book Selection
Students: <person 1>, <person 2>
"""
# --- Imports ---
import os
import re
import json
import spacy

# import nltk
# --- You may add other imports here ---


# TODO: Load the spaCy model
# TODO: Load the book text

# Clustering Dictionaries
pride_and_prejudice_characters = {
    # "mary_bennet": ["Marry Bennet", "Mary"],
    "elizabeth_lizzy": ["Elizabeth Bennet", "Elizabeth", "Lizzy", "Miss Eliza"],
    "jane_bennet": ["Jane Bennet", "Jane"],
    "mr_collins": ["Mr Collins", "Collins"],
    "mr_darcy": ["Mr Darcy", "Darcy"],
    "mr_bingley": ["Mr Bingley", "Bingley"],
    "mr_wickham": ["Mr Wickham", "Wickham"],
    "lydia": ["Lydia", "Lydia Bennet"],
    # "catherine_bennet": ["Kitty", "Kitty Bennet", "Catherine Bennet"],
    "lady_catherine_de_bourgh": ["Lady Catherine de Bourgh", "Mrs de Bourgh", "Lady Catherine", "Catherine de Bourgh"]
}


# Feel free to add more functions as needed!


# Function to process the text and perform NER
def perform_ner(text, spacy_model):
    # TODO: Process the text using the provided model and return the entities
    # Example: return nlp_model(text).ents
    pass


# Function to extract and structure entity information
def extract_entity_info(entities):
    entity_data = []
    # TODO: Iterate over entities and extract necessary information
    # Append the extracted info to entity_data
    return entity_data


# Function to save data to JSON file
def save_to_json(data, filename):
    # TODO: Save the data to a JSON file
    pass


# Main Function
def main():
    import spacy
    nlp = spacy.load("en_core_web_sm")

    elizabeth_lizzy = {
        "superstring": "elizabeth_lizzy",
        "name": "Elizabeth Bennet",
        "aliases": ["Elizabeth Bennet", "Elizabeth", "Lizzy", "Miss ELiza"],
        "occurrences": []  # More occurrences for CharacterName
    }
    jane_bennet = {
        "superstring": "jane_bennet",
        "name": "Jane Bennet",
        "aliases": ["Jane Bennet", "Jane"],
        "occurrences": []  # More occurrences for CharacterName
    }

    mr_collins = {
        "superstring": "mr_collins",
        "name": "Mr Collins",
        "aliases": ["Mr Collins", "Collins"],
        "occurrences": []  # More occurrences for CharacterName
    }

    mr_darcy = {
        "superstring": "mr_darcy",
        "name": "Mr Fitzwilliam Darcy",
        "aliases": ["Mr Darcy", "Darcy"],
        "occurrences": []  # More occurrences for CharacterName
    }

    mr_bingley = {
        "superstring": "mr_bingley",
        "name": "Mr Bingley",
        "aliases": ["Mr Bingley", "Bingley"],
        "occurrences": []  # More occurrences for CharacterName
    }

    lydia = {
        "superstring": "lydia",
        "name": "Lydia Bennet",
        "aliases": ["Lydia", "Lydia Bennet"],
        "occurrences": []  # More occurrences for CharacterName
    }

    lady_catherine_de_bourgh = {
        "superstring": "lady_catherine_de_bourgh",
        "name": "Lady Catherine de Bourgh",
        "aliases": ["Lady Catherine de Bourgh", "Mrs de Bourgh", "Lady Catherine", "Catherine de Bourgh"],
        "occurrences": []  # More occurrences for CharacterName
    }

    path = ".\\pride_and_prejudice\\chapters\\"

    character_dicts = [elizabeth_lizzy, jane_bennet, mr_collins, mr_collins, mr_darcy, mr_bingley, lydia,
                       lady_catherine_de_bourgh]

    for filename in os.listdir(path):

        with open(f".\\pride_and_prejudice\\chapters\\{filename}", "r", encoding="UTF8") as file:
            doc = nlp(file.read())
            tokens = list(doc.ents)


            for token in tokens:
                if token.label_ == "PERSON":
                    for name in character_dicts:
                        # print(token.text , name)
                        if token.text.lower() in name["superstring"]:
                            if name == jane_bennet and token.text == "Bennet":  # to catch when 'Bennet' does not refer to Jane
                                pass
                            else:
                                context_dict = {
                                    "sentence": token.sent.text,
                                    "chapter": filename.strip(".txt"),
                                    "position": {"start": token.start, "end": token.end}
                                }

                                name["occurrences"].append(context_dict)

    with open(".\\pride_and_prejudice\\pride_and_prejudice_MainCharacters_NER", "a", encoding="UTF8") as jsonfile:
        for character_dict in character_dicts:
            jsonfile.write(json.dumps(character_dict, indent=3))



    # Perform NER on the text
    # entities = perform_ner(book_text)

    # Extract information from entities
    # entity_info = extract_entity_info(entities)

    # Save the results to a JSON file
    # save_to_json(entity_info, 'BookTitle_NER.json')


# Run the main function
if __name__ == "__main__":
    main()
