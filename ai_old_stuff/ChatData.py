from transformers import GPT2LMHeadModel, GPT2Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("wrench_tokenizer_02")

tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})

model = GPT2LMHeadModel.from_pretrained("fine_tuned_gpt2")

inp = "what is a odometer"

input_ids = tokenizer.encode(inp, return_tensors="pt")
ai_response = model.generate(
    input_ids,
    max_length=100,
    do_sample=True,
    num_beams=15,
    temperature=0.1,
    top_k=40,
    top_p=1.95,
    num_return_sequences=1,
    pad_token_id=tokenizer.eos_token_id,
    no_repeat_ngram_size=5,
    repetition_penalty=1.5,
)

print("ai_response:", ai_response)

# Decode the filtered list of token IDs
output_text = tokenizer.decode(ai_response[0], skip_special_tokens=True)


print("Response:", output_text)