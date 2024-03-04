import os
import re
from PyPDF2 import PdfReader
import docx
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments


#function to read different file types
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

def read_word(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text

def read_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def read_documents_from_directory(directory):
    combined_text = ""
    for filename in os.listdir(directory, filename):
        file_path = os.path.join(directory, filename)
        if filename.endswith(".pdf"):
            combined_text += read_pdf(file_path)
        elif filename.endswith(".docx"):
            combined_text += read_word(file_path)
        elif filename.endswith(".txt"):
            combined_text += read_text(file_path)
    return combined_text

def train_chatbot(directory, model_output_path, train_fraction=0.8):
    #read documents from the directory
    combined_text = read_documents_from_directory(directory)
    combined_text = re.sub(r'\n+', '\n', combined_text).strip()#remove extra newlines characters

    #split the text into training validation sets
    split_index = int(train_fraction * len(combined_text))
    train_text = combined_text[:split_index]
    val_text = combined_text[split_index:]

    #save the training and validation text to files
    with open("train_text.txt", "w") as f:
        f.write(train_text)

    with open("val_text.txt", "w") as f:
        f.write(val_text)

    #set up the tokenizer and model
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2-large")
        model = GPT2LMHeadModel.from_pretrained("gpt2-large")

    #prepare the dataset
    train_dataset = TextDataset(tokenizer=tokenizer, file_path="train_text.txt", block_size=128)
    val_dataset = TextDataset(tokenizer=tokenizer, file_path="val_text.txt", block_size=128)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    #set up the training arguments
    training_args = TrainingArguments(
        output_dir=model_output_path,
        overwrite_output_dir=True,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=30,
        save_steps=10_000,
        save_total_limit=2,
        logging_dir='/logs',   
    )

    #train the model
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    trainer.train()
    trainer.save_model(model_output_path)

    #save the tokenizer
    tokenizer.save_pretrained(model_output_path)

def generate_reaponse(model, tokenizer, prompt, max_length=50):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    #create the attention mask and pad token id
    attention_mask = torch.ones_like(input_ids)
    pad_token_id = tokenizer.eos_token_id

    output = model.generate(
        input_ids,
        max_length=max_length,
        num_return_sequences=1,
        attention_mask=attention_mask,
        pad_token_id=pad_token_id,
    )

    return tokenizer.decode(output[0], skip_special_tokens=True)

def main():
    directory = "/ai_docs"
    model_output_path = "/fine_tuned_gpt2_qa"

    #train the chatbot
    train_chatbot(directory, model_output_path)

    #load the trained model and tokenizer
    model = GPT2LMHeadModel.from_pretrained(model_output_path)
    tokenizer = GPT2Tokenizer.from_pretrained(model_output_path)

    #test the chatbot
    prompt = "I love painting, i love to paint"
    response = generate_reaponse(model, tokenizer, prompt)
    print("generated response:", response)