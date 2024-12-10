const recordBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const transcript = document.getElementById('result');
const loading = document.getElementById('loading');

let recorder;
let audioChunks = [];

// 녹음 시작
recordBtn.addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            recorder = new MediaRecorder(stream);
            audioChunks = [];
            recorder.ondataavailable = e => audioChunks.push(e.data);
            recorder.start();

            recordBtn.disabled = true;
            stopBtn.disabled = false;
            loading.style.display = 'block';
        });
        
});

// 녹음 종료
stopBtn.addEventListener('click', async () => {
    if (recorder && recorder.state !== 'inactive') {
        recorder.stop();
        recorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            const formData = new FormData();
            formData.append('audio', audioBlob);

            try {
                const response = await fetch('/speech-to-text', {
                    method: 'POST',
                    body: formData,
                });

                const data = await response.json();
                transcript.textContent = data.text
                    ? `인식된 텍스트: ${data.text}`
                    : `오류: ${data.error}`;
            } catch (error) {
                transcript.textContent = "서버와 통신 중 문제가 발생했습니다.";
            } finally {
                loading.style.display = 'none';
                recordBtn.disabled = false;
                stopBtn.disabled = true;
            }
        };
    }
});
