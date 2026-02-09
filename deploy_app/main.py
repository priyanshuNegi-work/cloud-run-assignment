import os
import time
import psutil  # <--- NEW: Tool to read system metrics
from flask import Flask, jsonify

app = Flask(__name__)

# Record the start time when the container boots up
START_TIME = time.time()

@app.route("/")
def hello_world():
    # Task 2 Requirement
    return "Hello from Cloud Run! System check complete."

@app.route("/analyze")
def analyze_system():
    # Task 4 Extension Logic

    # 1. Calculate Uptime
    current_time = time.time()
    uptime_seconds = int(current_time - START_TIME)

    # 2. Get Resource Metrics
    cpu_usage = psutil.cpu_percent(interval=0.1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent

    # 3. Calculate Health Score (0-100)
    # Simple Logic: 100 minus the average load
    average_load = (cpu_usage + memory_usage) / 2
    health_score = max(0, 100 - average_load) 

    # 4. Human-readable message
    if health_score > 80:
        message = "System is healthy."
    elif health_score > 50:
        message = "System is under load."
    else:
        message = "System is stressed!"

    return jsonify({
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(current_time)),
        "uptime_seconds": uptime_seconds,
        "cpu_metric": f"{cpu_usage}%",
        "memory_metric": f"{memory_usage}%",
        "health_score": round(health_score, 2),
        "message": message
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
