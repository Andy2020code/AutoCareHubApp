import random

# List of possible greetings
greetings = [
    "Hello!",
    "Hi there!",
    "Greetings!",
    "Hey!",
    "Welcome!",
]

# List of introduction phrases
introductions = [
    "I am a language model powered by GPT-2.",
    "My purpose is to assist you with generating text based on your prompts.",
    "I have been trained on a diverse range of internet text.",
    "I am capable of producing coherent and contextually relevant responses.",
    "I can help you with various tasks such as writing, generating ideas, answering questions, and much more.",
    "Just provide me with a prompt, and I'll do my best to provide you with a helpful response.",
    "Feel free to ask me anything or give me a task to complete.",
    "I'm here to assist you and make your interactions with text easier and more enjoyable.",
    "Thank you for using me, and I look forward to assisting you!",
    "Greetings! I am an AI language model.",
    "Hello there! I'm a language model designed to help you with text generation.",
    "Hey! I'm here to assist you with your writing needs.",
    "Salutations! I'm an AI programmed to generate text based on your prompts.",
    "Hi! I'm a language model trained on a vast amount of data.",
    "Howdy! I'm here to provide you with text generation services.",
    "Welcome! I'm an AI language model ready to assist you.",
    "Good day! I'm here to help you with your writing tasks.",
    "Greetings and salutations! I'm a language model ready to assist you.",
    "Hey there! I'm an AI language model at your service.",
    "Hello! I'm here to assist you with generating text.",
    "Hi there! I'm a language model ready to help you with your writing.",
    "Greetings! I'm an AI language model designed to assist you.",
    "Salutations! I'm here to provide you with text generation services.",
    "Hey! I'm an AI language model ready to assist you.",
    "Hello there! I'm a language model here to help with your writing needs.",
    "Howdy! I'm an AI language model ready to assist you with text generation.",
    "Welcome! I'm a language model designed to help you with your writing.",
    "Good day! I'm here to assist you with text generation.",
    "Greetings and salutations! I'm an AI language model at your service.",
    "Hey there! I'm a language model ready to assist you with your writing tasks.",
    "Hello! I'm an AI language model here to help you with text generation.",
    "Hi there! I'm a language model designed to assist you with your writing needs.",
    "Greetings! I'm an AI language model ready to help you with generating text.",
    "Salutations! I'm here to provide you with text generation services.",
    "Hey! I'm an AI language model ready to assist you with your writing.",
    "Hello there! I'm a language model designed to help you with text generation.",
    "Howdy! I'm here to assist you with your writing needs.",
    "Welcome! I'm an AI language model at your service.",
    "Good day! I'm a language model ready to help you with your writing tasks.",
    "Greetings and salutations! I'm here to assist you with generating text.",
    "Hey there! I'm a language model ready to help you with text generation.",
    "Hello! I'm an AI language model designed to assist you.",
    "Hi there! I'm here to provide you with text generation services.",
    "Greetings! I'm an AI language model ready to assist you.",
    "Salutations! I'm a language model ready to help you with your writing.",
    "Hey! I'm an AI language model designed to help you with text generation.",
    "Hello there! I'm here to assist you with your writing needs.",
    "Howdy! I'm an AI language model ready to help you with text generation.",
    "Welcome! I'm a language model designed to assist you with your writing.",
    "Good day! I'm here to assist you with generating text.",
    "Greetings and salutations! I'm a language model at your service.",
    "Hey there! I'm a language model ready to assist you with your writing tasks.",
    "Hello! I'm an AI language model here to help you with generating text.",
    "Hi there! I'm a language model designed to assist you with your writing needs.",
    "Greetings! I'm an AI language model ready to help you with text generation.",
    "Salutations! I'm here to provide you with text generation services.",
    "Hey! I'm an AI language model ready to assist you with your writing.",
    "Hello there! I'm a language model designed to help you with text generation.",
    "Howdy! I'm here to assist you with your writing needs.",
    "Welcome! I'm an AI language model at your service."
]

# Generate introduction data
num_samples = 500  # You can adjust the number of samples as needed
intro_data = []

for _ in range(num_samples):
    intro = random.choice(greetings) + " " + " ".join(random.sample(introductions, len(introductions)))
    intro_data.append(intro)

# Save the generated data to a file
output_file = "introduction_data.txt"
with open(output_file, "w") as file:
    file.write("\n".join(intro_data))

print("Introduction data generated and saved to:", output_file)
