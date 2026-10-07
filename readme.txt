NeuroAI - Video Demo Script
============================
Goal: ~2 minute walkthrough

0. BEFORE RECORDING
--------------------
- Start the server:
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

- Confirm models are ready:
  curl -s http://localhost:11434/api/tags | jq '.models[].name'
  (should show "mistral" and "orca-mini")

- Open http://localhost:8000/static/demo.html


1. INTRO (10-15 sec)
---------------------
"This is NeuroAI - a containerized FastAPI microservice that runs
open-source AI models like Mistral and Orca Mini locally through Ollama.
Every request is protected by JWT authentication, and all data is
validated with Pydantic v2."

Briefly show the Architecture tab.


2. REGISTER TAB (15 sec)
-------------------------
Fill in username / email / password, click Register.

"I'll create an account - the password is hashed with Argon2 before
it's stored, never saved in plain text."


3. LOGIN TAB (15 sec)
----------------------
Login with the same credentials.

"Logging in returns a JWT access token - this is what authorizes every
protected API call from here on. You can see it right in the response."


4. AI MODEL TAB (40-50 sec) - the core demo
--------------------------------------------
Select Provider: Ollama -> Model: Orca Mini (or Mistral) -> type a
prompt like "What is machine learning?" -> click Generate Text.

"I'll send an authenticated request to generate text. The request body
is validated with a Pydantic v2 schema - if I'm not logged in or the
token's invalid, this gets rejected with a 401."

Show the real generated output. Click Check Status.

"This confirms the model is running locally - no external API calls,
fully open-source."


5. API FLOW TAB (15 sec)
-------------------------
"This tab visualizes the full request lifecycle - register, login,
receive token, attach token to every request, get a validated JSON
response back."


6. ENDPOINTS / RAW REQUESTS TABS (15 sec)
------------------------------------------
"Every endpoint and its raw request/response shape is documented here -
this isn't just a UI demo, it's the actual API contract."

(Optional: show /docs Swagger UI too.)


7. ADMIN TAB - RBAC DEMO (30-40 sec)
--------------------------------------
"NeuroAI also has role-based access control - two roles, user and admin.
Everyone registers as a plain user. The first admin has to be bootstrapped
from the terminal, since there's no admin yet to promote anyone."

In a terminal (before or during recording):
  python scripts/create_admin.py <your_username>

"Now that I'm an admin, logging back in shows 'admin' right next to my
name in the top-right status chip."

Go to the Admin tab:
- Click "List All Users" -> shows every registered user and their role.
- Promote another username to admin, then List Users again to confirm.
- Delete a user, then List Users again to confirm it's gone.

"And to prove this is actually enforced, not just hidden in the UI -"
Log out, log in as a different, non-admin account, open the Admin tab,
click any button:

"Same endpoint, but now it returns 403 Forbidden - the role check happens
server-side, in the require_admin dependency, not just by hiding a button."


8. WRAP-UP (10 sec)
--------------------
"NeuroAI is a JWT-secured, Pydantic-validated FastAPI microservice with
role-based access control, serving open models locally via Ollama, fully
containerized with Docker. Code is on GitHub."

Show: github.com/Manojkumar43774/assignment-2


BACKUP COMMANDS IF UI HAS ISSUES
---------------------------------
curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo_user","password":"DemoPass123"}' | jq .

curl -s -X POST http://localhost:8000/model/generate \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"What is machine learning?","max_tokens":100,"temperature":0.7,"provider":"ollama","model":"orca-mini"}' | jq .
