const video = document.getElementById('video');
const video1 = document.getElementById('video1');

const ws = new WebSocket('ws://localhost:8000/web');

ws.onmessage = function(event) {
      const blob = new Blob([event.data], { type: 'image/jpeg' });
      const img = new Image();
      mg.onload = function() {
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        URL.revokeObjectURL(img.src); // Cleanup memory
      };
      video.src = URL.createObjectURL(blob);
    };
ws.onopen = function() {
      console.log("WebSocket connection opened");
    };

const web = new WebSocket('ws://localhost:8000/web1')
    
web.onmessage = function(event) {
      const blob = new Blob([event.data], { type: 'image/jpeg' });
      const img = new Image();
      mg.onload = function() {
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        URL.revokeObjectURL(img.src); // Cleanup memory
      };
      video1.src = URL.createObjectURL(blob);
    };

web.onclose = function() {
      console.log("WebSocket connection closed");
    };