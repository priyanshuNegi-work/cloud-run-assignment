async function fetchSystemData() {
    try {
        const response = await fetch('/analyze');
        if (!response.ok) throw new Error('Network error');
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error(error);
        const status = document.getElementById('connection-status');
        status.innerHTML = "● Offline";
        status.style.color = "#f38ba8";
        status.style.background = "rgba(243, 139, 168, 0.1)";
    }
}

// Helper: Get color based on percentage/score
function getColor(value, isScore = false) {
    // For Score: Higher is better. For Usage: Lower is better.
    let good = isScore ? value > 80 : value < 50;
    let medium = isScore ? value > 50 : value < 80;

    if (good) return "#a6e3a1"; // Green
    if (medium) return "#f9e2af"; // Yellow
    return "#f38ba8"; // Red
}

function updateDashboard(data) {
    // 1. Header
    document.getElementById('timestamp').innerText = data.timestamp;
    document.getElementById('uptime').innerText = data.uptime_seconds;
    
    const status = document.getElementById('connection-status');
    status.innerHTML = "● Live";
    status.style.color = "#a6e3a1";
    status.style.background = "rgba(166, 227, 161, 0.1)";

    // 2. Health Score & Message
    const score = data.health_score;
    const scoreEl = document.getElementById('health-score');
    const circle = document.getElementById('score-circle');
    const msgEl = document.getElementById('status-message');

    scoreEl.innerText = score;
    msgEl.innerText = data.message;

    const themeColor = getColor(score, true);
    circle.style.borderColor = themeColor;
    circle.style.color = themeColor;
    msgEl.style.color = themeColor;

    // 3. CPU
    const cpu = data.cpu_metric;
    const cpuUsage = cpu.signals.current_usage_percent;
    document.getElementById('cpu-usage').innerText = cpuUsage + "%";
    
    const cpuBar = document.getElementById('cpu-bar');
    cpuBar.style.width = cpuUsage + "%";
    cpuBar.style.backgroundColor = getColor(cpuUsage, false); // Dynamic Color!

    document.getElementById('load-1m').innerText = cpu.signals.load_average.last_1_min;
    document.getElementById('load-5m').innerText = cpu.signals.load_average.last_5_min;
    document.getElementById('cpu-cores').innerText = cpu.capacity.allocated_vcpus;
    document.getElementById('cpu-ratio').innerText = cpu.capacity.utilization_ratio;

    // 4. Memory
    const mem = data.memory_metric;
    document.getElementById('mem-used').innerText = mem.signals.used_mb;
    document.getElementById('mem-total').innerText = mem.signals.total_mb;
    document.getElementById('mem-available').innerText = mem.signals.available_mb;
    document.getElementById('mem-headroom').innerText = mem.capacity.headroom_percent + "%";

    const memPercent = (mem.signals.used_mb / mem.signals.total_mb) * 100;
    const memBar = document.getElementById('mem-bar');
    memBar.style.width = memPercent + "%";
    memBar.style.backgroundColor = getColor(memPercent, false); // Dynamic Color!
}

setInterval(fetchSystemData, 2000);
fetchSystemData();