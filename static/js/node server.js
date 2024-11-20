app.get('/dealAudio', async (req, res) => {
    const { text, voice, file_name } = req.query;

    try {
        await generateAudio(text, voice, file_name); // 确保音频生成完成
        const filePath = `output_directory/${file_name}`;
        res.json({ audio_file: filePath });
    } catch (error) {
        console.error("音频生成失败:", error);
        res.status(500).json({ error: "音频生成失败" });
    }
});

document.getElementById("start").addEventListener("click", function() {
    let text = document.getElementById("text").value.trim();
    if (text === "") {
        alert("请输入内容");
        return;
    }

    axios.get("http://127.0.0.1:2020/dealAudio", {
        params: {
            text: text,
            voice: "zh-CN-XiaoxiaoNeural",
            file_name: "test.mp3"
        }
    })
    .then(response => {
        const audioUrl = response.data.audio_file + "?v=" + new Date().getTime();
        const audio = new Audio(audioUrl);
        audio.play();
    })
    .catch(error => {
        console.error('请求接口失败:', error);
    });
});