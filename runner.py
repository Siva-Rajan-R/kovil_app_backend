# run_both.py
import subprocess

# Start Gunicorn with Uvicorn workers
gunicorn_cmd = [
    "gunicorn",
    "main:app",
    "-k", "uvicorn.workers.UvicornWorker",
    "--bind", "0.0.0.0:8000",
    "--timeout", "90"
]
gunicorn_proc = subprocess.Popen(gunicorn_cmd)

# Start ARQ worker
arq_proc = subprocess.Popen(["arq", "arq_bgtasks.main.WorkerSettings"])

# Wait for both to finish
gunicorn_proc.wait()
arq_proc.wait()
