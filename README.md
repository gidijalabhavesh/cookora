# Pantry — Smart Recipe Generator

Pantry turns ingredients you already have into a practical recipe. Choose a
cuisine, serving count, and dietary preference, then get clear instructions,
estimated cooking times, substitutions, and food-safety reminders.

## Run locally

1. Use Python 3.10 or newer and install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` to your API key.
3. Start the app:

   ```powershell
   python -m uvicorn api:app --reload --host 127.0.0.1 --port 8001
   ```

4. Open <http://localhost:8001>.

The frontend and API run on the same origin locally. The original Streamlit
interface is also available with `streamlit run main.py` if Streamlit is
installed.

## Deploy the API to Render

1. Push this repository to GitHub and create a Render Blueprint from
   `render.yaml`.
2. Set `OPENAI_API_KEY` in Render's environment settings.
3. Set `FRONTEND_URL` to the Vercel site origin after deploying the frontend.
   Multiple allowed origins can be comma-separated.
4. Deploy the service and verify its `/api/health` endpoint.

## Deploy the frontend to Vercel

1. Import this repository into Vercel.
2. Set the `RECIPE_API_URL` environment variable to the Render API base URL
   (for example, `https://smart-recipe-api.onrender.com`).
3. Deploy the project. `vercel.json` builds the static files into `dist`.
4. Copy the Vercel production origin into Render's `FRONTEND_URL` and redeploy
   the Render service.

## Configuration and safety

- Keep API keys in local `.env` files or provider environment settings. Never
  commit secrets.
- `OPENAI_MODEL` is optional and defaults to `gpt-4.1-mini`.
- `/api/health` reports whether an AI key is configured, without exposing it.
- Recipe suggestions are not a substitute for checking food labels, allergens,
  or food-safety guidance. Verify ingredients and cook food thoroughly.