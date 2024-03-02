import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import json

#Download the model
#spacy.cli.download("en_core_web_trf")



def machine_learning_entities(request, keywords):

    # Load the model
    nlp = spacy.load('en_core_web_trf')

    # Access the loaded model and pass the keywords to it
    doc = nlp(keywords)

    for ent in doc.ents:
        # Print the entity and label
        entity = ent.text
        label = ent.label_
        # Print them in the console
        print("entity:", entity, "=>", label)
    else:
        print("No entities found")



