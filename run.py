from fastapi import FastAPI, Request
from pydantic import BaseModel
from huggingface_hub import login
from model import MSG
import utils
import os

hf_token = os.environ.get('HUGGING_FACE_HUB_TOKEN')
if hf_token is None:
    raise ValueError("HUGGING_FACE_HUB_TOKEN 환경변수가 설정되지 않았습니다.")

# Hugging Face login
login(hf_token)

msg = MSG(
    summarizing_model_name = "google/gemma-2-2b-it",
    scoring_model_name = "gemini-1.0-pro",
    device = "cpu", # depends
)

app = FastAPI()
class TextInput(BaseModel):
    text: str
    topics: str = ''

@app.post('/process')
async def process_text(input_data: TextInput):
    text_input = input_data.text
    topics = input_data.topics

    msg.summarize(text_input)

    score, reason = msg.scoring(topics)

    return {
        'score': msg.score,
        'reason': msg.reason,
        'summary': msg.summary
    }

