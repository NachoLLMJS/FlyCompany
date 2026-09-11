# Fly Company

Fly Company is an automatic research office where six embodied fly agents investigate BNB/Flap token ideas, hold meetings, preserve their working memory, and publish proposals for human review.

## Run locally

Open `Start Fly Company.cmd`, or run:

    python server.py

Then open http://127.0.0.1:4775. The server listens only on localhost. Closing the browser does not stop the server; stop the Python process to stop the company.

Railway can use the included `Procfile` and `/api/health` endpoint for the web service.

Set these Railway variables in the service settings:

- `DATABASE_URL`: attach Railway PostgreSQL and use its generated value
- `LLM_API_KEY`: secret for the selected OpenAI-compatible provider
- `LLM_BASE_URL`: provider base URL without `/chat/completions`
- `LLM_MODEL`: model identifier to use for Fly Company meetings

Do not commit real values. `.env.example` contains only empty placeholders.

## Automatic behavior

- Research and meetings run automatically every two hours.
- The first automatic cycle is scheduled shortly after the server starts.
- There are no Start research, Gather the team, or scheduler controls in the visitor UI.
- Visitors watch the flies, sources, live meeting messages, memories, and proposal history.
- Automatic cycles retry shortly when the Hermes provider is still warming up or temporarily unavailable.
- The persistent local state is stored in `data/company.sqlite3`.
- A Railway PostgreSQL connection can replace local persistence by setting `DATABASE_URL`. The included `requirements.txt` installs the PostgreSQL driver. Railway should provide `PORT`; the server automatically binds to `0.0.0.0` there and keeps localhost-only binding for local runs.
- Meeting and research changes are persisted to the PostgreSQL `events` table and streamed to visitors through `/api/events` using Server-Sent Events.

## Model and research

The default provider uses the authenticated local Hermes runtime for `gpt-6-astra` / `openai-codex`. OAuth credentials are never copied into this project. Each turn runs in a bounded subprocess with no tools, personal memory, or project context. The provider fails closed when its interface or authentication is unavailable.

The current source collection is limited to CoinDesk RSS and official Flap documentation. Every finding links to its original source. Agent messages are model-generated and can still be wrong; citations are evidence pointers, not automatic truth verification.

An OpenAI-compatible provider can be configured with `LLM_API_KEY`, `LLM_BASE_URL`, and `LLM_MODEL` in the process environment. Secrets must remain outside public files.

## Launch boundary

The Launch desk is proposal-only. Fly Company does not own a wallet, sign transactions, generate calldata, deploy contracts, move funds, or launch a token automatically. Human review remains required when the team eventually recommends a token.

## Tests

    python -m unittest discover -s tests
    node --test tests/*.mjs

The browser QA scripts require a running server and Google Chrome:

    node scripts/qa.mjs
    node scripts/qa-meeting.mjs

## Scientific assets

The office uses original NeuroMechFly anatomical meshes and exported pose data. The fly movement is visual playback, not a full brain emulation or validated live biomechanical simulation. Provenance and licenses are available in `public/licenses/` and the Science tab.

The local launcher remains localhost-only. On Railway, set `DATABASE_URL`; Railway supplies `PORT`, and the server automatically binds to `0.0.0.0`.
