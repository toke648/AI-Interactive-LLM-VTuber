""" utf-8 encoding audio_record.py """
import speech_recognition as sr
from typing import Optional

class SpeechRecognizer:
    """语音识别类"""
    def __init__(self,
                 energy_threshold: int = 300,
                 pause_threshold: float = 0.6,
                 timeout_seconds: float = 2.0,
                 phrase_time_limit: float = 6.0,
                 device_index: Optional[int] = None,
                 language: str = 'zh-CN'):
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = pause_threshold
        self.timeout_seconds = timeout_seconds
        self.phrase_time_limit = phrase_time_limit
        self.device_index = device_index
        self.language = language

    def record(self,
               recognizer: Optional[sr.Recognizer] = None,
               language: Optional[str] = None
               ) -> Optional[str]:

        # 如果识别器不为空，则使用识别器，否则使用默认识别器
        r = recognizer or self.recognizer
        lang = language or self.language
        mic_kwargs = {}

        # 如果设备索引不为空，则设置设备索引
        if self.device_index is not None:
            mic_kwargs['device_index'] = self.device_index
        try:
            with sr.Microphone(**mic_kwargs) as source:
                try:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                except Exception:
                    pass
                try:
                    audio = r.listen(source,
                                     timeout=self.timeout_seconds,
                                     phrase_time_limit=self.phrase_time_limit)
                except sr.WaitTimeoutError:
                    print('No sound detected (timeout)')
                    return None
                try:
                    text = r.recognize_google(audio, language=lang)
                    print(f"ASR: {text}")
                    return text
                except sr.UnknownValueError:
                    print('ASR could not understand the audio')
                    return None
                except sr.RequestError as e:
                    print(f"ASR request error: {e}")
                    return None
                    
        except OSError as e:
            print(f"Microphone error: {e}")
            return None
