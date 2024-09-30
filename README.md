# msg-model

## Requirments
`python >= 3.9`
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Environment Variable setting



Linux/MacOS (bash/zsh):

```bash
export HUGGING_FACE_HUB_TOKEN='your_token_here'
export GOOGLE_API_KEY='your_apikey_here'
```

Windows (CMD):
```cmd
set HUGGING_FACE_HUB_TOKEN=your_token_here
set GOOGLE_API_KEY=your_apikey_here
```
Windows (PowerShell):
```powershell
$Env:HUGGING_FACE_HUB_TOKEN = 'your_token_here'
$Env:GOOGLE_API_KEY = 'your_apikey_here'
```

These commands are for a single session.
If you want to keep the variable, add the command in your shell configuration file. (~/.bashrc, ~/.zshrc, ...)

> Example
```bash
$ echo 'export GOOGLE_API_KEY='"YOUR API KEY"' >> ~/.bashrc
```


### Run
Execute `run.py`
```bash
python3 run.py
```