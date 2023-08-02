function playAudio() {
    var text = document.getElementById("output").textContent;
    fetch('/play-text', {
        method: 'POST',
        body: new URLSearchParams({
            text: text
        })
    })
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                console.error("Error initiating audio playback");
            }
        })
        .then(blob => {
            var audio = new Audio(URL.createObjectURL(blob));
            audio.play();
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
