from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from transformers import GPT2Tokenizer, GPT2LMHeadModel, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
import os
import json

# Load pre-trained GPT-2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2", pad_token="50256")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Set end-of-sequence token as the padding token
tokenizer.pad_token = tokenizer.eos_token

file_path = os.path.relpath('server/chatbot/intents.json', os.path.dirname(__file__))
file_path_01 = os.path.relpath('server/chatbot/input_output_pairs.json', os.path.dirname(__file__))

if os.path.exists(file_path):
    print('File found')
    with open(file_path) as file:
        data_file = json.loads(file.read())
        print('data_file:', data_file)
else:
    print('File not found')
    data_file = {}



if os.path.exists(file_path_01):
    print('File 2 found')
    with open(file_path, "w") as file_02:
        for entry in file_02:
            file_02.write(f"input: {file_02['input_text']} output: {file_02['target_text']}\n")
            print('file_02:', file_02)
else:
    print('File not found')
    file_02 = {}

# Extract input-output pairs from the dataset
input_texts = [example["input_text"] for example in data_file]
target_texts = [example["target_text"] for example in data_file]

# Tokenize the target texts
tokenized_targets = tokenizer(target_texts, padding=True, truncation=True, return_tensors="pt")

# Define the block size (maximum length of input sequences)
block_size = 128  # Adjust this according to your model's maximum input length

# Create TextDataset and DataCollator
train_dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=file_path,
    block_size=block_size,
)

# Use both input and target sequences during training
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False
)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./output",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=1000,
    save_total_limit=2,
)

# Create Trainer and start training
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

trainer.train()

# Define the home view
def home(request):
    return render(request, 'chat.html')

# Define the generate_response view
def generate_response(request, user_input):
    # Get the input text from the request
    input_text = user_input

    # Encode the input text with attention mask and padding
    tokenized_input = tokenizer.encode_plus(
        input_text,
        padding=True,
        truncation=True,
        return_attention_mask=True,
        return_tensors="pt"
    )

    # Get the input IDs and attention mask from the tokenized input
    input_ids = tokenized_input["input_ids"]
    attention_mask = tokenized_input["attention_mask"]

    # Generate a response
    output = model.generate(input_ids, attention_mask=attention_mask, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2)

    # Decode the response
    response_text = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Return the generated response as JSON
    return JsonResponse({"response": response_text})
