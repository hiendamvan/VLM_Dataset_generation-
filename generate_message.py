from google import genai
from google.genai import types
from dotenv import load_dotenv 
load_dotenv()
import os

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY")) 

for folder in os.listdir("./sample_images/"):
    for file in os.listdir(os.path.join("./sample_images/", folder)):
        print(file)
        if file.endswith(".jpg") or file.endswith(".png"):
            image_path = os.path.join("./sample_images/", folder, file)
            with open(image_path, "rb") as img_input:
                img_bytes = img_input.read()

            contents = [
                types.Part.from_bytes(data=img_bytes, mime_type="image/png"),
                "Is the Amperes value greater than 0. Answer OK or NOK!"
            ]
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=contents
            )
            print("-----------------------------------------------")
            print(response.text)
            break 
    break 