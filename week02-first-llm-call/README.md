# Week 2: Your First AI Calls from Python

Goal this week: connect Python to a real AI model on Azure, build a chat
program, and get **typed, structured data** back from the AI (the skill
you'll use in almost every AI project).

Do the steps **in order**.

> Reminder: you installed uv with the backup method, so every command
> starts with `python -m uv`.

---

## Part A: Create your AI model on Azure (about 30 to 45 minutes, one time only)

Azure's website changes its screens often. If a button has a slightly
different name than below, look for the closest match, or send Claude a
screenshot.

### Step 1: Create an Azure account
1. Go to https://azure.microsoft.com/free and click **Try Azure for free**.
2. Sign in with a Microsoft account (or create one).
3. Fill in the form. A card is used to verify your identity.
   Microsoft says you won't be charged unless you choose to upgrade.

### Step 2: Set a budget alert (5 minutes, do NOT skip this)
This emails you if you ever spend money, so there are no surprises.
1. Go to https://portal.azure.com
2. In the top search bar, type **Cost Management** and open it.
3. Click **Budgets**, then **+ Add**.
4. Set the amount to **5** (US dollars), monthly. Add your email for alerts at 50% and 100%.
5. Click **Create**.

### Step 3: Create an AI resource and project
1. Go to https://ai.azure.com (this is **Microsoft Foundry**, which used to be
   called Azure AI Foundry) and sign in with the same account.
2. Click **Create project** (or **+ New project**).
3. Give it a name, for example `ai-learning`.
4. If it asks for a **region**, choose one near you that is listed, for example
   **East US 2** or **Southeast Asia**. (Not every model exists in every region;
   if the model in Step 4 isn't available, try East US 2.)
5. Click **Create** and wait a minute or two.

### Step 4: Deploy a model
"Deploying" means: making a copy of the model available to your account.
1. In your project, open **Models + endpoints** or **Model catalog** (left menu).
2. Click **Deploy model** / **Deploy base model**.
3. Choose a **small, cheap chat model**. Look for one with **"mini"** in the
   name, for example `gpt-4.1-mini` or `gpt-5-mini`. Mini models are much
   cheaper and more than good enough for learning.
4. Keep the default deployment type and click **Deploy**.
5. Write down the **deployment name** (often the same as the model name).

### Step 5: Copy your 3 values
Open your deployment's page. You need:
1. **Endpoint** (may be called "Target URI" or "Azure OpenAI endpoint").
   It looks like `https://SOMETHING.openai.azure.com/...` or
   `https://SOMETHING.cognitiveservices.azure.com/...`
2. **Key** (click the copy button next to it; "Key 1" if there are two).
3. The **deployment name** from Step 4.

> ⚠️ The key is like a password: anyone who has it can spend your credits.
> Never post it online, in screenshots, or in chat (including with Claude).

---

## Part B: Set up the project (10 minutes)

### Step 6: Create your .env file (where your secret key lives)
1. In VS Code: **File > Open Folder**, choose `ai tutorial\week02-first-llm-call`.
2. In the left sidebar, right-click `.env.example`, choose **Copy**, then
   right-click in empty space and **Paste**. Rename the copy to exactly **`.env`**.
3. Open `.env` and fill in your values:
   - `AI_ENDPOINT`: take the start of your endpoint, **up to and including
     `.azure.com`**, and add `/openai/v1/` at the end.
     Example: `https://my-ai-resource.openai.azure.com/openai/v1/`
   - `AI_API_KEY`: your key
   - `AI_MODEL`: your deployment name
   - The two prices: find your model on the Azure OpenAI pricing page
     (search "Azure OpenAI pricing"). They're only used to show you costs, so
     if you can't find them, leave the example values.
4. Save the file.

Why a .env file? It's like `dotnet user-secrets` or `appsettings.Development.json`
that you never commit. `.gitignore` already excludes it from Git.

### Step 7: Install the packages
```powershell
python -m uv sync
```
(Same as Week 1: reads `pyproject.toml`, creates `.venv`, installs packages.)

---

## Part C: The lessons

### Lesson 1: Hello AI (30 minutes)
```powershell
python -m uv run python 01_hello_ai.py
```
✅ You should see a 2-sentence answer about REST APIs, then token counts and a
cost (a tiny fraction of a cent). Then do the experiments at the bottom of the file.

### Lesson 2: Chat with memory (45 minutes)
```powershell
python -m uv run python 02_chat.py
```
Chat with it, then type `exit`. Key idea: **the model has no memory**. We
resend the whole conversation every time. Do the experiments at the bottom.

### Lesson 3: Structured outputs (1 hour, the most important lesson)
```powershell
python -m uv run python 03_structured_output.py
```
✅ Each comment comes back as a typed `Feedback` object (sentiment, topic,
urgent, summary), including the Tagalog one. Do the experiments at the bottom.

### Week 2 exercise: classify a whole CSV (1 to 2 hours)
Open `04_classify_csv.py` and fill in the 4 TODOs. Run it with:
```powershell
python -m uv run python 04_classify_csv.py
```
✅ When it works, you get `results.csv` (open it in Excel), a sentiment count,
the list of urgent comments, and the total cost for 12 comments.

Then ask Claude to review your code.

---

## Checklist for Week 2
- [ ] Azure account created, with a $5 budget alert
- [ ] A mini model deployed, and the `.env` file filled in
- [ ] Lesson 1 runs and shows tokens and cost
- [ ] Lesson 2: the chat remembers your name
- [ ] Lesson 3: you added the `language` field and it works
- [ ] Exercise: `results.csv` created, urgent comments printed

Next: **Week 3: prompt engineering and handling errors**
(what to do when the AI is wrong, slow, or the call fails).

---

## Common problems
| Problem | Fix |
|---|---|
| `Setup needed: your .env file is missing...` | Do Step 6. The file must be named exactly `.env` (not `.env.txt`). |
| `401` / `Access denied` / `invalid key` | Wrong key, or the key and endpoint come from different resources. Copy both again. |
| `404` / `DeploymentNotFound` | `AI_MODEL` must be the **deployment** name. Also check that `AI_ENDPOINT` ends with `/openai/v1/`. |
| `429` / `rate limit` | You sent too many requests too fast. Wait a minute and run again. |
| An error about `temperature` or `max_tokens` not supported | Some newer models don't accept these settings. Remove that argument. |
| `ModuleNotFoundError` | Run `python -m uv sync`, and always use `python -m uv run python ...`. |
