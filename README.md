# Cho-Han (catalog #446)

Even/odd dice betting game from Sweigart’s *Big Book of Small Python Projects*, Project #15.

## Run the web demo (port 3034)

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\cho-han\web"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload --reload-dir .. --port 3034
```

Open http://localhost:3034

Provenance: [BOOK_DIRECTIONS.md](./BOOK_DIRECTIONS.md).
