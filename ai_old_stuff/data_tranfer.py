# Import necessary libraries
import json
import torch
import torch.nn as nn
from torch.optim import AdamW
from transformers import GPT2Tokenizer, GPT2Config, GPT2LMHeadModel, TrainingArguments, Trainer, DataCollatorForLanguageModeling, get_scheduler
from torch.utils.data import Dataset, DataLoader
from collections import defaultdict
from tqdm import tqdm
from tokenizers import ByteLevelBPETokenizer
from datasets import load_dataset


# Path to your JSON file
json_file_path = "car_parts_dictionary.json"

text_file_path = "chat_data.txt"

# Check and select the device (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f'Using device: {device}')

IMPORT_TXT = False
if IMPORT_TXT:
    # Initialize an empty dictionary to store the content
    data_dict_02 = {}

    #set the maximum line length
    max_line_length = 128

    #initialize the list of lines
    lines = []

    #import txt file
    with open(text_file_path, "r") as file:
        print("File found")
        for line in file:
            #take out white space
            line = line.strip()

            #check if it exceeds the maximun length
            while len(line) > max_line_length:

                #split the line at themax length
                split_point = max_line_length

                while split_point > 0 and line[split_point - 1] != "":
                    split_point -= 1

                #if no space was found, split at the maximum length
                if split_point == 0:
                    split_point = max_line_length

                #add the first part of the line to the list
                lines.append(line[:split_point])

                #update the line to the second part
                line = line[split_point:].strip()
            
            #add the last part of the line to the list
            lines.append(line)

        

IMPORT_JSON = False
if IMPORT_JSON:
    # Initialize an empty dictionary to store the content
    all_text = []

    # Read data from the JSON file
    with open(json_file_path, "r") as file:
        print("File found")
        dictionary = json.load(file)
        

        # Extract the content from the JSON data
        for item in dictionary["dictionary"]:
            all_text.append(item["id"])
            all_text.append(item["component_name"])
            all_text.append(item["component_definition"])
            all_text.append(item["component_function"])
            all_text.append(item["component_location"])
        else:
            print("ID not found in the dictionary")


    all_text = [str(item) for item in all_text]
    
    combined_text = " ".join(all_text)
    

WRITE_FILE = False
if WRITE_FILE:
    #write the dictionary to a txt file
    with open("data_transfer_output.txt", "w") as file:
        if combined_text:
            file.write(combined_text + "\n")
            print("completed writing to file")

WRITE_FILE_TXT = False
if WRITE_FILE_TXT:
    with open("data_transfer_output_02.txt", "w") as file:
        for line in lines:
            file.write(f"{line}\n")
        print("Completed writing to file")


data = "data_transfer_output.txt"

TRAIN_BASE = True
if TRAIN_BASE:
    tokenizer = ByteLevelBPETokenizer()

    # Convert the data_dict to a list of strings

    tokenizer.train(files=data, vocab_size=5200, min_frequency=2, special_tokens=[
        "<s>",
        "<pad>",
        "</s>",
        "<unk>",
        "<mask>",
    ])

    tokenizer.save_model("wrench_tokenizer_02")


TRAIN_MODEL = True
if TRAIN_MODEL:
    # Initialize GPT2 tokenizer and add special tokens
    tokenizer = GPT2Tokenizer.from_pretrained("wrench_tokenizer_02")
    tokenizer.add_special_tokens({
        "eos_token": "</s>",
        "bos_token": "<s>",
        "unk_token": "<unk>",
        "pad_token": "<pad>",
        "mask_token": "<mask>",
    })


    class database_04(Dataset):
        def __init__(self, text_file, tokenizer, max_length):
            self.tokenizer = tokenizer
            self.training_txt = text_file
            self.max_length = max_length

        def __len__(self):
            return len(self.training_txt)
        
        def __getitem__(self, idx):
            text = self.training_txt[idx]
            tokenized_training_text = self.tokenizer(
                text,
                max_length=self.max_length,
                padding="max_length",
                pad_to_max_length=True,
                truncation=True,
                return_tensors="pt"
            )
            return tokenized_training_text
    
    config = GPT2Config(
        vocab_size=tokenizer.vocab_size,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )

    model = GPT2LMHeadModel(config)
    data = "data_transfer_output.txt"
    dataset_01 = load_dataset("text", data_files=data)

    def encode(lines):
        return tokenizer(lines["text"], add_special_tokens=True, truncation=True, padding='max_length', max_length=514, return_tensors="pt", pad_to_max_length=True)
    
    dataset_01.set_transform(encode)
    dataset_01 = dataset_01["train"]
    data_collator_01 = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.25)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="fine_tuned_gpt2",  # Output directory for model checkpoints and logs
        overwrite_output_dir=True,        # Overwrite the content of the output directory
        num_train_epochs=10,               # Number of training epochs
        per_device_train_batch_size=100,    # Batch size per GPU/CPU during training
        save_steps=100,                   # Save checkpoint every X updates steps
        save_total_limit=2,               # Limit the total amount of checkpoints to save
        logging_steps=100,                # Log training loss and learning rate every X updates steps
        learning_rate=5e-5,               # Learning rate
        warmup_steps=500,                 # Linear warmup over warmup_steps
        weight_decay=0.02,                # Weight decay
        gradient_accumulation_steps=1,
        prediction_loss_only=True,
        report_to="tensorboard",
        remove_unused_columns=False,
    )      

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset_01,
        data_collator=data_collator_01,
    )

    # Train the model
    trainer.train()

    # Save the trained model
    trainer.save_model(training_args.output_dir)


GENERIC_TRAINER = False
if GENERIC_TRAINER:
    tokenizer = GPT2Tokenizer.from_pretrained("wrench_tokenizer_02")
    tokenizer.add_special_tokens({
        "eos_token": "</s>",
        "bos_token": "<s>",
        "unk_token": "<unk>",
        "pad_token": "<pad>",
        "mask_token": "<mask>",
    })

    paths = ["chat_data.txt"]

    vocab_size = 5200

    config = GPT2Config(
        vocab_size = tokenizer.vocab_size,
        bos_token_id = tokenizer.bos_token_id,
        eos_token_id = tokenizer.eos_token_id,
    )

    model = GPT2LMHeadModel(config)

    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

    dataset = load_dataset("text", "train", "validation", data_files=paths)

    def encode(lines):
        return tokenizer(lines["text"], add_special_tokens=True, truncation=True, padding="max_length", max_length=128, return_tensors="pt")

    dataset.set_transform(encode)
    dataset = dataset["train"]

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.15)

    training_args = TrainingArguments(
        output_dir = "fine_tuned_gpt2",
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=60,
        save_steps=100,
        save_total_limit=2,
        prediction_loss_only=True,
        remove_unused_columns=False,
        weight_decay=0.01,
        evaluation_strategy="epoch",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        optimizers=(optimizer, None)
    )

    trainer.train()
    trainer.save_model("fine_tuned_gpt2")
