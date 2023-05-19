document.getElementById('panLeft').addEventListener('click', function() {
    sendControlSignal('panLeft');
    console.log('pan left');
});

document.getElementById('panRight').addEventListener('click', function() {
    sendControlSignal('panRight');
    console.log('pan right');
});

document.getElementById('tiltUp').addEventListener('click', function() {
    sendControlSignal('tiltUp');
    console.log('tilt up');
});

document.getElementById('tiltDown').addEventListener('click', function() {
    sendControlSignal('tiltDown');
    console.log('tilt down');
});

document.getElementById('manualControl').addEventListener('click', function() {
    sendControlSignal('manualControl');
    console.log('manual control');
});

function sendControlSignal(command) {
    // Here you would send a request to your server-side code or API.
    // For example, using the Fetch API:
    /*
    fetch('/your-api-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command: command })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch((error) => {
        console.error('Error:', error);
    });
    */
    console.log(`Command sent: ${command}`);
}
