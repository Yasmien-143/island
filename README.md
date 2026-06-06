# Island Mini System

Simple Flask app to coordinate an island meet on **Wednesday, June 10, 2026**.

Features:
- Users can vote whether they are available on the date
- Users can add items to bring (shared list)
- Data persisted in a database (Postgres recommended for deployment)

Quick start (local):

```bash
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
# optional: set DATABASE_URL to a Postgres URL, otherwise SQLite will be used
python app.py
```

Deploy to Render:
1. Push this repository to GitHub.
2. Create a new Web Service on Render and connect your repo.
3. Set the build command to `pip install -r requirements.txt` and the start command to `gunicorn app:app`.
4. Add a PostgreSQL database on Render and set the `DATABASE_URL` environment variable in the service settings to the provided Postgres URL.

API endpoint:
- `GET /api/status` returns JSON with `date`, `yes`, `no`, and `items`.

If you want, I can: push a Git repo, create a Render `render.yaml`, or add user authentication. What would you like next?
