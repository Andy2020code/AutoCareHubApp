from transformers import GPT2TokenizerFast

# Load the tokenizer
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

# Data
data = [
    {
        "context": "The Tesla Model S is an all-electric luxury sedan produced by Tesla, Inc. It features advanced autopilot capabilities and a large touchscreen display.",
        "questions": [
            {
                "question": "What company produces the Tesla Model S?",
                "answer": "Tesla, Inc."
            },
            {
                "question": "What type of car is the Tesla Model S?",
                "answer": "all-electric luxury sedan"
            },
            {
                "question": "What are some features of the Tesla Model S?",
                "answer": "advanced autopilot capabilities and a large touchscreen display"
            }
        ]
    }
]

# Tokenize the context
context_tokens = tokenizer(data[0]["context"], return_offsets_mapping=True, return_special_tokens_mask=True)

# Define a function to find the start and end positions of the answer in the context
def find_answer_positions(context_tokens, answer):
    answer_tokens = tokenizer(answer, return_special_tokens_mask=True)["input_ids"][1:-1]  # Remove special tokens
    for i in range(len(context_tokens) - len(answer_tokens) + 1):
        if context_tokens[i:i+len(answer_tokens)] == answer_tokens:
            return i, i + len(answer_tokens) - 1
    return None, None

# Iterate over each question-answer pair
for qa_pair in data[0]["questions"]:
    question = qa_pair["question"]
    answer = qa_pair["answer"]
    # Tokenize the question
    question_tokens = tokenizer(question)["input_ids"]
    # Find the start and end positions of the answer in the context
    start_pos, end_pos = find_answer_positions(context_tokens["input_ids"], answer)
    print("Question:", question)
    print("Answer:", answer)
    print("Start Position:", start_pos)
    print("End Position:", end_pos)
    print("Context Tokens:", context_tokens["input_ids"])
    print("Answer Tokens:", tokenizer(answer)["input_ids"])
    print()

