NeuroAI - Video Demo Script
============================
Goal: ~2-3 minute walkthrough

0. BEFORE RECORDING
--------------------
- Start the server:
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

- Confirm models are ready:
  curl -s http://localhost:11434/api/tags | jq '.models[].name'
  (should show "mistral", "orca-mini", and "llava")

- Open http://localhost:8000/static/demo.html
  (the AI Model tab is now the default tab that loads first)


1. INTRO (10-15 sec)
---------------------
"This is NeuroAI - a containerized FastAPI microservice that runs
open-source AI models like Mistral, Orca Mini, and the vision model
LLaVA locally through Ollama. Every request is protected by JWT
authentication, all data is validated with Pydantic v2, and access is
further restricted with role-based access control."

Briefly show the Architecture tab.


2. AI MODEL TAB - LOGGED OUT (10 sec)
---------------------------------------
The page opens on the AI Model tab by default, styled like a ChatGPT-
style chat screen. Try typing a prompt and hitting send while logged out.

"If I try to chat, attach a photo, or use the mic without being logged
in, NeuroAI pops up a login/register prompt right here instead of just
failing silently - the same modal appears anywhere in the app that
needs auth, including the Admin tab."

Click "Register" on the popup to jump to the Register tab.


3. REGISTER TAB (15 sec)
-------------------------
Fill in username / email / password (fields start blank with ghost
placeholders like "Enter username"), click Register.

"I'll create an account - the password is hashed with Argon2 before
it's stored, never saved in plain text. There's also a show/hide
password toggle on every password field."


4. LOGIN TAB (15 sec)
----------------------
Login with the same credentials.

"Logging in returns a JWT access token - this is what authorizes every
protected API call from here on. You can see it right in the response."


5. AI MODEL TAB - CHAT + VOICE (30-40 sec)
---------------------------------------------
Back on the AI Model tab, now logged in. Type a prompt like
"What is machine learning?" (or click a suggestion chip) and hit send.

"This is a full chat interface - messages render as bubbles, and I can
expand the settings gear to pick a provider/model, max tokens, and
temperature without cluttering the main screen."

Click the mic icon and speak a prompt instead of typing it.

"Voice input runs entirely in the browser via the Web Speech API - no
extra backend calls."


6. AI MODEL TAB - PHOTO / VISION DEMO (30-40 sec)
----------------------------------------------------
Click the paperclip, attach a photo, and ask a question about it, e.g.
"What is in this image?"

"Attaching a photo automatically switches the model to LLaVA, Ollama's
vision-capable model. The image is base64-encoded in the browser and
sent to /model/generate alongside the prompt - this is a real vision
answer, not a canned response. If I try the same thing on a text-only
provider like Hugging Face, the backend rejects it with a 400."

Click the X on the photo preview to remove it before sending, then show
Check Status (inside the settings popover) confirming the model is
running locally - no external API calls.


7. API FLOW / ENDPOINTS / RAW REQUESTS TABS (15 sec)
--------------------------------------------------------
"These tabs visualize the full request lifecycle and document every
endpoint's raw request/response shape - this isn't just a UI demo, it's
the actual API contract."

(Optional: show /docs Swagger UI too.)


8. ADMIN TAB - RBAC DEMO (30-40 sec)
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

"If I try any of this while logged out, the same login/register popup
from the AI Model tab shows up here too - these endpoints share one auth
prompt across the whole app."

"And to prove RBAC is actually enforced, not just hidden in the UI -"
Log out, log in as a different, non-admin account, open the Admin tab,
click any button:

"Same endpoint, but now it returns 403 Forbidden - the role check happens
server-side, in the require_admin dependency, not just by hiding a button."


9. WRAP-UP (10 sec)
--------------------
"NeuroAI is a JWT-secured, Pydantic-validated FastAPI microservice with
role-based access control and real vision support, serving open models
locally via Ollama, fully containerized with Docker. Code is on GitHub."

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

# Vision / photo demo (base64-encode a small image first):
IMG_B64=$(base64 -i photo.png | tr -d '\n')
curl -s -X POST http://localhost:8000/model/generate \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"What is in this image?\",\"max_tokens\":150,\"temperature\":0.7,\"provider\":\"ollama\",\"model\":\"llava\",\"image_base64\":\"$IMG_B64\"}" | jq .

# Admin RBAC (requires an admin token from create_admin.py):
curl -s http://localhost:8000/admin/users \
  -H "Authorization: Bearer <ADMIN_TOKEN>" | jq .
curl -s -X POST http://localhost:8000/admin/users/<username>/promote \
  -H "Authorization: Bearer <ADMIN_TOKEN>" | jq .
curl -s -X DELETE http://localhost:8000/admin/users/<username> \
  -H "Authorization: Bearer <ADMIN_TOKEN>" | jq .
