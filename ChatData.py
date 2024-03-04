from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer, DataCollatorForLanguageModeling

tokenizer = GPT2Tokenizer.from_pretrained("wrench_tokenizer")

tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})

model = GPT2LMHeadModel.from_pretrained("GPyT")

NEWLINECHAR = "<N>"

def encode_newlines(inp):
    return inp.replace("\n", NEWLINECHAR)

def decode_newlines(inp):
    return inp.replace(NEWLINECHAR, "\n")

inp = "hello"

input_ids = tokenizer.encode(inp, return_tensors="pt")
model_out = model.generate(
    input_ids,
    max_length = 100,
    temperature = 0.7,
    no_repeat_ngram_size = 5,
    num_return_sequences = 3,
    num_beams = 5,
    return_dict_in_generate = True,
    output_scores = True
)

for seq in model_out["sequences"]:
    print("sql:", decode_newlines(tokenizer.decode(seq)))