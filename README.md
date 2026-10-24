# Pantry — Smart Recipe Generator

Pantry turns ingredients you already have into a practical recipe, with cuisine, serving-size, and dietary preferences. The app uses the Python recipe logic in `model.py` and `tools.py`, a FastAPI API, and a static frontend.

## Run locally

1. Use Python 3.10 or newer and install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Create a `.env` file based on `.env.example` and set `OPENAI_API_KEY`.

3. Start the app:

   ```powershell
   python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
   ```

4. Open <http://localhost:8000>.

The UI and API are served from the same local origin. The existing Streamlit interface is also available with `streamlit run main.py` after installing Streamlit; its AI recipe generation uses the same `.env` settings.

## Deploy the API to Render

1. Push this repository to GitHub and create a new Render Blueprint using `render.yaml`.
2. Set `OPENAI_API_KEY` to your OpenAI API key in Render. Set `FRONTEND_URL` to the deployed Vercel site origin, for example `https://pantry-your-team.vercel.app`.
3. Deploy the service. Its health endpoint is `/api/health`.

The Render API base URL will look like `https://smart-recipe-api.onrender.com`.

## Deploy the frontend to Vercel

1. Import the same GitHub repository into Vercel.
2. Add the environment variable `RECIPE_API_URL` with the Render API base URL (for example, `https://smart-recipe-api.onrender.com`).
3. Deploy. The included `vercel.json` builds the static frontend into `dist`.

Set `FRONTEND_URL` in Render to the Vercel production origin after the Vercel site is created, then redeploy the Render service if necessary. For multiple allowed origins, separate them with commas.

## Configuration and safety

- Keep API keys in local `.env` files or deployment-provider environment settings. Never commit them.
- `OPENAI_MODEL` is optional and defaults to `gpt-4.1-mini`.
- The health response reports whether an AI key is configured, without exposing it.
- Recipe suggestions are not a substitute for checking food safety or ingredient labels. Verify allergens and cook food thoroughly.
