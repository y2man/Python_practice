ISAAC AI FRONTEND

1. Extract this folder into your project at:
   13_ai_and_llm_integration/06_ai_chat_frontend

2. In VS Code, open index.html with Live Server.
   The current backend URL is configured in script.js:
   https://python-practice-4cx5.onrender.com

3. IMPORTANT — update backend CORS before browser testing.
   In the backend main.py, update the existing CORSMiddleware settings to include PATCH and Authorization:

   allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
   allow_headers=["Content-Type", "Authorization"],

   Keep the existing localhost and 127.0.0.1 origins for Live Server port 5501.
   Commit and push the backend change so Render deploys it.

4. Open the frontend at http://127.0.0.1:5501 or http://localhost:5501.
   Register an account, sign in, then test new chats, history, rename, and delete.

NOTES
- JWT is stored in browser localStorage for this learning project. This is convenient but is less secure than an HttpOnly cookie for a production application; protect against XSS and never store passwords.
- The frontend uses the existing API response contracts: /register, /login, /ask, /conversations, /conversations/{id} GET/PATCH/DELETE.
- The Render free service may take a little time to wake up on its first request.
