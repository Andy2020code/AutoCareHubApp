from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling, GPT2LMHeadModel, GPT2Config
from transformers import GPT2Tokenizer
from tokenizers import ByteLevelBPETokenizer
from torch.utils.data import Dataset, DataLoader
import torch
from tqdm import tqdm
from pathlib import Path
from datasets import load_dataset

from transformers import get_scheduler
from transformers import AdamW

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f'Using device: {device}')

train_data_path = "chat_data.txt"
output_file = "all_data.txt"
vocab_size = 515
max_length = 515
batch_size = 4
num_train_epochs = 5
learning_rate = 5e-5

TRAIN_BASE = False

if TRAIN_BASE:
    tokenizer = ByteLevelBPETokenizer()
    tokenizer.train(files=train_data_path, vocab_size=52_00, min_frequency=2, special_tokens=[
        "<s>",
        "<pad>",
        "</s>",
        "<unk>",
        "<mask>",
    ])

    tokenizer.save_model("wrench_tokenizer")

inp = "hello"

tokenizer = GPT2Tokenizer.from_pretrained("wrench_tokenizer")

tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})

#set padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id


model = GPT2LMHeadModel.from_pretrained("gpt2")

block_size=128

class database_01(Dataset):
    def __init__(self, train_data_path, tokenizer, block_size):
        self.tokenizer = tokenizer
        with open(train_data_path, "r", encoding="utf-8") as file:
            self.text = file.read().splitlines()

    def __len__(self):
        return len(self.text)

    def __getitem__(self, idx):
        # tokenize the sample text
        tokenized_sample = self.tokenizer(
            self.text[idx], 
            padding='max_length', 
            max_length=515, 
            truncation=True, 
            return_tensors="pt",
            pad_to_max_length=True
        )

        tokenized_sample["labels"] = tokenized_sample["input_ids"]

        return tokenized_sample

custom_dataset_01 = database_01(
    train_data_path, 
    tokenizer, 
    block_size
)

#create a data collator that will dynamically pad the inputs to the maximum length in batch
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Create a data loader with batch progress bar
train_dataloader  = DataLoader(
    custom_dataset_01,
    batch_size=batch_size,
    collate_fn=data_collator,
    shuffle=True
)




# Define training arguments
training_args = TrainingArguments(
    output_dir="GPyT",
    overwrite_output_dir=True,
    num_train_epochs=num_train_epochs,
    per_device_train_batch_size=batch_size,
    save_steps=10_000,
    evaluation_strategy="no",
    eval_steps=500,
    report_to="tensorboard",
    learning_rate=learning_rate,
    warmup_steps=1000,
    weight_decay=0.1,
    save_total_limit=2,
    prediction_loss_only=True,
    gradient_accumulation_steps=16,
    seed=42,
    remove_unused_columns=False
)

# Define the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=custom_dataset_01,
    eval_dataset=None
)

optimizer = AdamW(model.parameters(), lr=training_args.learning_rate)


for batch in tqdm(train_dataloader, desc="Batch Progress", leave=False):
    model.train()
    optimizer.zero_grad()
    batch = {key: value.to(device) for key, value in batch.items()}
    outputs = model(**batch)
    loss = outputs.loss
    loss.backward()
    optimizer.step()

trainer.save_model("GPyT")