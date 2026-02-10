import os
import time
import psutil  # <--- NEW: Tool to read system metrics
from flask import Flask, jsonify




# -------------------------------
# Observation Manager
# -------------------------------

class ObservationManager:
    def __init__(self, max_entries=50, max_age_seconds=600):
        """
        max_entries → Maximum number of stored snapshots
        max_age_seconds → Maximum age of snapshots (10 minutes default)
        """
        self.max_entries = max_entries
        self.max_age_seconds = max_age_seconds
        self.observations = []

    def add_snapshot(self, snapshot):
        """Add a new observation snapshot."""
        self.observations.append(snapshot)
        self._cleanup_old_entries()

    def get_recent_history(self):
        """Return stored observation history."""
        return self.observations

    def _cleanup_old_entries(self):
        """Maintain hybrid window: limit by count + time."""
        current_time = time.time()

        # Remove entries older than time window
        self.observations = [
            obs for obs in self.observations
            if current_time - obs["timestamp"] <= self.max_age_seconds
        ]

        # Limit number of entries
        if len(self.observations) > self.max_entries:
            self.observations = self.observations[-self.max_entries:]








# -------------------------------
# Snapshot Builder
# -------------------------------

def build_observation_snapshot():
    """Create a system observation snapshot."""

    current_time = time.time()

    snapshot = {
        "timestamp": current_time,
        "uptime_seconds": int(current_time - START_TIME),

        # Temporary signals (psutil still used for now)
        "cpu_usage_percent": psutil.cpu_percent(interval=0.1),

        "memory_usage_percent": psutil.virtual_memory().percent
    }

    return snapshot







app = Flask(__name__)

# Record the start time when the container boots up
START_TIME = time.time()


# Global observation manager instance
observation_manager = ObservationManager()


@app.route("/")
def hello_world():
    # Task 2 Requirement
    return "Hello from Cloud Run! System check complete."

@app.route("/analyze")
def analyze_system():
    
    # Build and store observation snapshot
    snapshot = build_observation_snapshot()
    observation_manager.add_snapshot(snapshot)

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
