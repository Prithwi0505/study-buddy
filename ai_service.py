import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# -------------------------------
# ENV VALIDATION (CRITICAL)
# -------------------------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not set. "
        "Add it in Railway → Variables."
    )

# OpenAI SDK requires this name internally
os.environ["OPENAI_API_KEY"] = OPENROUTER_API_KEY

# -------------------------------
# OPENROUTER CLIENT
# -------------------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://study-buddy.up.railway.app",
        "X-Title": "Study Buddy"
    }
)

# -------------------------------
# SYLLABUS ANALYSIS
# -------------------------------
def analyze_syllabus(text: str):
    prompt = f"""
You are an exam-focused academic assistant.

The text below may be noisy or incomplete.

Your task:
1. Identify the subject (if possible)
2. Identify units/modules
3. Infer standard exam-relevant topics for each unit
4. For EACH unit provide:
   - Very Important topics
   - Important topics
   - Optional topics

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

Text:
{text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content