import os
import time
from flask import Flask, jsonify
import threading


# -------------------------------
# Observation Manager
# -------------------------------

class ObservationManager:
    def __init__(self, max_entries=50, max_age_seconds=600):
        self.max_entries = max_entries
        self.max_age_seconds = max_age_seconds
        self.observations = []

    def add_snapshot(self, snapshot):
        self.observations.append(snapshot)
        self._cleanup_old_entries()

    def get_recent_history(self):
        return self.observations

    def _cleanup_old_entries(self):
        current_time = time.time()

        self.observations = [
            obs for obs in self.observations
            if current_time - obs["timestamp"] <= self.max_age_seconds
        ]

        if len(self.observations) > self.max_entries:
            self.observations = self.observations[-self.max_entries:]


# -------------------------------
# Raw System Readers
# -------------------------------

def read_cpu_times():
    with open("/proc/stat", "r") as f:
        first_line = f.readline()

    parts = first_line.split()
    cpu_values = list(map(int, parts[1:]))

    idle_time = cpu_values[3] + cpu_values[4]
    total_time = sum(cpu_values)

    return total_time, idle_time


def read_load_average():
    with open("/proc/loadavg", "r") as f:
        data = f.read().split()

    return {
        "last_1_min": float(data[0]),
        "last_5_min": float(data[1]),
        "last_15_min": float(data[2])
    }


def read_memory_info():
    meminfo = {}

    with open("/proc/meminfo", "r") as f:
        for line in f:
            key, value = line.split(":")
            meminfo[key] = int(value.strip().split()[0])

    total_kb = meminfo["MemTotal"]
    available_kb = meminfo["MemAvailable"]
    used_kb = total_kb - available_kb

    return {
        "total_mb": round(total_kb / 1024, 2),
        "available_mb": round(available_kb / 1024, 2),
        "used_mb": round(used_kb / 1024, 2)
    }


# -------------------------------
# Snapshot Builder
# -------------------------------

def build_observation_snapshot():
    current_time = time.time()

    total_cpu, idle_cpu = read_cpu_times()
    memory_info = read_memory_info()

    return {
        "timestamp": current_time,
        "uptime_seconds": int(current_time - START_TIME),
        "cpu_total_time": total_cpu,
        "cpu_idle_time": idle_cpu,
        "load_average": read_load_average(),
        "memory": memory_info
    }


# -------------------------------
# Background Sampler
# -------------------------------

class BackgroundSampler:
    def __init__(self, interval_seconds=2):
        self.interval_seconds = interval_seconds
        self._running = False

    def start(self):
        if self._running:
            return

        self._running = True
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        while self._running:
            snapshot = build_observation_snapshot()
            observation_manager.add_snapshot(snapshot)
            time.sleep(self.interval_seconds)


# -------------------------------
# Flask Setup
# -------------------------------

app = Flask(__name__)

START_TIME = time.time()

observation_manager = ObservationManager()

background_sampler = BackgroundSampler(interval_seconds=2)
background_sampler.start()


# -------------------------------
# Routes
# -------------------------------

@app.route("/")
def hello_world():
    return "Hello from Cloud Run! System check complete."


@app.route("/analyze")
def analyze_system():

    snapshot = build_observation_snapshot()
    observation_manager.add_snapshot(snapshot)

    history = observation_manager.get_recent_history()

    # ---- CPU Usage Calculation ----
    cpu_usage_percent = 0

    if len(history) >= 3:
        prev = history[-3]
        curr = history[-1]

        total_diff = curr["cpu_total_time"] - prev["cpu_total_time"]
        idle_diff = curr["cpu_idle_time"] - prev["cpu_idle_time"]

        if total_diff > 0:
            cpu_usage_percent = 100 * (1 - idle_diff / total_diff)


    # cpu_count = os.cpu_count()
    cpu_count = os.cpu_count() or 1


    cpu_utilization_ratio = cpu_usage_percent / (cpu_count * 100)


    # ---- Memory Usage Calculation ----
    memory = snapshot["memory"]

    memory_usage_percent = (
        memory["used_mb"] / memory["total_mb"]
    ) * 100


    memory_headroom_percent = (
        memory["available_mb"] / memory["total_mb"]
    ) * 100


    # ---- Health Score ----
    average_load = (cpu_usage_percent + memory_usage_percent) / 2
    health_score = max(0, 100 - average_load)

    # ---- Message ----
    if health_score > 80:
        message = "System is healthy with stable resource availability."
    elif health_score > 50:
        message = "System is under moderate load. Resources are still within safe limits."
    else:
        message = "System is under high stress. Resource pressure detected."


    current_time = time.time()

    return jsonify({
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(current_time)),
        "uptime_seconds": int(current_time - START_TIME),

        "cpu_metric": {
            "signals": {
                "current_usage_percent": round(cpu_usage_percent, 2),
                "load_average": snapshot["load_average"]
            },
            "capacity": {
                "allocated_vcpus": cpu_count,
                "utilization_ratio": round(cpu_utilization_ratio, 4)
            }
        },

        "memory_metric": {
            "signals": memory,
            "capacity": {
                "headroom_percent": round(memory_headroom_percent, 2)
            }
        },

        "health_score": round(health_score, 2),
        "message": message
    })



# -------------------------------
# Local Run
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
