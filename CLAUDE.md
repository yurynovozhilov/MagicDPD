# Claude Instructions for MagicDPD

## Python packages

Never install Python packages with `--break-system-packages`.
Use a virtual environment instead:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install <package>
```
