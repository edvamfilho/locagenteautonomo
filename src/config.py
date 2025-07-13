from dotenv import load_dotenv
import os, pathlib
load_dotenv(pathlib.Path(__file__).resolve().parent.parent / ".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
