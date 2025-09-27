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
            unlockAudioPlayback();
            window.talk(window.model4, "audio/demo.mp3");
        });

        let audioModeEnabled = false; // 是否处于音频模式（按钮变绿）
        let isRecording = false; // 录音状态
        let audioUnlocked = false; // 是否已解锁自动播放
        let audioContext = null;   // WebAudio 解锁用

        // 通过一次用户手势同时解锁 HTMLAudio 与 WebAudio
        function unlockAudioPlayback() {
            if (audioUnlocked) return;
            try {
                // 1) 解锁 HTMLAudio：播放一段静音音频后立即暂停
                const silent = new Audio('data:audio/mp3;base64,//uQZAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAACcQACcQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');
                silent.muted = true;
                const p1 = silent.play().then(() => { try { silent.pause(); } catch (e) {} }).catch(() => {});

                // 2) 解锁 WebAudio：resume 并播放 1 帧静音 Buffer
                if (!audioContext) {
                    audioContext = new (window.AudioContext || window.webkitAudioContext)();
                }
                const p2 = audioContext.resume().then(() => {
                    const buffer = audioContext.createBuffer(1, 1, audioContext.sampleRate);
                    const source = audioContext.createBufferSource();
                    source.buffer = buffer;
                    source.connect(audioContext.destination);
                    try { source.start(0); } catch (e) {}
                }).catch(() => {});

                Promise.allSettled([p1, p2]).then(() => {
                    audioUnlocked = true;
                    console.log('🔓 Audio autoplay unlocked (HTMLAudio & WebAudio)');
                });
            } catch (e) {}
        }

        // 任意一次交互即尝试解锁
        document.addEventListener('click', unlockAudioPlayback, { once: true });
        document.addEventListener('pointerdown', unlockAudioPlayback, { once: true });
        document.addEventListener('touchstart', unlockAudioPlayback, { once: true });

        // 应用页面背景（优先使用本地缓存，其次拉取设置），并监听跨页更新
        function applyBgFromObject(path) {
            const type = (path && path.background_type) || 'color';
            if (type === 'image' && path && path.background_image) {
                document.body.style.background = `url(${path.background_image}) center/cover no-repeat fixed`;
            } else if (path && path.background_color) {
                document.body.style.background = path.background_color;
            }
        }
        async function applyBackgroundFromSettings() {
            try {
                // 1) 本地缓存优先（由 settings.html 保存时写入）
                const cached = localStorage.getItem('vtuber_bg');
                if (cached) {
                    try { applyBgFromObject(JSON.parse(cached)); } catch(e) {}
                }
                // 2) 拉取服务端配置兜底
                const resp = await fetch('/settings');
                const cfg = await resp.json();
                applyBgFromObject((cfg && cfg.path) || {});
            } catch (e) {
                console.warn('背景设置加载失败:', e);
            }
        }
        applyBackgroundFromSettings();
        // 3) 跨页监听：settings.html 保存后通过 localStorage 通知本页立即更新
        window.addEventListener('storage', (ev) => {
            if (ev.key === 'vtuber_bg' && ev.newValue) {
                try { applyBgFromObject(JSON.parse(ev.newValue)); } catch(e) {}
            }
        });

        // ================= MCP UI：状态查询与启停 =================
        async function refreshMcpStatus() {
            try {
                const resp = await fetch('/mcp/status');
                const data = await resp.json();
                const btn = document.getElementById('mcp-toggle');
                if (!btn) return;
                if (data.running) {
                    btn.textContent = 'MCP: 运行中（点击停止）';
                    btn.dataset.running = '1';
                } else {
                    btn.textContent = 'MCP: 未运行（点击启动）';
                    btn.dataset.running = '0';
                }
            } catch(e) {
                const btn = document.getElementById('mcp-toggle');
                if (btn) btn.textContent = 'MCP: 状态获取失败';
            }
        }
        async function toggleMcp() {
            const btn = document.getElementById('mcp-toggle');
            if (!btn) return;
            const running = btn.dataset.running === '1';
            btn.disabled = true;
            try {
                const resp = await fetch(running ? '/mcp/stop' : '/mcp/start', { method: 'POST' });
                await resp.json();
            } catch(e) {}
            await refreshMcpStatus();
            btn.disabled = false;
        }
        const mcpBtn = document.getElementById('mcp-toggle');
        if (mcpBtn) {
            mcpBtn.addEventListener('click', toggleMcp);
            refreshMcpStatus();
        }

        // 轮询等待 audio 文件生成，      语音聊天的主要功能逻辑
        let lastAudioUrl = null; // 防止重复播放
        let pollingTimer = null;
        const historyList = document.getElementById('history-list');
        let histories = [];
        const thinking = document.getElementById('thinking');
        let currentPlayToken = 0; // 播放令牌，避免播放旧音频

        try {
            const saved = localStorage.getItem('vtuber_histories');
            if (saved) histories = JSON.parse(saved) || [];
        } catch (e) {}
        renderHistory();

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
                  const u = response.data.audio_file.startsWith('http') ? response.data.audio_file : (`http://127.0.0.1:5000` + response.data.audio_file);
                  const playToken = ++currentPlayToken;
                  const finalUrl = u + `?t=${Date.now()}`;
                  // 仅播放当前令牌对应的音频
                  if (playToken === currentPlayToken) {
                    if (window.model4) {
                      model4.motion("Tap");
                      window.talk(window.model4, finalUrl);
                    } else {
                      playModelAudio(finalUrl);
                    }
                  }
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
        // 轮询最近一次ASR文本，拿到后自动填充输入框并触发发送
        function pollAsrAndAutoSend() {
          let attempts = 0;
          const timer = setInterval(() => {
            attempts++;
            axios.get('http://127.0.0.1:5000/latest_asr')
              .then(resp => {
                if (resp.data && resp.data.text) {
                  clearInterval(timer);
                  const inputEl = document.getElementById('text');
                  if (inputEl) inputEl.value = resp.data.text;
                  document.getElementById('start').click();
                }
              })
              .catch(() => {
                if (attempts > 10) {
                  clearInterval(timer);
                }
              });
          }, 1000);
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

        // 文本模式的实现（发送按钮）
        let audio = new Audio();
        document.getElementById('start').addEventListener('click', function() {
            // 先尝试解锁自动播放
            unlockAudioPlayback();
            const text = document.getElementById('text').value.trim();
            if (!text) {
                alert("请输入内容");
                return;
            }
            $("#start").prop("disabled", true); // 防止多次点击
            const playToken = ++currentPlayToken;
            toggleThinking(true);
            toggleSendLoading(true);

            axios.post('http://127.0.0.1:5000/text', {
                text: text
            })
            .then(response => {
                const audioUrl = (response.data.audio_file.startsWith('http') ? response.data.audio_file : (`http://127.0.0.1:5000` + response.data.audio_file)) + `?t=${Date.now()}`;
                console.log("音频文件路径:", audioUrl);

                // 仅当令牌未过期时播放
                if (playToken === currentPlayToken) {
                    if (window.model4) {
                        model4.motion("Tap");
                        window.talk(window.model4, audioUrl);
                    } else {
                        playModelAudio(audioUrl);
                    }
                }

                // 写入历史并渲染
                histories.push({ role: 'user', content: text });
                const aiText = response.data.text || '';
                histories.push({ role: 'assistant', content: '' });
                renderHistory();
                saveHistories(); // 保存到 localStorage
                // 将最新一条AI内容做打字机式流式显示
                typewriterUpdateLast(aiText, 105); // 打字机效果：逐字更新最后一条AI消息，1为速度，越大越快

                // 设置音频源并播放， 会导致重复播放
                // audio.src = audioUrl;
                // audio.oncanplay = () => {
                //     audio.play().catch(error => console.error('播放音频失败:', error));
                // };

                audio.onerror = () => {
                    console.error('音频加载失败');
                };

                $("#start").prop("disabled", false); // 恢复按钮状态
                toggleThinking(false);
                toggleSendLoading(false);
            })
            .catch(error => {
                console.error('接口请求失败:', error);
                $("#start").prop("disabled", false);
                toggleThinking(false);
                toggleSendLoading(false);
            });
        });
        
        console.log("模型是否 ready:", model4 && model4.motionManager);

        // 播放器：使用原生 Audio 播放（在无模型时使用）
        function playModelAudio(url) {
        const finalUrl = url.startsWith('http') ? url : (`http://127.0.0.1:5000` + url);
        const audio = new Audio();
        audio.crossOrigin = "anonymous";
        audio.muted = false;
        audio.volume = 1.0;
        audio.src = finalUrl + `?t=${Date.now()}`;

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

        // 保存历史记录到 localStorage
        function saveHistories() {
            try {
                localStorage.setItem('vtuber_histories', JSON.stringify(histories));
            } catch (e) {
                console.error('保存历史记录失败:', e);
            }
        }

        // 清除历史记录
        function clearHistories() {
            histories = [];
            localStorage.removeItem('vtuber_histories');
            renderHistory();
        }

        // 左侧历史列表渲染
        function renderHistory() {
            if (!historyList) return;
            historyList.innerHTML = '';
            histories.slice(-100).forEach((item, idx) => {
                const div = document.createElement('div');
                div.className = 'history-item';
                div.textContent = (item.role === 'user' ? '你: ' : 'AI: ') + (item.content || '');
                historyList.appendChild(div);
            });
        }
        // 打字机效果：逐字更新最后一条AI消息
        function typewriterUpdateLast(fullText, intervalMs) {
            const startIndex = histories.length - 1;
            if (startIndex < 0 || histories[startIndex].role !== 'assistant') return;
            let i = 0;
            const timer = setInterval(() => {
                if (i > fullText.length) { 
                    clearInterval(timer); 
                    saveHistories(); // 打字机效果完成后保存
                    return; 
                }
                histories[startIndex].content = fullText.slice(0, i);
                renderHistory();
                i++;
            }, Math.max(8, intervalMs || 12));
        }
        function toggleThinking(show) {
            const el = document.getElementById('thinking');
            if (!el) return;
            el.style.display = show ? 'inline-flex' : 'none';
        }
        function toggleSendLoading(loading) {
            const sendBtn = document.getElementById('start');
            if (!sendBtn) return;
            sendBtn.classList.toggle('loading', loading);
            sendBtn.disabled = !!loading;
        }


        // GPT风格麦克风按钮：切换录音
        const micBtn = document.getElementById('mic-btn');
        if (micBtn) {
            micBtn.addEventListener('click', function() {
                // 视觉切换
                this.classList.toggle('active');
                // 触发原有开始/停止逻辑
                document.getElementById('start-recognize').click();
            });
        }

        // 清除历史记录按钮
        const clearHistoryBtn = document.getElementById('clear-history');
        if (clearHistoryBtn) {
            clearHistoryBtn.addEventListener('click', function() {
                if (confirm('确定要清除所有历史记录吗？')) {
                    clearHistories();
                }
            });
        }

        // 点击录音识别按钮（原按钮继续保留，供 JS 触发）
        document.getElementById('start-recognize').addEventListener('click', function () {
            // 解锁浏览器自动播放（HTMLAudio + WebAudio）
            unlockAudioPlayback();
                    
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
                        // 停止后改为轮询ASR文本，拿到后自动填充并发送
                        pollAsrAndAutoSend();
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

