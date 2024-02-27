from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from spacy.training import Example

from .machine_learning_entities import machine_learning_entities

import spacy

import random
import json
import os

from spacy.util import minibatch
import json

# Import the intents.json file
file_path = os.path.relpath('server/chatbot/intents.json', os.path.dirname(__file__))

if os.path.exists(file_path):
    print('file found')
    with open(file_path) as file:
        data_file = json.loads(file.read())
else:
    print('file not found')
    data_file = {}

# Start with blank English model
nlp = spacy.blank('en')

# Add the textcat to the pipeline
nlp.add_pipe("textcat")

# Get the textcat component
textcat = nlp.get_pipe("textcat")

# Add labels to text classifier
for intent in data_file["intents"]:
    textcat.add_label(intent["tag"])

# Convert the data into SpaCy format
train_data = []
optimizer = nlp.begin_training()
losses = {}

for intent in data_file['intents']:
    for pattern in intent['patterns']:
        train_data.append(Example.from_dict(nlp.make_doc(pattern), {'cats': {intent['tag']: True}}))

# Train the model


for i in range(10):
    random.shuffle(train_data)
    losses = {}

    # Batch the examples and iterate over them
    for batch in minibatch(train_data, size=8):
        for example in batch:
            # Update the model
            nlp.update([example], sgd=optimizer, losses=losses)

    print(losses)

# Save the model
nlp.to_disk("model")

# Load the model
nlp = spacy.load("model")








def home(request):
    return render(request, 'chat.html')


# Function to predict the intent of a message
def predict_intent(request, keywords):

    text = keywords
    # Use the model to predict the intent
    doc = nlp(text)

    # Find the label with the highest score
    max_score = max(doc.cats.values())
    predicted_intent = [k for k, v in doc.cats.items() if v == max_score][0]

    #send data to the machine learning function for entit recognition
    machine_learning_entities(request, keywords)


    return predicted_intent


# Function to generate a response
def generate_response(intent):
    # Find the intent in the data
    for i in data_file["intents"]:
        if i['tag'] == intent:
            # Choose a random response
            response = random.choice(i["responses"])
            return response



# Function to handle a message
def handle_message(request, keywords):
    # Predict the intent of the message
    intent = predict_intent(request, keywords)

    # Generate a response
    response = generate_response(intent)

    # Return the response as JSON
    return JsonResponse({"response": response})




