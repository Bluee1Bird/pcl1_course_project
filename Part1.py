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


# Function to process the text and perform NER
def perform_ner(text, nlp):
    doc=  nlp(text)
    return list(doc.ents)


# Function to extract and structure entity information
def extract_entity_info(tokens, filename, character_dicts):
    for token in tokens:
        if token.label_ == "PERSON":
            for name in character_dicts:
                if token.text.lower() in name["superstring"]:
                    if name["superstring"] == "jane_bennet" and token.text == "Bennet":  # to catch when 'Bennet' does not refer to Jane
                        pass
                    else:
                        context_dict = {
                            "sentence": token.sent.text,
                            "chapter": filename.strip(".txt"),
                            "position": {"start": token.start, "end": token.end}
                        }

                        name["occurrences"].append(context_dict)


# Function to save data to JSON file
def save_to_json(character_dicts):
    with open(".\\pride_and_prejudice\\pride_and_prejudice_MainCharacters_NER.json", "w", encoding="UTF8") as jsonfile:
        json.dump(character_dicts, jsonfile, indent=3)


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
        if str(filename) == "0.txt": continue
        print(filename)

        with open(f".\\pride_and_prejudice\\chapters\\{filename}", "r", encoding="UTF8") as file:
            tokens = perform_ner(file.read(), nlp)

            extract_entity_info(tokens, filename, character_dicts)

    save_to_json(character_dicts)



# Run the main function
if __name__ == "__main__":
    main()
