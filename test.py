# run_both.py
import subprocess

# start uvicorn
uvicorn_proc = subprocess.Popen(["uvicorn", "main:app", "--reload"])

# start arq worker
arq_proc = subprocess.Popen(["arq", "arq_bgtasks.main.WorkerSettings"])

# wait for both
uvicorn_proc.wait()
arq_proc.wait()

