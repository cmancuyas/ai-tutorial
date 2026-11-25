# Week 1: Python for a C# Developer

Goal this week: get Python tools set up, learn the basic syntax, and build
and test a small web API. Do the steps **in order**. Each step says what to
type and what you should see.

---

## Part A: Install the tools (about 15 minutes)

### Step 1: Check Python (already installed on your PC)
Open **PowerShell** (Start menu, type `PowerShell`, press Enter) and type:

```powershell
python --version
```

You should see `Python 3.14.x` (any 3.12 or newer is fine).
If you see an error instead, install Python from https://www.python.org/downloads/
and tick **"Add python.exe to PATH"** during setup.

### Step 2: Install uv (the package manager)
`uv` does the job of `dotnet` + NuGet: it creates the project environment
and downloads packages.

```powershell
winget install --id=astral-sh.uv -e
```

**Close PowerShell and open a new one** (so it picks up the new command), then check:

```powershell
uv --version
```

You should see something like `uv 0.x.x`.

### Step 3: Set up your editor (Cursor or VS Code)
You have Cursor installed, which works the same as VS Code. Open it, go to the
**Extensions** panel (`Ctrl + Shift + X`) and install:

1. **Python** (by Microsoft / ms-python): runs and debugs Python
2. **Ruff** (by Astral): formats your code and points out mistakes

(Pylance or a similar language server is installed with the Python extension;
it gives you IntelliSense like in Visual Studio.)

---

## Part B: Open the project (5 minutes)

### Step 4: Open this folder in your editor
In Cursor: **File > Open Folder** and pick the `ai-learning` folder.

Open the terminal inside the editor: **View > Terminal** (or `` Ctrl + ` ``).
All commands below are typed there.

### Step 5: Install the project packages
```powershell
uv sync
```

What this does: creates a `.venv` folder (a private Python just for this
project, so packages don't mix between projects) and installs FastAPI,
pytest, etc. from `pyproject.toml`. It's like `dotnet restore`.

### Step 6: Pick the project's Python in the editor
Press `Ctrl + Shift + P`, type **Python: Select Interpreter**, and choose the
one that shows `.venv`. Now IntelliSense knows your packages.

---

## Part C: Learn (the actual lessons)

### Lesson 1: Python syntax (1 to 2 hours)
Open `lessons/01_python_basics.py` and read it top to bottom. Every section
shows the C# you know and the Python version. Then run it:

```powershell
uv run python lessons/01_python_basics.py
```

Do the 4 exercises at the bottom of the file. Re-run after each change.

> Tip: `uv run <command>` means "run this using the project's .venv".
> Always put `uv run` in front of `python`, `pytest`, and `uvicorn`.

### Lesson 2: A web API with FastAPI (1 to 2 hours)
Open `app/main.py` and read it. Then start the server:

```powershell
uv run uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs in your browser. This is Swagger, built in.
Try **POST /surveys** (click "Try it out"), then **GET /surveys** and **GET /stats**.
Try sending `"rating": 9` and look at the error you get back.

`--reload` restarts the server every time you save a file, like `dotnet watch`.
Press `Ctrl + C` in the terminal to stop it.

### Lesson 3: Tests with pytest (30 minutes)
Open `tests/test_main.py` and read it. Run the tests (stop the server first,
or open a second terminal with the `+` button):

```powershell
uv run pytest -v
```

You should see `5 passed`. If you also see "1 warning" about `httpx`, that's
fine: it comes from inside the library, not from your code. Then break something on purpose (change
`status_code=201` to `200` in `app/main.py`), run the tests again, and see one
fail. Change it back.

### Exercises (the important part)
At the bottom of `app/main.py` there are 3 exercises: add a DELETE endpoint,
add a "low ratings" endpoint, and write tests for both. Try them yourself
first. If you get stuck, ask Claude for a **hint**, not the full answer.

---

## Checklist for Week 1
- [ ] `python --version` and `uv --version` both work
- [ ] `uv sync` finished without errors
- [ ] Lesson 1 runs, and you finished its 4 exercises
- [ ] You saw the Swagger page at /docs and created a survey
- [ ] `uv run pytest -v` shows all tests passing
- [ ] You added DELETE and /surveys/low, with tests

When everything is ticked, you're ready for **Week 2: calling an LLM for the first time.**

---

## Common problems
| Problem | Fix |
|---|---|
| `uv : The term 'uv' is not recognized` | Close and reopen PowerShell / the editor after installing uv. |
| `ModuleNotFoundError: No module named 'fastapi'` | You ran `python` without `uv run`, or skipped `uv sync`. |
| `IndentationError` | Python uses spaces instead of `{ }`. Use 4 spaces per level; don't mix tabs and spaces. |
| Port 8000 already in use | A server is still running in another terminal. Press `Ctrl + C` there. |
| Red squiggles under imports in the editor | Do Step 6 (select the `.venv` interpreter). |
