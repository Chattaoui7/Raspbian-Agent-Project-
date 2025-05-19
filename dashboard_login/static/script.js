// Initialize Leaflet map
const map = L.map('map').setView([37.776, -122.416], 16);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
const path = [
  [37.7749, -122.4194],
  [37.775, -122.418],
  [37.7755, -122.417],
  [37.776, -122.416]
];
L.polyline(path, { color: 'lime' }).addTo(map);
L.marker(path[path.length - 1]).addTo(map);

// Battery chart
const batteryCtx = document.getElementById('batteryChart').getContext('2d');
new Chart(batteryCtx, {
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
      y: { ticks: { color: '#ccc' } }
    }
  }
});

// Altitude chart
const altitudeCtx = document.getElementById('altitudeChart').getContext('2d');
new Chart(altitudeCtx, {
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
      y: { ticks: { color: '#ccc' } }
    }
  }
});

