from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling, GPT2LMHeadModel, GPT2Config
from transformers import GPT2Tokenizer
from tokenizers import ByteLevelBPETokenizer
from torch.utils.data import Dataset, DataLoader
import torch
from tqdm import tqdm
from torch.optim import AdamW

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f'Using device: {device}')

train_data_path = "chat_data.txt"
output_file = "all_data.txt"
vocab_size = 52_000

TRAIN_BASE = True

if TRAIN_BASE:
    tokenizer = ByteLevelBPETokenizer()

    tokenizer.train(files=train_data_path, vocab_size=52_00, min_frequency=2, special_tokens=[
        "<s>",
        "<pad>",
        "</s>",
        "<unk>",
        "<mask>",
        "<|ans|>",
    ])

    tokenizer.save_model("wrench_tokenizer")

inp = "hello"

tokenizer = GPT2Tokenizer.from_pretrained("wrench_tokenizer")

tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>",
})

#set padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id


model = GPT2LMHeadModel.from_pretrained("gpt2-medium")


class database_01(Dataset):
    def __init__(self, train_data_path, tokenizer):
        self.tokenizer = tokenizer
        total_length = 0
        non_empty_lines = []
        with open(train_data_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    non_empty_lines.append(line)
                    total_length += len(line)
        self.text = non_empty_lines
        average_length = total_length / len(self.text)
        print("Average line length:", average_length)

    def __len__(self):
        return len(self.text)

    def __getitem__(self, idx):
        # tokenize the sample text
        tokenized_sample = self.tokenizer(
            self.text[idx],
            max_length=128,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
            pad_to_max_length=True,
        )

        processed_data = tokenized_sample["input_ids"]

        return processed_data


custom_dataset_01 = database_01(
    train_data_path, 
    tokenizer
)

#create a data collator that will dynamically pad the inputs to the maximum length in batch
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

batch_size = 5
train_dataloader  = DataLoader(
    custom_dataset_01,
    batch_size=batch_size,
    collate_fn=data_collator,
)




# Define training arguments
training_args = TrainingArguments(
    output_dir="GPyT",
    overwrite_output_dir=True,
    num_train_epochs=5,
    per_device_train_batch_size=batch_size,
    save_steps=10,
    report_to="tensorboard",
    learning_rate=5e-5,
    warmup_steps=1000,
    weight_decay=0.1,
    save_total_limit=2,
    seed=42,
)

# Define the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=custom_dataset_01,
)

optimizer = AdamW(model.parameters(), lr=training_args.learning_rate)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=5, verbose=True)
progress_bar = tqdm(total=len(train_dataloader), desc="Batch Progress")

for batch in train_dataloader:
    model.train()
    optimizer.zero_grad()
    batch = {key: value.to(device) for key, value in batch.items()}
    outputs = model(**batch)
    loss = outputs.loss

    # Backpropagation
    loss.backward()

    # Gradient clipping
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

    optimizer.step()

    # Update learning rate scheduler
    scheduler.step(loss)

    #update the progress bar with the current training loss
    progress_bar.set_postfix({"Training Loss": f"{loss.item():.4f}"})
    progress_bar.update(1)



#close the progress bar
progress_bar.close()


trainer.save_model("GPyT")