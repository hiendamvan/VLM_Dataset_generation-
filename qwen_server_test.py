import os
import json
import re
import base64
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from prompt import PROMPTS, LINKS

# Load API key
load_dotenv()

# Tạo client Qwen
custom_client = AsyncOpenAI(
    base_url="https://netmind.viettel.vn/dgx-qwq/v1",  
    api_key=os.getenv("QWEN_API_KEY")
)

# Model bạn muốn dùng
MODEL_NAME = "Qwen/Qwen3-30B-A3B-Instruct-2507-FP8-server-78"

async def call_model(img_bytes: bytes, prompt: str, model: str = MODEL_NAME) -> str:
    """Gọi Qwen với ảnh + prompt, trả về raw text."""
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    
    response = await custom_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )
    return response.choices[0].message.content.strip()


def extract_json(raw_output: str) -> dict:
    """Làm sạch output và parse JSON."""
    cleaned = raw_output.replace("```json", "").replace("```", "").strip()
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if not match:
        raise ValueError("No JSON object found in model response")
    return json.loads(match.group(0))


async def process_image(image_path: str, prompt: str) -> dict:
    """Xử lý một ảnh, trả về dict JSON kết quả."""
    with open(image_path, "rb") as f:
        img_bytes = f.read()

    raw_output = await call_model(img_bytes, prompt)
    data = extract_json(raw_output)
    data["image_path"] = image_path
    return data


OUTPUT_FILE = "dataset.jsonl"

async def main():
    cnt = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
        for task_name, folder in LINKS.items():
            prompt = PROMPTS[task_name]
            for file in os.listdir(folder):
                if file.lower().endswith((".jpg", ".png")):
                    image_path = os.path.join(folder, file)
                    print(f"Processing {task_name} - {file}")
                    try:
                        result = await process_image(image_path, prompt)
                        f_out.write(json.dumps(result, ensure_ascii=False) + "\n")
                        print(result)
                    except Exception as e:
                        print("Error:", e)

                    # cnt += 1
                    # if cnt == 10:  # debug: giới hạn số ảnh, bỏ nếu muốn full
                    #     return


if __name__ == "__main__":
    asyncio.run(main())
