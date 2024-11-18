from django.shortcuts import render
from django.views import View
import openai
import requests
from django.conf import settings
from django.http import JsonResponse
import time
import gradio as gr

openai.api_key = settings.OPENAI_API_KEY

"""
def openai_create(prompt):
    response = openai.chat.completions.create(
        model="https://chatgpt.com/g/g-67333d3872e881909c14d9bb6c420b07-mprofi-asystent",
        messages=[
            {"role":"system", "content": ""},
            {"role":"user", "content":prompt}
        ],
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )
    return response.choices[0].message.content

def conversation_history(input, history):
    history = history or []
    s = list(sum(history,()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    return history, history

blocks = gr.Blocks()

with blocks:
    chatbot = gr.Chatbot()
    message = gr.TextArea()
    state = gr.State()
    submit = gr.Button("Click")
    submit.click(conversation_history, inputs=[message, state], outputs=[chatbot, state])

blocks.launch(debug=True)

"""

class HomeView(View):
    last_requested_time = 0
    request_interval = 1
    def get(self, request):
        first_message = "Cześć, jak mogę ci dzisiaj pomóc?"
        return render(request, 'index.html', {"response":first_message})
    def post(self, request):
        user_input = request.POST.get('user_input')
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {settings.OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role":"system", "content":"Ten GPT pełni rolę obsługi klienta dla strony mprofi.pl i jej podstron. Chatbot zachowuje przyjazny ton, jest cierpliwy, empatyczny i profesjonalny. Odpowiada na szczegółowe zapytania dotyczące usług i produktów, takich jak marketing internetowy, projektowanie stron, oraz inne usługi oferowane na stronie. Udziela krótkich, zwięzłych i rzeczowych odpowiedzi. Pomaga użytkownikom w poruszaniu się po stronie, informuje o ofertach, terminach i procedurach. Gdy pytanie dotyczy lokalizacji informacji na stronie, bot od razu wyświetla link do odpowiedniej podstrony, aby ułatwić użytkownikom dostęp. Może udzielać wskazówek dotyczących kontaktu z zespołem obsługi oraz wyjaśniać dostępne formy współpracy. Korzysta wyłącznie z informacji zawartych na stronie mprofi.pl i jej podstronach jako źródła odpowiedzi. Jeśli zapytanie użytkownika wykracza poza te informacje lub odpowiedź nie jest dostępna, chatbot informuje, że nie może odpowiedzieć na to pytanie i sugeruje kontakt z obsługą klienta. Nie korzysta z zewnętrznych narzędzi do przeszukiwania sieci. W razie pytania wykraczającego poza system mProfi niech udzieli odpowiedzi iż nie posiada takich informacji i nie może na nie odpowiedzi"},
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            response_text = response_data['choices'][0]['message']['content']
        else:
            response_text = f"Błąd {response.status_code}: {response.text}"
        return render(request, 'index.html', {'response':response_text})