# Python + Flask

To run dev mode:

- cd server-test
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `export FLASK_APP=entrypoint.py`
- `export APP_SETTINGS_MODULE=config.dev`
- `flask run --debug`

Docker image:

- In process...
