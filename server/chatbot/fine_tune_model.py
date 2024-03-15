from transformers import GPT2ForQuestionAnswering, GPT2Tokenizer, Trainer, TrainingArguments, AdamW, get_linear_schedule_with_warmup
from torch.utils.data import Dataset, DataLoader
import torch
import json
import os

model = GPT2ForQuestionAnswering.from_pretrained('gpt2-large')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2-large')
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
tokenizer.pad_token = '[PAD]'



json_path = os.path.join(os.path.dirname(__file__), "training_data.json")

with open( json_path, 'r') as file:
    training_data = json.load(file)

training_array = []

for item in training_data["dictionary_content"]:
    context = item["context"]
    question = item["question"]
    answer = item["answer"]
    answer_start = item["answer_start"]
    answer_end = item["answer_end"]

    training_array.append({
        "context": context,
        "question": question,
        "answer": {
            "text": answer,
            "start_position": answer_start,
            "end_position": answer_end
        }
    })

traning_encoded = []
for item in training_array:
    context_encoded = tokenizer.encode(item["context"], return_tensors="pt")
    question_encoded = tokenizer.encode(item["question"], return_tensors="pt")
    answer_text_encoded = tokenizer.encode(item["answer"]["text"], return_tensors="pt")
    
    # Convert start and end positions to single integers
    answer_start = item["answer"]["start_position"]
    answer_end = item["answer"]["end_position"]

    traning_encoded.append({
        "context": context_encoded,
        "question": question_encoded,
        "answer": {
            "text": answer_text_encoded,
            "start_position": answer_start,
            "end_position": answer_end
        }
    })




# Define your custom dataset class
class Q_A_DATASET(Dataset):
    def __init__(self, training_encoded):
        self.train_data = training_encoded

    def __len__(self):
        return len(self.train_data)

    def __getitem__(self, idx):
        sample = self.train_data[idx]

        # Extract tensors from the sample
        context = sample["context"]
        question = sample["question"]
        answer_text = sample["answer"]["text"]
        answer_start = sample["answer"]["start_position"]
        answer_end = sample["answer"]["end_position"]

        return {
            "context": context,
            "question": question,
            "answer_text": answer_text,
            "answer_start": answer_start,
            "answer_end": answer_end
        }

def collate_fn(data):
    # Encode context and question sequences
    encoded_inputs = tokenizer(
        [f"Question: {item['question']} Context: {item['context']}" for item in data],
        padding=True,
        truncation=True,
        return_tensors="pt",
        return_token_type_ids=False,
        return_attention_mask=True,
        return_overflowing_tokens=False,
        return_special_tokens_mask=False,
        pad_to_max_length=True,
        max_length=248,
    )

    # Convert strings to integers and then create tensors
    answer_start_tensor = torch.stack([torch.tensor(int(item['answer_start'])) for item in data])
    answer_end_tensor = torch.stack([torch.tensor(int(item['answer_end'])) for item in data])
    return {
        'input_ids': encoded_inputs['input_ids'],
        'attention_mask': encoded_inputs['attention_mask'],
        'answer_start': answer_start_tensor,
        'answer_end': answer_end_tensor,
    }

#create a dataset instance
dataset = Q_A_DATASET(traning_encoded)

#create a dataloader
data_loader_01 = DataLoader(dataset, batch_size=80, shuffle=True, collate_fn=collate_fn)



num_epochs = 20

# Set up optimizer and scheduler
optimizer = AdamW(model.parameters(), lr=3e-5)
total_steps = len(data_loader_01) * num_epochs
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)

# Define loss function
loss_fn = torch.nn.CrossEntropyLoss()

# Training loop
total_loss = 0.0  # Initialize total loss
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    
    for batch in data_loader_01:
        # Access tensors from the batch
        context_input_ids = batch['input_ids']
        answer_start_input_ids = batch['answer_start']
        answer_end_input_ids = batch['answer_end']
        attention_mask = batch['attention_mask']

        # Forward pass
        outputs = model(
            input_ids=context_input_ids,
            attention_mask=attention_mask,
            start_positions=answer_start_input_ids,
            end_positions=answer_end_input_ids,
        )


        loss = outputs.loss
        
        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scheduler.step()

        total_loss += loss.item()

    # Print average loss for this epoch
    average_loss = total_loss / len(data_loader_01)
    print(f"Epoch {epoch + 1}/{num_epochs}, Average Loss: {average_loss}")

# Save trained model
save_path = os.path.join(os.path.dirname(__file__), "gpt2_qa_trained")
model.save_pretrained("save_path")
