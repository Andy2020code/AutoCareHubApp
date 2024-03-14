import json
import spacy
from django.shortcuts import render
from django.http import JsonResponse
import os


# Define the home view
def home(request):
    return render(request, 'chat.html')

########################################################
# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), "wrench_base_model")
nlp = spacy.load(model_path)

# Load the training data from a JSON file
json_path = os.path.join(os.path.dirname(__file__), "training_data.json")
with open(json_path, "r") as file:
    print("file found")
    training_data = json.load(file)

# Define the function to identify intent and return response
def get_response(request, user_input):
    # Process the input text
    doc = nlp(user_input)
    
    # Get the predicted intent label
    predicted_intent = max(doc.cats, key=doc.cats.get)
    
    # Retrieve the response associated with the predicted intent label
    response = "No response found"
    for example in training_data:
        if example["label"] == predicted_intent:
            response = example["response"]
            break
    
    return JsonResponse({"response": response})
