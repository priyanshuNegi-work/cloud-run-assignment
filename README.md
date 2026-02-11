# 🚀 Cloud Run System Monitor (Manual Kernel Reader)

A full-stack system monitoring dashboard deployed on **Google Cloud Run**. 
Unlike standard monitoring tools that rely on libraries like `psutil`, this project **manually reads the Linux Kernel's system files** (`/proc/`) to extract real-time metrics from the host machine.

---

## 🌟 Key Features

### 1. 🧠 Manual Kernel Discovery (No Libraries)
Instead of using high-level abstractions, this app reads raw system files directly:
* **CPU Load:** Parses `/proc/loadavg` to get 1m, 5m, and 15m load averages.
* **Memory Usage:** Parses `/proc/meminfo` to calculate "Real" Used vs. Available memory (handling Linux cache correctly).
* **CPU Stats:** Parses `/proc/stat` to calculate precise CPU usage percentages using delta ticks.

### 2. ⚡ Real-Time Dashboard
* **Frontend:** HTML5, CSS3 (Dark Mode), and Vanilla JavaScript.
* **Backend:** Flask API serving JSON data.
* **Live Updates:** The dashboard polls the `/analyze` endpoint every 2 seconds to update gauges and progress bars instantly.

### 3. 🏥 Custom Health Score Algorithm
A unique algorithm that calculates a **0-100 Health Score**:
* **Base Score:** 100
* **Penalties:**
    * **CPU Overload:** Penalizes if 1-minute load exceeds the CPU Core count.
    * **Memory Pressure:** Penalizes if RAM usage exceeds 75%.
* **Visual Feedback:** The UI changes color (Green 🟢 / Yellow 🟡 / Red 🔴) based on the score.

---

## 📂 Project Structure

```text
├── README.md               # Project documentation
├── sys_check.sh            # Helper script for system checks
└── deploy_app/             # Main Application Folder
    ├── Dockerfile          # Container build instructions
    ├── main.py             # Flask App (Backend & Manual Kernel Readers)
    ├── requirements.txt    # Python dependencies
    ├── log.txt             # Application logs (generated)
    ├── static/             # Frontend Assets
    │   ├── dashboard.js    # UI Logic (Fetch API & DOM updates)
    │   └── style.css       # Styling (Dark Mode)
    └── templates/          # HTML Templates
        └── index.html      # Dashboard Structure
```
---

## 🛠️ How to Run Locally

You can test the entire application on your local machine using Docker.

**1. Build the Image**

```bash
docker build -t system-monitor .
```

**2. Run the Container**

```bash
docker run -p 8080:8080 system-monitor
```

**3. Access the Dashboard**

#### Open your browser and visit: `http://localhost:8080`

---

## ☁️ Deployment (Google Cloud Run)

This project is optimized for Serverless deployment.

**1. Deploy Command**

```bash
gcloud run deploy priyanshu-negi --source . --region asia-south1 --allow-unauthenticated
```

**2. Output**

Google Cloud will provide a live URL (e.g., `https://priyanshu-negi-xyz.asia-south1.run.app`).

---

## 📡 API Reference

### `GET /analyze`

Returns the raw system metrics and health analysis.

**Response Example:**

```json
{
  "timestamp": "2026-02-11 05:30:00",
  "uptime_seconds": 120,
  "health_score": 98.5,
  "message": "System is healthy with stable resource availability.",
  "cpu_metric": {
    "signals": {
      "current_usage_percent": 12.5,
      "load_average": {
        "last_1_min": 0.45,
        "last_5_min": 0.30,
        "last_15_min": 0.15
      }
    },
    "capacity": {
      "allocated_vcpus": 2,
      "utilization_ratio": 0.125
    }
  },
  "memory_metric": {
    "signals": {
      "total_mb": 2048.0,
      "used_mb": 450.5,
      "available_mb": 1597.5
    },
    "capacity": {
      "headroom_percent": 78.0
    }
  }
}
```

---

## 🧠 Engineering Insights (Why read `/proc`?)

When running inside a **Docker Container**, standard tools often report the *Container's* limits, not the *Host's* reality.

By reading `/proc` files directly, we bypass the abstraction layer. This allows the application to:

1. See the **True CPU Load** of the underlying VM/Server.
2. Monitor the **Actual Memory Pressure** on the host node.
3. Provide accurate scaling metrics regardless of container quotas.


