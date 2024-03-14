from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

bag_of_words = []

# Add special tokens or update vocabulary as needed
tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>",
})

current_vocab = tokenizer.get_vocab()

with open("data_transfer_output.txt", "r") as file:
    for line in file:
        bag_of_words.append(line.strip())


print("current_vocab:", current_vocab)

# Save the tokenizer
tokenizer.save_pretrained("wrench_tokenizer_02")