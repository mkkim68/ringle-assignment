import { useState, useRef, useEffect } from "react";
import { getAIChat } from "../api";

function Chat() {
  const [isListening, setIsListening] = useState(false);
  const [userSpeech, setUserSpeech] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [volume, setVolume] = useState(0); // 음성 볼륨 상태

  const recognitionRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const sourceRef = useRef(null);
  const rafIdRef = useRef(null);

  // 볼륨 측정 함수
  const analyzeVolume = () => {
    if (!analyserRef.current) return;

    const bufferLength = analyserRef.current.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    analyserRef.current.getByteFrequencyData(dataArray);

    let sum = 0;
    for (let i = 0; i < bufferLength; i++) {
      sum += dataArray[i];
    }
    const average = sum / bufferLength;

    setVolume(average);

    rafIdRef.current = requestAnimationFrame(analyzeVolume);
  };

  const handleStartListening = async () => {
    if (isListening) return; // 이미 켜져 있으면 무시

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("이 브라우저는 음성 인식을 지원하지 않습니다.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;

    recognition.lang = "ko-KR";
    recognition.interimResults = true;
    recognition.continuous = true; // 중단 없이 인식 유지

    recognition.onstart = () => {
      setIsListening(true);
      setUserSpeech("");
    };

    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map((result) => result[0].transcript)
        .join("");
      setUserSpeech(transcript);
    };

    recognition.onerror = (event) => {
      console.error("SpeechRecognition error", event.error);
    };

    recognition.onend = () => {
      setIsListening(false);
      stopAudioAnalysis();
    };

    recognition.start();

    // Web Audio API 셋업
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioContextRef.current = new AudioContext();
      analyserRef.current = audioContextRef.current.createAnalyser();
      sourceRef.current =
        audioContextRef.current.createMediaStreamSource(stream);

      sourceRef.current.connect(analyserRef.current);
      analyserRef.current.fftSize = 256;

      analyzeVolume();
    } catch (err) {
      console.error("Audio setup error:", err);
    }
  };

  const stopAudioAnalysis = () => {
    if (rafIdRef.current) {
      cancelAnimationFrame(rafIdRef.current);
    }
    if (analyserRef.current) {
      analyserRef.current.disconnect();
      analyserRef.current = null;
    }
    if (sourceRef.current) {
      sourceRef.current.disconnect();
      sourceRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
  };

  const handleSubmit = async () => {
    if (!userSpeech.trim()) return;

    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    stopAudioAnalysis();

    try {
      const aiResponse = await getAIChat(userSpeech);
      setChatHistory((prev) => [...prev, { user: userSpeech, ai: aiResponse }]);
      setUserSpeech("");
    } catch (err) {
      console.error("AI 응답 불러오기 실패");
    }
  };

  // 파형(볼륨) 높이에 따라 막대 높이 조절용 스타일
  const bars = 10;
  const barElements = [];
  for (let i = 0; i < bars; i++) {
    // 볼륨을 0~1 범위로 normalize (적절히 조정)
    const height = Math.min(50, (volume / 256) * 100 + Math.random() * 10);
    barElements.push(
      <div
        key={i}
        style={{
          width: 5,
          height,
          margin: "0 2px",
          backgroundColor: "#4caf50",
          borderRadius: 2,
          transition: "height 0.1s ease",
          display: "inline-block",
        }}
      ></div>
    );
  }

  return (
    <div>
      <h1>AI 채팅</h1>

      <button onClick={handleStartListening} disabled={isListening}>
        🎤 음성 인식 시작
      </button>

      {isListening && (
        <div
          style={{
            margin: "10px 0",
            height: 60,
            display: "flex",
            alignItems: "flex-end",
          }}
        >
          {barElements}
        </div>
      )}

      <p>
        <strong>사용자 입력:</strong> {userSpeech}
      </p>

      <button
        onClick={handleSubmit}
        disabled={!isListening && !userSpeech.trim()}
      >
        답변완료
      </button>

      <div>
        <h2>대화 기록</h2>
        <ul>
          {chatHistory.map((entry, index) => (
            <li key={index} style={{ marginBottom: 10 }}>
              <p>
                <strong>👤 나:</strong> {entry.user}
              </p>
              <p>
                <strong>🤖 AI:</strong> {entry.ai}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Chat;
