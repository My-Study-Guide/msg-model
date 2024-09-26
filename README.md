# msg-model

### Requirments
`python >= 3.9`
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Environment Variable setting

For now, revise the code and add your Hugging Face token in the code.

`run.py`
```python
login("your_hf_token")
```
Will be updated as environment variable format soon.


**Google API Key**

Window
```bash
> setx GOOGLE_API_KEY "YOUR API KEY"
```
Linux(Ubuntu)
```bash
$ echo 'export GOOGLE_API_KEY='"YOUR API KEY"' >> ~/.bashrc
```

### Run
Execute `run.py`
```bash
python3 run.py
```