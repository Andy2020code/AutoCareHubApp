from django.http import JsonResponse
from .word_list import us_words
from .word_list_definition import us_words_definition

def lookup_word_definition(corrected_keyword):   

    return JsonResponse({'response': corrected_keyword})


##############################CAR ISSUES DICTIONARY####################################

#Radiator issue, possible causes and solutions
def radiator_issues(user_request):
    # Tokenization
    tokens = user_request.split()

    # Keyword Detection
    keywords = us_words  # Keywords indicating the main topic or action
    
    # Context Analysis
    if any(keyword in tokens for keyword in keywords):
        # Analyze the context to determine the meaning
        if "radiator" in tokens and "is" in tokens and "not" in tokens and "working" in tokens:
            # If the sentence mentions the car not starting
            response = "It seems like there might be a problem with your car's radiator."
        elif "car" in tokens:
            # If the sentence mentions the car without indicating a problem
            response = "You mentioned your car. Is there something specific you want to know?"
        else:
            # If the sentence does not mention the car
            response = "It's not clear what you're referring to. Could you provide more details?"
    else:
        # If the sentence does not contain any relevant keywords
        response = "Your sentence doesn't seem to be related to a specific topic."

    return JsonResponse({'response': response})