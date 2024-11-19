// DOMContentLoaded 确保代码在DOM加载后运行
document.addEventListener("DOMContentLoaded", () => {
    // 数字人模型
    // const cubism4Model = "./assets/kei_vowels_pro/kei_vowels_pro.model3.json";
    const cubism4Model = "./assets/Hiyori/Hiyori.model3.json";
    // const cubism4Model = "./assets/March 7th/March 7th.model3.json";
    // const cubism4Model = "./assets/haru/haru_greeter_t03.model3.json";
    // const cubism4Model = "./assets/ariu/ariu.model3.json";
    // const cubism4Model = "./assets/mianfeimox/llny.model3.json";
    // const cubism4Model = "./assets/草莓兔兔 试用/草莓兔兔  试用.model3.json"
    const live2d = PIXI.live2d;
    (async function main() {
        const app = new PIXI.Application({
            view: document.getElementById("canvas"),
            autoStart: true,
            resizeTo: window,
            backgroundColor: 0x333333
        });

        const models = await Promise.all([
            live2d.Live2DModel.from(cubism4Model)
        ]);

        models.forEach((model) => {
            app.stage.addChild(model);

            const scaleX = (innerWidth) / model.width;
            const scaleY = (innerHeight) / model.height;

            // fit the window
            model.scale.set(Math.min(scaleX, scaleY));
            model.y = innerHeight * 0.1;
            draggable(model);
        });

        const model4 = models[0];
        console.log(innerWidth)
        // model4.x = innerWidth / 2;
        // 居中显示
        model4.x = (innerWidth - model4.width) / 2;

        model4.on("hit", (hitAreas) => {
            if (hitAreas.includes("Body")) {
                model4.motion("Tap");
            }

            if (hitAreas.includes("Head")) {
                model4.expression();
            }
        });


        $("#play").click(function () {
            talk(model4, "audio/demo.mp3");
        });

        $("#start").click(function () {
            let text = $("#text").val().trim();
            if (text === "") {
                alert("请输入内容");
                return false;
            }
            $("#start").prop("disabled", true); // 防止多次点击

            axios.get(`http://127.0.0.1:2020/dealAudio?file_name=output.mp3&voice=zh-CN-XiaoxiaoNeural&text=${encodeURIComponent(text)}&timestamp=${Date.now()}`)
                .then(response => {
                    const audioUrl = response.data.audio_file + `?t=${Date.now()}`;
                    console.log("音频文件路径:", audioUrl);

                    talk(model4, audioUrl); // 播放音频并绑定动作
                    model4.motion("Tap");   // 触发自定义动作

                    audio.oncanplay = () => { // 确保音频可播放后再触发
                        audio.play().catch(error => console.error('播放音频失败:', error));
                    };

                    audio.onerror = () => {
                        console.error('音频加载失败');
                    };

                    $("#start").prop("disabled", false); // 恢复按钮状态
                })
                .catch(error => {
                    console.error('接口请求失败:', error);
                    $("#start").prop("disabled", false);
                });
        });


    })();


    function talk(model, audio) {
        var audio_link = audio;  //[Optional arg, can be null or empty] [relative or full url path] [mp3 or wav file] "./Keira.wav"
        var volume = 1; // [Optional arg, can be null or empty] [0.0 - 1.0]
        var expression = 8; // [Optional arg, can be null or empty] [index|name of expression]
        var resetExpression = true; // [Optional arg, can be null or empty] [true|false] [default: true] [if true, expression will be reset to default after animation is over]
        var crossOrigin = "anonymous"; // [Optional arg, to use not same-origin audios] [DEFAULT: null]

        model.speak(audio_link, {
            volume: volume,
            expression: expression,
            resetExpression: resetExpression,
            crossOrigin: crossOrigin
        })
        model.speak(audio_link)
        model.speak(audio_link, {volume: volume})
        model.speak(audio_link, {expression: expression, resetExpression: resetExpression})

    }


    function draggable(model) {
        model.buttonMode = true;
        model.on("pointerdown", (e) => {
            model.dragging = true;
            model._pointerX = e.data.global.x - model.x;
            model._pointerY = e.data.global.y - model.y;
        });
        model.on("pointermove", (e) => {
            if (model.dragging) {
                model.position.x = e.data.global.x - model._pointerX;
                model.position.y = e.data.global.y - model._pointerY;
            }
        });
        model.on("pointerupoutside", () => (model.dragging = false));
        model.on("pointerup", () => (model.dragging = false));
    }

});

