import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from groq import Groq
from django.shortcuts import render
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
    



class AiChatBotView(View):
    def get(self, request):
        return render(request, 'chat.html')
    

@csrf_exempt  # Allows testing without CSRF token (remove in production)
def bot_reply_with_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body).get("message", "")

            if not data:
                return JsonResponse({"error": "Message is required"}, status=400)

            client = Groq(
                api_key="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"  # Replace with your actual env var
            )

            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": data}],
                model="llama-3.3-70b-versatile",
            )

            ai_response = chat_completion.choices[0].message.content
            return JsonResponse({"response": ai_response})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)
