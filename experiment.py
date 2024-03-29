# Target 
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

with open("EnglishTarget.txt", "r") as file:
    text = file.read()
# Fine tuning using Prompt

genai.configure(api_key="AIzaSyDiEvJyv_j5ZLMDt6E6lSM3ytQTqvWEpUE")

def generate_gemini_content(tulisan, prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+tulisan)
    return response.text

hint1="Berikan hint untuk tebakan kata dari kata di bawah ini"
hint2='Berikan ciri-ciri untuk tebakan kata dari kata di bawah ini'
hint3="Berikan penjelasan terkait kata di bawah ini, tanpa menyebutkan katanya"
        
hint = generate_gemini_content(text, hint1)
print("Hint", hint)