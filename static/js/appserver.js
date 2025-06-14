// DOMContentLoaded 确保代码在DOM加载后运行
document.addEventListener("DOMContentLoaded", () => {

    // 数字人模型
    // const cubism4Model = "./live2d/Hiyori/Hiyori.model3.json";
    const cubism4Model = "./live2d/cutegirl/cutegirl.model3.json";

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

        window.model4 = models[0];
        console.log(innerWidth)
        // model4.x = innerWidth / 2;
        // 居中显示
        window.model4.x = (innerWidth - window.model4.width) / 2;

        window.model4.on("hit", (hitAreas) => {
            if (hitAreas.includes("Body")) {
                window.model4.motion("Tap");
            }

            if (hitAreas.includes("Head")) {
                window.model4.expression();
            }
        });


        $("#play").click(function () {
            window.talk(window.model4, "audio/demo.mp3");
        });

        let audioModeEnabled = false; // 是否处于音频模式（按钮变绿）
        let isRecording = false; // 录音状态

        // 轮询等待 audio 文件生成，      语音聊天的主要功能逻辑
        let lastAudioUrl = null; // 防止重复播放
        let pollingTimer = null;

        function waitForAudioAndPlay() {
          if (pollingTimer) {
            clearInterval(pollingTimer);
            pollingTimer = null;
          }
          
          console.log("🔄 开始轮询 /latest_audio...");
          let attempts = 0;
          pollingTimer = setInterval(() => {
            attempts++;
            axios.get("http://127.0.0.1:5000/latest_audio")
              .then(response => {
                console.log("✅ 轮询响应:", response.data);
                if (response.data.audio_file) {
                  clearInterval(pollingTimer);
                  pollingTimer = null;
                  console.log("🎧 获取到音频文件:", response.data.audio_file);
                  playModelAudio(response.data.audio_file);
                }
              })
              .catch(err => {
                if (attempts > 10) {
                  clearInterval(pollingTimer);
                  pollingTimer = null;
                  console.error("⛔ 音频轮询失败:", err);
                }
              });
          }, 2000);
        }
        



        // 文本模式下监听回车键输入
        document.getElementById('text').addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                document.getElementById('start').click(); // 触发点击事件

                // 这里可以添加其他逻辑，比如清除文本框内容
                document.getElementById('text').value = ''; // 清除文本框内容
            }

        });

        // 文本模式的实现
        let audio = new Audio();
        document.getElementById('start').addEventListener('click', function() {
            const text = document.getElementById('text').value.trim();
            if (!text) {
                alert("请输入内容");
                return;
            }
            $("#start").prop("disabled", true); // 防止多次点击

            axios.post('http://127.0.0.1:5000/text', {
                text: text
            })
            .then(response => {
                const audioUrl = response.data.audio_file + `?t=${Date.now()}`;
                console.log("音频文件路径:", audioUrl);

                // 播放音频
                talk(model4, audioUrl); // 播放音频并绑定动作
                model4.motion("Tap");   // 触发自定义动作

                // 设置音频源并播放， 会导致重复播放
                // audio.src = audioUrl;
                // audio.oncanplay = () => {
                //     audio.play().catch(error => console.error('播放音频失败:', error));
                // };

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
        
        console.log("模型是否 ready:", model4 && model4.motionManager);

        function playModelAudio(url) {
        const audio = new Audio(url);
        audio.crossOrigin = "anonymous";

        audio.oncanplay = () => {
            console.log("🎶 开始播放音频");
            audio.play().catch(err => {
                console.error("播放失败，可能是未触发用户事件：", err);
            });
        };

        audio.onerror = () => {
            console.error("音频加载失败");
        };

        // 可以绑定 Live2D 动作
        if (window.model4) {
            model4.motion("Tap");
        }
    }


        // 点击录音识别按钮
        document.getElementById('start-recognize').addEventListener('click', function () {
            // 👇 添加空播放做初始化授权
            const testAudio = new Audio();
            testAudio.play().catch(() => {}); // 确保 Chrome/Safari 获得自动播放授权
                    
            isRecording = !isRecording;
            this.style.backgroundColor = isRecording ? '#4CAF50' : '';
            this.textContent = isRecording ? 'Stop voice recognition' : 'Start voice recognition';  // 切换按钮文本： this.textContent ：获取按钮文本

            const url = isRecording ? 'http://127.0.0.1:5000/start_record' : 'http://127.0.0.1:5000/stop_record';

            axios.post(url)  // 发送 POST 请求
                .then(response => {
                    // 控制按钮状态（开始/停止播放（能正常））
                    // const audio = new Audio();
                    // audio.src = "http://127.0.0.1:5000/audio/output.mp3?t=" + Date.now();

                    // audio.oncanplay = () => {
                    //     console.log("音频加载完成，开始播放");
                    //     audio.play().catch(err => console.error("播放失败：", err));
                    // };

                    if (!isRecording && response.data.status === 'stopped') {
                        // const audioUrl = response.data.audio_file + `?t=${Date.now()}`;
                        // console.log("音频文件路径:", audioUrl);

                        // // 播放音频
                        // talk(model4, audioUrl); // 播放音频并绑定动作
                        
                        waitForAudioAndPlay();  // ✅ 真正的播放由轮询来负责
                        model4.motion("Tap");   // 触发自定义动作

                        // audio.src = audioUrl;
                        // audio.oncanplay = () => {
                        //     audio.play().catch(error => console.error('播放音频失败:', error));
                        // };

                        audio.onerror = () => {
                            console.error('音频加载失败');
                        };
                    }
                })
                .catch(error => {
                    console.error("控制失败:", error);
                    this.style.backgroundColor = '';
                    this.textContent = 'Start voice recognition';
                    isRecording = false;
                });
        });

    })();


    window.talk = function(model, audio) {
        var audio_link = audio;  //[Optional arg, can be null or empty] [relative or full url path] [mp3 or wav file] "./Keira.wav"
        var volume = 1; // [Optional arg, can be null or empty] [0.0 - 1.0]
        var expression = 8; // [Optional arg, can be null or empty] [index|name of expression]
        var resetExpression = true; // [Optional arg, can be null or empty] [true|false] [default: true] [if true, expression will be reset to default after animation is over]
        var crossOrigin = "anonymous"; // [Optional arg, to use not same-origin audios] [DEFAULT: null]

        model.speak(audio_link, {
            volume: 1,
            expression: 8,
            resetExpression: true,
            crossOrigin: "anonymous"
        })

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

