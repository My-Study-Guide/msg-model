import requests
import utils

API_URL = 'http://localhost:8000/process'

text_input = utils.read_txt('samples/sample_text1.txt')
topic = utils.read_txt('samples/sample_topic1.txt')

data = {
    'text': text_input,
    'topics': topic
}

response = requests.post(API_URL, json=data)

if response.status_code == 200:
    result = response.json()
    print("Score:", result['score'])
    print("Reason:", result['reason'])
    print("Summary:", result['summary'])
else:
    print("Error:", response.status_code, response.text)
