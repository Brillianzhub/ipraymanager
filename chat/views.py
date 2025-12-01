import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def chat_with_model(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        user_prompt = data.get("prompt", "")

        # Forward to Ollama running locally
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama2",
                    "prompt": user_prompt
                },
                stream=False
            )
            model_output = response.json()
            return JsonResponse(model_output, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST only"}, status=405)
