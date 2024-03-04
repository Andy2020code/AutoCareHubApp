import json
from transformers import GPT2Tokenizer, GPT2LMHeadModel, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from django.shortcuts import render
from django.http import JsonResponse



json_file = "intents.json"
# Step 1: Parse the JSON file
def parse_intents(json_file):
    if json_file is not None:
        print("File found")
        with open(json_file, 'r') as file:
            intents_data = json.load(file)
        intents = {}
        for intent in intents_data["intents"]:
            tag = intent["tag"]
            patterns = intent["patterns"]
            responses = intent["responses"]
            intents[tag] = {"patterns": patterns, "responses": responses}
        return intents
    else:
        print("error with json file")

# Step 2: Prepare the data
def prepare_data(intents_converted):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.add_special_tokens({'pad_token': '<|endoftext|>'})

    tokenized_intents = {}
    for tag, data in intents_converted.items():
        tokenized_patterns = tokenizer(data["patterns"], truncation=True, padding=True, return_tensors="pt")
        tokenized_responses = tokenizer(data["responses"], truncation=True, padding=True, return_tensors="pt")
        tokenized_intents[tag] = {"patterns": tokenized_patterns, "responses": tokenized_responses}
    return tokenized_intents

# Step 3: Fine-tune the GPT-2 model
def fine_tune_model(tokenized_intents, tokenizer, json_file):
    dataset = TextDataset(tokenized_intents, file_path=json_file, block_size=128)
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    training_args = TrainingArguments(
        per_device_train_batch_size=4,
        num_train_epochs=3,
        logging_dir='./logs',
    )
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )
    trainer.train()
    return model


# Step 4: Use the trained model
def generate_response(model, tokenizer, user_input):
    input_ids = tokenizer.encode(user_input, return_tensors="pt")
    output = model.generate(input_ids, max_length=50, num_return_sequences=1, temperature=0.7)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Use the trained model to generate response
def get_response(request, user_input):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.add_special_tokens({'pad_token': '<|endoftext|>'})
    intents_converted = parse_intents(json_file)
    tokenized_intents = prepare_data(intents_converted)  # Pass the global tokenizer
    model = fine_tune_model(tokenized_intents, tokenizer, 'intents.json')

    response = generate_response(model, tokenizer, user_input)
    decoded_response = tokenizer.decode(response, skip_special_tokens=True)
    return JsonResponse({'response': decoded_response})





# Define the home view
def home(request):
    return render(request, 'chat.html')