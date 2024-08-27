# main.py
import io
import logging
import base64
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import torch
from transformers import AutoModelForCausalLM, AutoProcessor

from app.models import OCRRequest, OCRResponse
from app.utils import extract_images_from_pdf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methds=["*"],
    allow_headers=["*"],
)

model_id = "microsoft/Phi-3.5-vision-instruct"
try:
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="cuda",
        trust_remote_code=True,
        torch_dtype="auto",
        #_attn_implementation='flash_attention_2'
    )
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True, num_crops=16)
    logger.info("Model and processor loaded successfully")
except Exception as e:
    logger.error(f"Error loading model and processor: {str(e)}")


@app.post("/process_pdf", response_model=OCRResponse)
async def process_pdf(file: UploadFile = File(...), request: OCRRequest = None):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload pdf")

    try:
        pdf_content = await file.read()
        images = extract_images_from_pdf

        if not images:
            raise HTTPException(status_code=400, detail="No images found in pdf")

        placeholder = "".join([f"<|image_{i+1}|>\n" for i in range(len(images))])
        messages = [
            {
                "role": "user",
                "content": placeholder + (request.prompt if request.prompt else "Describe the content of these images.")
            }
        ]
        prompt = processor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = processor(prompt, images, return_tensors="pt").to("cuda:0")

        generation_args = {
            "max_new_tokens": 1000,
            "temperature": 0.0,
            "do_sample": False,
        }

        generate_ids = model.generate(**inputs, eos_token_id=processor.tokenizer.eos_token, **generation_args)
        generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
        response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

        return OCRResponse(response=response)

    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occured while processing: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "health"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





