from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import openai
from django import views



def Homepage(request):
    return render(request, 'home.html')


def get_completion(prompt): 
    print(prompt) 
    query = openai.Completion.create( 
        model="gpt-3.5-turbo-0125", 
        prompt=prompt, 
        max_tokens=100, 
        n=1, 
        stop=None, 
        temperature=0.5, 
    ) 
  
    response = query.choices[0].text 
    print("Response:", response) 
    return response 
  
  
def query_view(request): 
    
    if request.method == 'POST': 
        prompt = request.POST.get('prompt') 
        response = get_completion(prompt) 
        return JsonResponse({'response': response}) 
    
    return render(request, 'chatbot.html') 