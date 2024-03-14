from transformers import GPT2Tokenizer, GPT2ForQuestionAnswering, Trainer, TrainingArguments
import torch
import json
from torch.utils.data import Dataset, DataLoader

# Load pre-trained tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token  # Set EOS token as padding token
model = GPT2ForQuestionAnswering.from_pretrained("gpt2")

# Load training data from JSON file
with open("car_dataset.json", "r") as file:
    train_data = json.load(file)
        



class dataset_01(Dataset):
    def __init__(self, train_data, tokenizer, max_length):
        self.training_data = train_data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.training_data)

    def __getitem__(self, idx):
        context = self.training_data[idx]["context"]
        questions = self.training_data[idx]["questions"]

        encoded_data = []
        start_positions = []
        end_positions = []

        for question in questions:
            answer = question["answer"]
            answer_start = context.find(answer)
            answer_end = answer_start + len(answer)

            # Convert start and end positions to tensors
            start_position_tensor = torch.tensor([[answer_start] * self.max_length], dtype=torch.long)
            end_position_tensor = torch.tensor([[answer_end] * self.max_length], dtype=torch.long)




            # Append the tensors to start_positions and end_positions lists
            start_positions.append(start_position_tensor)
            end_positions.append(end_position_tensor)
            
            text = f"Question: {question['question']} Answer: {answer} start_logits: {answer_start} end_logits: {answer_end} Context: {context} Start Position: {answer_start} End Position: {answer_end}"
            
            # Tokenize the text
            inputs = self.tokenizer(
                text,
                max_length=self.max_length,
                padding='max_length',
                pad_to_max_length=True,
                return_tensors="pt"
            )

            # Append the encoded data
            encoded_data.append({
                "input_ids": inputs["input_ids"],
                "attention_mask": inputs["attention_mask"]
            })

        # Add start_positions and end_positions to each encoded data
        for data, start, end in zip(encoded_data, start_positions, end_positions):
            data["start_positions"] = start
            data["end_positions"] = end
        return data




batch_size = 15
max_length = 248
dataset_instance = dataset_01(train_data, tokenizer, max_length)
dataloader_instance = DataLoader(dataset_instance, batch_size=batch_size, shuffle=True)

#create a data collator
class DataCollator:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def __call__(self, batch):
        input_ids_list = []
        attention_mask_list = []
        start_positions_list = []
        end_positions_list = []

        for item in batch:
            input_ids_list.append(item["input_ids"])
            attention_mask_list.append(item["attention_mask"])
            start_positions_list.append(item["start_positions"])
            end_positions_list.append(item["end_positions"])

        return {
            "input_ids": torch.stack(input_ids_list),
            "attention_mask": torch.stack(attention_mask_list),
            "start_positions": torch.cat(start_positions_list, dim=0),
            "end_positions": torch.cat(end_positions_list, dim=0)
        }


    

# Fine-tune the model
training_args = TrainingArguments(
    output_dir="qanda",  # Specify the output directory where model checkpoints and logs will be saved
    per_device_train_batch_size=15,
    num_train_epochs=50,
    learning_rate=5e-5,
    report_to="tensorboard",
    logging_dir="logs",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset_instance,
    data_collator=DataCollator(tokenizer),
)

trainer.train()

# Save the fine-tuned model
model.save_pretrained("fine_tuned_model")
