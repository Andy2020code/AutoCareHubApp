from django.shortcuts import render
from django.http import JsonResponse
from nltk.corpus import wordnet as wn

from .dictionary import lookup_word_definition, radiator_issues

from .word_list import us_words


from .models import Word_Map_Model



def chat(request):
    return render(request, 'chatbot/index.html')


def get_user_data(request):
    if request.method == "POST":
        user_data = request.POST.get('user-input-box')
        print('sent to get_response:', user_data)
        return get_response(request, user_data)
    else:
        return JsonResponse({'error': 'This endpoint only accepts POST requests'})





def get_response(request, user_data):
    print('received_data:', user_data)
    return JsonResponse({'sentence': user_data})


####################################################################

def dictionary(request):
    # Get all words in the WordNet corpus
    words = set(wn.words())

    # Convert the set to a list for JSON serialization
    word_list = list(words)

    # put the words in alphabetical order
    word_list.sort()

    # Return the word list as a JSON response
    return JsonResponse({'words': word_list})

####################################################################

