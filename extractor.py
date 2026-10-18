import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from jsonschema import ValidationError, validate

MODEL = "gemini-3.5-flash-lite"

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def load_prompt(path):
    """Split the prompt file into the system instruction and the user template."""
    text = Path(path).read_text(encoding="utf-8")
    system_part, user_part = text.split("USER:", 1)
    system = system_part.replace("SYSTEM:", "").strip()
    user_template = user_part.strip()
    return system, user_template


def extract(input_text, prompt_path="prompts/v1_basic.txt"):
    """Send one application to the model and return the raw reply text."""
    system, user_template = load_prompt(prompt_path)
    user_message = user_template.replace("{{input_text}}", input_text)
    response = client.models.generate_content(
        model=MODEL,
        contents=user_message,
        config=genai.types.GenerateContentConfig(system_instruction=system),
    )
    return response.text


def parse_and_validate(raw_text, schema):
    """Turn the reply into a dictionary and check it against the schema."""
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").removeprefix("json").strip()
    data = json.loads(cleaned)
    validate(instance=data, schema=schema)
    return data


if __name__ == "__main__":
    schema = json.loads(Path("schema.json").read_text(encoding="utf-8"))
    sample = "Ada Obi is a 300-level Computer Engineering student at the University of Uyo, applying for a Data Analyst internship starting 2 February 2027."
    raw = extract(sample)
    print("Raw reply:", raw)
    try:
        result = parse_and_validate(raw, schema)
        print("Valid:", json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValidationError) as error:
        print("Failed:", error)