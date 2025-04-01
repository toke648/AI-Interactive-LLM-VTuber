document.addEventListener('DOMContentLoaded', function() {
    const recordButton = document.getElementById('record');
    const stopButton = document.getElementById('stop');
    let mediaRecorder;
    let audioChunks = [];

    recordButton.addEventListener('click', async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('audio', audioBlob, 'recording.wav');

                // 使用axios发送POST请求
                axios.post('/api/upload-audio', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then(function (response) {
                    console.log('Success:', response.data);
                })
                .catch(function (error) {
                    console.error('Error:', error);
                });

                audioChunks = [];
            };

            mediaRecorder.start();
            recordButton.disabled = true;
            stopButton.disabled = false;
        } catch (err) {
            console.error('Error accessing microphone:', err);
        }
    });

    stopButton.addEventListener('click', () => {
        mediaRecorder.stop();
        recordButton.disabled = false;
        stopButton.disabled = true;
    });
});
