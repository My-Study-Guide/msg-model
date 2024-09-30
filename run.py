from huggingface_hub import login
from model import MSG
import utils
import os

hf_token = os.environ.get('HUGGING_FACE_HUB_TOKEN')
login(hf_token) # 환경변수

msg = MSG(
    summarizing_model_name = "google/gemma-2-2b-it",
    scoring_model_name = "gemini-1.0-pro",
    device = "cpu", # depends
)

text_input = utils.read_txt('sample_text.txt')
topics = ''
msg.summarize(text_input)
score, reason = msg.scoring(topics)
