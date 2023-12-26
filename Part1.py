"""
PCL 1 Fall Semester 2023 - Course Project
Part 0: Book Selection
Students: <person 1>, <person 2>
"""
# --- Imports ---
import os
import json


# Function to process the text and perform NER
def perform_ner(text: str, nlp) -> list[any]:
    """
    Perform Named Entity Recognition (NER) on the input text using the provided spaCy NLP model.

    Args:
        text (str): The input text to analyze.
        nlp: A spaCy NLP model with NER capabilities.

    Returns:
        list: A list of named entities detected in the input text.
    """
    doc = nlp(text)
    return list(doc.ents)


# Function to extract and structure entity information
def extract_entity_info(tokens, filename: str, character_dict_list: list):
    """
    Extract information about PERSON entities from the given tokens.

    Args:
        tokens (iterable): A list of spaCy tokens.
        filename (str): The name of the source file (without the ".txt" extension).
        character_dict_list (list): A list of dictionaries containing character information.

    Modifies:
        Updates character_dicts with occurrences of the detected PERSON entities in place.
    """
    # iterate through all the tokens
    for token in tokens:
        # we are only interested in those that have the label 'PERSON'
        if token.label_ == "PERSON":
            # check if the token that was found was one of the main characters by comparing against the main
            # character list
            for name in character_dict_list:
                # the value for the key 'superstring' is part of the clustering. Whenever a token is a substring of
                # the identifying superstring, it is handled as a mention of that character
                if token.text.lower() in name["superstring"]:
                    if name["superstring"] == "jane_bennet" and token.text == "Bennet":  # to catch when 'Bennet'
                        # does not refer to Jane ('Bennet' can refer to 3 different people, on one will be considered here
                        pass
                    else:
                        # add all the context information for the identified token to the character's dictionary
                        context_dict = {
                            "sentence": token.sent.text,
                            "chapter": filename.strip(".txt"),
                            "position": {"start": token.start, "end": token.end}
                        }

                        name["occurrences"].append(context_dict)


# Function to save data to JSON file
def save_to_json(character_dicts):
    """
    Save the provided character information dictionaries to a JSON file.

    Args:
        character_dicts (list): A list of dictionaries containing character information.

    Writes:
        Saves the character information to a JSON file named "pride_and_prejudice_MainCharacters_NER.json"
        with proper formatting and encoding.
    """
    # create the file and store the dictionaries as a json
    with open(".\\pride_and_prejudice\\pride_and_prejudice_MainCharacters_NER.json", "w", encoding="UTF8") as jsonfile:
        json.dump(character_dicts, jsonfile, indent=3)


# Main Function
def main():
    import spacy
    nlp = spacy.load("en_core_web_sm")

# define the basic structure of the dictionaries used to gather info about the main characters
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

    # put the boiler plate dictionaries in a list, to have them handy and be able to access them
    character_dicts_list = [elizabeth_lizzy, jane_bennet, mr_collins, mr_darcy, mr_bingley, lydia,
                       lady_catherine_de_bourgh]

    # iterate through every chapter of the book to make the analysis
    for filename in os.listdir(path):
        # 'chapter 0' is not part of the book, but the preface. We are not interested in the sentiments there
        if str(filename) == "0.txt": continue

        #open the file and perform the sentiment analysis on that chapter
        with open(f".\\pride_and_prejudice\\chapters\\{filename}", "r", encoding="UTF8") as file:

            # do the analysis with spacy
            tokens = perform_ner(file.read(), nlp)

            # extract the information from the analysed token
            extract_entity_info(tokens, filename, character_dicts_list)

    # save the result as a json
    save_to_json(character_dicts_list)


# Run the main function
if __name__ == "__main__":
    main()
