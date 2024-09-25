from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import re

login("your_hf_token")

# update required (using api)
with open('hello.txt', 'r') as file:
    text_input = file.read()

model_name = "google/gemma-2-2b-it"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    # device_map="auto",
)

chat = [
    { "role": "user", "content": f"Please summarize the following text in three lines or less.:{text_input}" },
]
prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

input_ids = tokenizer(prompt, return_tensors="pt")

outputs = model.generate(
    **input_ids,
    max_length=2000,
    do_sample=True,
    top_p=0.95,
    temperature=0.7,
    repetition_penalty=1.1,
)

raw_summary = tokenizer.decode(outputs[0])

pattern = r'<start_of_turn>model\s*(.*?)\s*<end_of_turn>'

match = re.search(pattern, raw_summary, re.DOTALL)

if match:
    # 그룹에서 매칭된 내용 추출
    summary = match.group(1).strip()
    print("summary:")
    print(summary)
else:
    print("Error!")

# summary -> 최종본