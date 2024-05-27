// let mediaRecorder;
// let recordedChunks = [];

// document.getElementById('record-btn').addEventListener('click', function() {
//     navigator.mediaDevices.getUserMedia({ audio: true })
//     .then(stream => {
//         mediaRecorder = new MediaRecorder(stream);
//         mediaRecorder.start();

//         mediaRecorder.ondataavailable = function(e) {
//             recordedChunks.push(e.data);
//         };

//         document.getElementById('stop-btn').disabled = false;
//     })
//     .catch(err => {
//         console.log('Microphone access denied: ', err);
//         alert('Microphone access denied');
//     });
// });

// document.getElementById('stop-btn').addEventListener('click', function() {
//     mediaRecorder.stop();
//     document.getElementById('stop-btn').disabled = true;

//     let blob = new Blob(recordedChunks, {
//         type: 'audio/wav'
//     });

//     let formData = new FormData();
//     formData.append('audio_data', blob);
//     formData.append('audio_name', document.getElementById('audio_name').value);
//     formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

//     fetch('/process_audio', {
//         method: 'POST',
//         body: formData
//     });
// });

// recording audio
const mic_btn = document.querySelector('#mic');
const playback = document.querySelector('.playback');


mic_btn.addEventListener('click', ToggleMic);

let can_record = false;
let is_recording = false;

let recorder = null;

let chunks = [];

function SetupAudio() {
    console.log("setup")
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({
            audio: true
        })
            .then(SetupStream)
            .catch(err => {
                console.error(err)
            })
    }
}
SetupAudio();

function SetupStream(stream) {
    recorder = new MediaRecorder(stream);

    recorder.ondataavailable = e => {
        chunks.push(e.data);
    }

    recorder.onstop = e => {
        const blob = new Blob(chunks, { type: "audio/ogg; codecs=opus" });
        chunks = [];
        const audioURL = window.URL.createObjectURL(blob);
        playback.src = audioURL;
    }

    can_record = true;
}

function ToggleMic() {
    if (!can_record) return;

    is_recording = !is_recording;

    if (is_recording) {
        recorder.start();

    } else {
        recorder.stop();
    }

    const blob = new Blob(chunks, { type: "audio/ogg; codecs=opus" });
    chunks = [];

    let formData = new FormData();
    formData.append('audio_data', blob);

    // POST request to the Django view
    fetch('/process_audio', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => console.log(data.text))
        .catch(error => console.error('Error:', error));
}