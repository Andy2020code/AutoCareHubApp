import spacy
import json
import random
import os
from spacy.training import Example

# Load the English model
nlp = spacy.load("en_core_web_sm")

# Load the training data from a JSON file

json_path = os.path.join(os.path.dirname(__file__), "training_data.json")
with open(json_path, "r") as file:
    print("file found")
    training_data = json.load(file)

# Create spaCy Examples from the training data
examples = []
for example in training_data:
    doc = nlp.make_doc(" ".join(token["LOWER"] for token in example["pattern"]))
    cats = {example["label"]: 1.0}
    example = Example.from_dict(doc, {"cats": cats})
    examples.append(example)

# Define the text classification pipeline
textcat = nlp.add_pipe("textcat")

# Add labels to the text categorization component
for example in training_data:
    textcat.add_label(example["label"])

# Train the text classification model
optimizer = nlp.begin_training()
for epoch in range(10):  # Adjust the number of epochs as needed
    random.shuffle(examples)
    for batch in spacy.util.minibatch(examples, size=8):
        nlp.update(batch, drop=0.2, sgd=optimizer)

# Save the trained model to disk
trained_model_path = os.path.join(os.path.dirname(__file__), "wrench_base_model")
nlp.to_disk(trained_model_path)
