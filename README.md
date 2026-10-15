### 1. Clone the repository

```powershell
git clone https://github.com/lhumpherson/Make-It-All-System.git
cd Make-It-All-System
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On Mac or Linux, activate with `source .venv/bin/activate` instead.

If Windows says running scripts is disabled, run this once and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the app

From the project root:

```powershell
python main.py
```

## Working on the project

- Pull the latest changes before starting: `git pull`
- Create a branch for each feature: `git checkout -b feature/todo-screen`
- Open a pull request into `main` when done. Don't push directly to `main`.