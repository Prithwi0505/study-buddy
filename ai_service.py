import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 🔑 IMPORTANT:
# OpenAI SDK internally requires OPENAI_API_KEY to exist
# We map OpenRouter key to it for Railway + local compatibility
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "Study Buddy"
    }
)

def analyze_syllabus(text: str):
    prompt = f"""
You are an exam-focused academic assistant.

The text below was extracted using OCR from an image.
It may be noisy, incomplete, or missing bullet points.

Your task:
1. Identify the subject (if possible)
2. Identify units/modules
3. Infer standard exam-relevant topics for each unit,
   even if the topics are not explicitly listed
4. For EACH unit, try to provide:
   - At least 2 Very Important topics (if academically reasonable)
   - Some Important topics
5. Only leave a list empty if inference is genuinely impossible

Classify topics into:
- Very Important
- Important
- Optional

Return ONLY valid JSON in this EXACT format:

{{
  "subject": "",
  "units": [
    {{
      "unit_name": "",
      "very_important": [],
      "important": [],
      "optional": []
    }}
  ]
}}

OCR Extracted Text:
{text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
