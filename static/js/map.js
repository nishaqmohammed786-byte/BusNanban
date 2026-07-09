document.addEventListener("DOMContentLoaded", function () {
    // 1. Center map around the midpoints so the whole Kilambakkam-Guindy line fits beautifully
    var map = L.map('chennai-map').setView([12.95, 80.15], 11);

    // 2. Load and display map tiles from OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // 3. Exact geographic coordinates along the GST Road transit corridor
    var stopKilambakkam = [12.8614, 80.0782];   // Main Terminus (KCBT)
    var stopPerungalathur = [12.9038, 80.1011]; // Connecting Hub
    var stopTambaram = [12.9249, 80.1167];      // Major Transit Station
    var stopChromepet = [12.9516, 80.1408];     // Intermediate Stop
    var stopAirport = [12.9807, 80.1638];       // Meenambakkam Airport
    var stopGuindy = [13.0090, 80.2131];        // Destination Terminal

    // 4. Set accurate terminal markers with flat, bulletproof chaining syntax
    L.marker(stopKilambakkam).addTo(map).bindPopup('<b>Main Terminus:</b> Kilambakkam (KCBT)');
    L.marker(stopGuindy).addTo(map).bindPopup('<b>Destination:</b> Guindy MTC Bus Stop');

    // 5. Array of coordinates mapping the true path of the highway
    var modernBusRoutePath = [
        stopKilambakkam,
        stopPerungalathur,
        stopTambaram,
        stopChromepet,
        stopAirport,
        stopGuindy
    ];

    // 6. Draw the bright blue routing track line
    var polyline = L.polyline(modernBusRoutePath, {
        color: '#3b82f6',
        weight: 6,
        opacity: 0.85,
        lineJoin: 'round'
    }).addTo(map);

    // 7. Auto-adjust viewport frame to frame the entire route line cleanly
    map.fitBounds(polyline.getBounds());
});