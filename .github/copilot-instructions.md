
# Project Instructions

## general instructions
- IMPORTANT RULE: always check the instruction in .github/copilot-instructions.md
- IMPORTANT RULE: always check the memory file in .memory/ to see the progress of the project
- your knowledge is outdated. When implementing code based on python packages, consult the official documentation in the internet for the most accurate and up-to-date information.
- to manage python packages and dependencies ALWAYS use the tool 'uv'
- to run the application use the command 'uv run main.py'
- use 'uv add <package_name>' to install new packages
- use functions from the 'icecream' package for debugging and logging.

## fastAPI
- the project has a backend built with FastAPI.
- it connects to the sqlite3 database named "database.db" using sqlalchemy.

## pydantic
- always use pydantic v2. documentation at https://docs.pydantic.dev/latest/api/base_model/

## google genai SDK
- The project uses the Google GenAI SDK for extracting data from patient notes from markdown files. The latest documentation is at https://github.com/googleapis/python-genai .
- The markdown files are located in pdf/markdown/ .
- The models to be used are gemini-2.5-flash-lite for very simple tasks, gemini-2.5-flash for regular tasks and gemini-2.5-pro for more complex tasks.
- To create structured output always use a pydantic V2 model. Check examples at: https://ai.google.dev/gemini-api/docs/structured-output 

## testing
- if you need to create testing scripts, ALWAYS create them in the tests/ directory.

## database
- the database is used to store patient and hospital admissions information.
- the database is a local sqlite3 database named "burning_man.db"

## memory
- create and update files for keeping track of the evolution of the project.
- these files should be stored in a dedicated directory called .memory/
- each time the project is updated, a new file should be created in the .memory/ directory with a timestamp and a brief description of the changes made.

## pipeline
- The pipeline is implemented in the `tests/` directory:
	- `tests/pdf_manager.py`: Converts and merges PDF files from `pdfs/` to markdown in `pdfs/markdown/`, with semantic markers and robust file handling.
	- `tests/doente_agente.py`: Extracts patient data from markdown files using Google GenAI and saves as JSON in `pdfs/json/`, skipping already processed files.
- All scripts use the `icecream` package for logging and debugging.
- Data flow:
	- Input PDFs: `pdfs/*.pdf`
	- Merged Markdown: `pdfs/markdown/*.md`
	- Extracted JSON: `pdfs/json/*-doente.json`
