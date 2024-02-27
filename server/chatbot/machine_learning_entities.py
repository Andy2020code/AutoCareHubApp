import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import json

# Download the model
#spacy.cli.download("en_core_web_lg")



def machine_learning_entities(request, keywords):
    #load the model
    nlp = spacy.blank('en')    
    # Access the loaded model and pass the keywords to it
    doc = nlp(keywords)

    for ent in doc.ents:
        #print the entity and label
        entity = ent.text
        label = ent.label_
        #print them in the console
        print("entity:", entity,"=>", label)
    else:
        print("No entities found")



