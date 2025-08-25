from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompt import PROMPTS, LINKS
import os
import json
import re

# Load API key
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def call_model(img_bytes: bytes, prompt: str, model: str = "gemini-2.0-flash") -> str:
    """Gọi Gemini với ảnh + prompt, trả về raw text."""
    contents = [
        types.Part.from_bytes(data=img_bytes, mime_type="image/png"),
        prompt,
    ]
    response = client.models.generate_content(model=model, contents=contents)
    return response.text.strip()


def extract_json(raw_output: str) -> dict:
    """Làm sạch output và parse JSON."""
    cleaned = raw_output.replace("```json", "").replace("```", "").strip()
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if not match:
        raise ValueError("No JSON object found in model response")
    return json.loads(match.group(0))


def process_image(image_path: str, prompt: str) -> dict:
    """Xử lý một ảnh, trả về dict JSON kết quả."""
    with open(image_path, "rb") as f:
        img_bytes = f.read()

    raw_output = call_model(img_bytes, prompt)
    data = extract_json(raw_output)
    data["image_path"] = image_path
    return data

OUTPUT_FILE = "dataset.jsonl"
def main():
    cnt = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
        for task_name, folder in LINKS.items():
            prompt = PROMPTS[task_name]
            for file in os.listdir(folder):
                if file.lower().endswith((".jpg", ".png")):
                    image_path = os.path.join(folder, file)
                    print(f"Processing {task_name} - {file}")
                    try:
                        result = process_image(image_path, prompt)
                        f_out.write(json.dumps(result, ensure_ascii=False) + "\n")
                        print(result)
                    except Exception as e:
                        print("Error:", e)

                    # cnt += 1
                    # if cnt == 10:  # debug: giới hạn số ảnh, bỏ nếu muốn full
                    #     return


if __name__ == "__main__":
    main()
