from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from django.shortcuts import render
from django.http import JsonResponse
import os


# Define the home view
def home(request):
    return render(request, 'chat.html')

########################################################
# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), "gpt2_qa_trained")
if model_path is not None:
    print("Model found")

model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Define the function to identify intent and return response
def get_response(request, user_input):
    # Tokenize input question and context
    inputs = tokenizer(user_input, return_tensors="pt", max_length=248, truncation=True)

    # Perform inference to generate the sequence
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_length=100,
            do_sample=True,
            top_k=35,
            top_p=5.95,
            temperature=0.1,
            num_beams=15,
            no_repeat_ngram_size=2,
            repetition_penalty=1.5,
            num_return_sequences=1
        )

    # Decode the generated sequence to get the answer string
    answer = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    print(answer)

    return JsonResponse({"response": answer})
