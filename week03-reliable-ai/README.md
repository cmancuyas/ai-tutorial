# Week 3: Making Your AI Reliable

Your Week 2 pipeline works when everything goes well. This week you make it
ready for the real world:

| Lesson | Question it answers |
|---|---|
| 1. Prompt engineering | How do I get **consistent, correct** answers, and **prove** a prompt is better? |
| 2. Errors and retries | What happens when Azure is busy, slow, or my config is wrong? |
| 3. Async / parallel | How do I process 10,000 comments in minutes instead of hours? |
| 4. Prompt injection | What if a comment tries to **hijack** my AI? |
| Exercise | Combine everything into one reliable pipeline |

> Reminder: every command starts with `python -m uv`.

---

## Part A: Put your work in Git (20 minutes, do this first)

Git keeps a history of your code, and GitHub shows it to employers.
The job posting asks for Git experience, so from now on every week gets committed.

### Step 1: Check Git
Open a terminal in VS Code and type:
```powershell
git --version
git config --global user.name
git config --global user.email
```
You should see a version number, your name, and your email.
If the email is empty, set it (use the email of your GitHub account):
```powershell
git config --global user.email "you@example.com"
```

### Step 2: Create the repository (in the `ai tutorial` folder, not a week folder)
1. In VS Code: **File > Open Folder**, choose the **`ai tutorial`** folder itself.
   You should see `ai-learning`, `week02-first-llm-call`, `week03-reliable-ai`,
   `.gitignore` and `README.md` on the left.
2. In the terminal:
```powershell
git init
git add .
git status
```

### Step 3: SAFETY CHECK before your first commit ⚠️
Read the list that `git status` printed under **"Changes to be committed"**.
- ✅ You should see `.env.example` files, `.py` files, `README.md`, `pyproject.toml`...
- ❌ You must **NOT** see any file named exactly **`.env`**, or any **`.venv`** folder.

The `.gitignore` file in the `ai tutorial` folder keeps them out. If you DO
see `.env` in the list, stop and ask Claude before continuing.

### Step 4: Commit
```powershell
git commit -m "Weeks 1-3: Python basics, first LLM calls, reliable AI pipeline"
```
A **commit** is a saved snapshot of your project, like a save point in a game.

### Step 5: Put it on GitHub (optional today, but do it this week)
1. Go to https://github.com and sign in (or create a free account).
2. Click **+** (top right) > **New repository**.
3. Name: `ai-engineering-journey`. Choose **Private** for now (you can make it
   public later, when you're ready to show employers).
4. Do **NOT** tick "Add a README" (you already have one). Click **Create repository**.
5. GitHub shows commands under **"...or push an existing repository"**. Run them;
   they look like this (with your own username):
```powershell
git remote add origin https://github.com/YOUR-USERNAME/ai-engineering-journey.git
git branch -M main
git push -u origin main
```
6. A browser window may open asking you to sign in to GitHub. Sign in yourself.

From now on, after each lesson or exercise:
```powershell
git add .
git commit -m "Short description of what you did"
git push
```

---

## Part B: Set up Week 3 (5 minutes)

### Step 6: Copy your .env file
Your Week 2 `.env` already works. Copy it into this folder:
1. In the VS Code sidebar, right-click `week02-first-llm-call/.env` > **Copy**.
2. Right-click the `week03-reliable-ai` folder > **Paste**.

### Step 7: Install packages
In the terminal, go into the Week 3 folder and install:
```powershell
cd week03-reliable-ai
python -m uv sync
```

---

## Part C: The lessons

### Lesson 1: Prompt engineering, measured (45 minutes)
```powershell
python -m uv run python 01_prompt_engineering.py
```
✅ You'll see a lazy prompt (V1) and the improved prompt (V2) answer the same 7
tricky comments, and a **score** for each. Read `feedback.py` to see what makes V2 better.

### Lesson 2: Errors and retries (30 minutes)
```powershell
python -m uv run python 02_errors_and_retries.py
```
✅ You'll catch a 404, a timeout, and watch a retry loop recover from a failing service.

### Lesson 3: Parallel calls (30 minutes)
```powershell
python -m uv run python 03_async_parallel.py
```
✅ The same 10 comments, one at a time vs 5 at a time. Parallel should be several times faster.

### Lesson 4: Prompt injection (30 minutes)
```powershell
python -m uv run python 04_prompt_injection.py
```
✅ You'll see attacks hidden in comments, and whether the vulnerable and defended versions fall for them.

### Week 3 exercise: the reliable pipeline (1 to 2 hours)
Open `05_exercise_reliable_pipeline.py` and fill in the 4 TODOs.
```powershell
python -m uv run python 05_exercise_reliable_pipeline.py
```
✅ Done when it classifies all 20 comments in parallel, lists urgent comments,
lists comments for human review (the 2 injection attempts in the CSV should
appear), and survives errors without crashing.

Then: `git add .`, `git commit -m "Week 3 exercise"`, `git push`. 🎉

---

## Checklist for Week 3
- [ ] Repository created, first commit done, and NO `.env` file committed
- [ ] (This week) Pushed to GitHub
- [ ] Lesson 1: you know V1 and V2's scores, and tried experiment (d)
- [ ] Lesson 2: you can explain which errors to retry and which to fix
- [ ] Lesson 3: you measured how much faster parallel is
- [ ] Lesson 4: you tried writing your own attack
- [ ] Exercise: all 4 TODOs done, and it survives a failing comment

Next: **Week 4: RAG**, so the AI can answer questions using YOUR documents.

---

## Common problems
| Problem | Fix |
|---|---|
| `Setup needed: copy your .env file...` | Do Step 6. |
| `git` says "not a git repository" | You're in the wrong folder. Run Git commands in the `ai tutorial` folder. |
| `git status` shows `.env` | Stop. Don't commit. Check that `ai tutorial\.gitignore` exists and contains `.env`, then ask Claude. |
| `RuntimeError: ... event loop` | Run the file with `python -m uv run python ...`, not from a notebook or the Run button. |
| `429` errors in Lesson 3 | Too many at once for your quota. Lower `Semaphore(5)` to `Semaphore(2)`. |
| `IndentationError` | Turn on View > Appearance > Render Whitespace > **Boundary** and count the dots. |
