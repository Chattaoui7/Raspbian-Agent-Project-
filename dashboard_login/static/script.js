const inptCoords = [34.020882, -6.841650]; // Approximate location of INPT
const map = L.map('map').setView(inptCoords, 17);

// Load the tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Initialize marker and polyline path
let path = [inptCoords];
const polyline = L.polyline(path, { color: 'lime' }).addTo(map);
let marker = L.marker(inptCoords).addTo(map);

// Function to generate a small random lat/lng offset
function getRandomNearbyCoord(coord, maxOffset = 0.0003) {
  const latOffset = (Math.random() - 0.5) * 2 * maxOffset;
  const lngOffset = (Math.random() - 0.5) * 2 * maxOffset;
  return [coord[0] + latOffset, coord[1] + lngOffset];
}

// Update the position every 1 second
setInterval(() => {
  const newCoord = getRandomNearbyCoord(path[path.length - 1]);
  path.push(newCoord);

  polyline.setLatLngs(path);
  marker.setLatLng(newCoord);
}, 1000);
const batteryCtx = document.getElementById('batteryChart').getContext('2d');
const altitudeCtx = document.getElementById('altitudeChart').getContext('2d');

// Initial values
let batteryLevel = 92;
let altitude = 140;
let timeIndex = 4;

// Get current time in HH:MM format
function getCurrentTimeLabel() {
  const now = new Date();
  return now.getHours().toString().padStart(2, '0') + ':' +
         now.getMinutes().toString().padStart(2, '0');
}

// Battery chart setup
const batteryChart = new Chart(batteryCtx, {
  type: 'line',
  data: {
    labels: ['12:00', '12:01', '12:02', '12:03'],
    datasets: [{
      label: 'Battery %',
      data: [98, 96, 94, 92],
      borderColor: '#4ade80',
      backgroundColor: 'transparent',
      tension: 0.4
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      x: { ticks: { color: '#ccc' } },
      y: { ticks: { color: '#ccc' }, min: 0, max: 100 }
    }
  }
});

// Altitude chart setup
const altitudeChart = new Chart(altitudeCtx, {
  type: 'line',
  data: {
    labels: ['12:00', '12:01', '12:02', '12:03'],
    datasets: [{
      label: 'Altitude (m)',
      data: [120, 130, 135, 140],
      borderColor: '#60a5fa',
      backgroundColor: 'transparent',
      tension: 0.4
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      x: { ticks: { color: '#ccc' } },
      y: { ticks: { color: '#ccc' }, beginAtZero: true }
    }
  }
});

// Update function
setInterval(() => {
  const timeLabel = getCurrentTimeLabel();

  // Simulate slow battery drain
  batteryLevel = Math.max(batteryLevel - 0.2, 0);
  batteryChart.data.labels.push(timeLabel);
  batteryChart.data.datasets[0].data.push(parseFloat(batteryLevel.toFixed(1)));

  // Simulate random altitude change
  altitude += Math.floor(Math.random() * 10 - 5);
  altitudeChart.data.labels.push(timeLabel);
  altitudeChart.data.datasets[0].data.push(altitude);

  // Keep last 10 points to avoid overflow
  if (batteryChart.data.labels.length > 10) {
    batteryChart.data.labels.shift();
    batteryChart.data.datasets[0].data.shift();
  }
  if (altitudeChart.data.labels.length > 10) {
    altitudeChart.data.labels.shift();
    altitudeChart.data.datasets[0].data.shift();
  }

  // Update charts
  batteryChart.update();
  altitudeChart.update();
}, 2000); // Updates every 2 seconds
 const cpuTempSpan = document.getElementById("cpu-temp");
  const socket = new WebSocket("ws://localhost:8500");

  socket.onopen = () => {
    console.log("WebSocket connection established.");
  };

  socket.onmessage = (event) => {
    console.log("Received temperature:", event.data);
    cpuTempSpan.textContent = event.data + " °C";
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
    cpuTempSpan.textContent = "Error";
  };

  socket.onclose = () => {
    console.warn("WebSocket closed.");
    cpuTempSpan.textContent = "Disconnected";
  };
