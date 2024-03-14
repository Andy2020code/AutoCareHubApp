from transformers import GPT2ForQuestionAnswering, GPT2Tokenizer
import torch

# Load the trained model and tokenizer
model_path = "fine_tuned_model"
model = GPT2ForQuestionAnswering.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Input question
question = "What type of car is the Tesla Model S?"

# Tokenize the input question
inputs = tokenizer(
    question,
    return_tensors="pt"
)
print("inputs:", inputs)

# Pass the input through the model
with torch.no_grad():
    outputs = model(**inputs)

# Extract the answer from the model's output logits
answer_start_index = torch.argmax(outputs.start_logits)
answer_end_index = torch.argmax(outputs.end_logits) + 1

# Decode the answer
answer = tokenizer.decode(inputs["input_ids"][0][answer_start_index:answer_end_index], skip_special_tokens=True)

print("Answer:", answer)
