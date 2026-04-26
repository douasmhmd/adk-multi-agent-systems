// file: app.js
import { AudioStreamer } from './audio-streamer.js';
import { MediaHandler } from './media-handler.js';

const GEMINI_MODEL = "models/gemini-3.1-flash-live-preview";

// =============================================================
// AudioRecorder class
// =============================================================
class AudioRecorder {
    constructor() {
        this.audioContext = null;
        this.workletNode = null;
        this.stream = null;
        this.source = null;
    }

    async start() {
        this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.audioContext = new AudioContext({ sampleRate: 16000 });
        await this.audioContext.audioWorklet.addModule('audio-processor.js');
        this.workletNode = new AudioWorkletNode(this.audioContext, 'audio-processor');
        this.source = this.audioContext.createMediaStreamSource(this.stream);
        this.source.connect(this.workletNode);
    }

    mute() {
        if (this.source && this.workletNode) this.source.disconnect(this.workletNode);
    }
    unmute() {
        if (this.source && this.workletNode) this.source.connect(this.workletNode);
    }
}

// =============================================================
// UI Elements
// =============================================================
const micButton = document.getElementById('micButton');
const webcamButton = document.getElementById('webcamButton');
const screenButton = document.getElementById('screenButton');
const videoElement = document.getElementById('videoElement');
const videoContainer = document.getElementById('videoContainer');
const statusElement = document.getElementById('status');
const connectionStatus = document.getElementById('connectionStatus');
const voiceIndicator = document.getElementById('voiceIndicator');
const conversationEl = document.getElementById('conversation');

// =============================================================
// UI Helpers
// =============================================================
function setConnectionStatus(connected) {
    if (connected) {
        connectionStatus.classList.remove('disconnected');
        connectionStatus.classList.add('connected');
        connectionStatus.querySelector('.status-text').textContent = 'Connected';
    } else {
        connectionStatus.classList.remove('connected');
        connectionStatus.classList.add('disconnected');
        connectionStatus.querySelector('.status-text').textContent = 'Disconnected';
    }
}

function setStatus(text, mode = '') {
    statusElement.textContent = text;
    statusElement.className = 'status-bar ' + mode;
}

function showVoiceIndicator(mode) {
    // mode: 'listening', 'speaking', or '' (hide)
    voiceIndicator.className = 'voice-indicator';
    if (mode === 'listening') {
        voiceIndicator.classList.add('active');
        voiceIndicator.querySelector('.indicator-label').textContent = 'Listening...';
    } else if (mode === 'speaking') {
        voiceIndicator.classList.add('active', 'speaking');
        voiceIndicator.querySelector('.indicator-label').textContent = 'Gemini is speaking...';
    }
}

function addMessage(text, sender = 'assistant') {
    // Remove welcome message if present
    const welcome = conversationEl.querySelector('.welcome-message');
    if (welcome) welcome.remove();

    const msg = document.createElement('div');
    msg.className = 'message ' + sender;
    msg.textContent = text;

    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const meta = document.createElement('div');
    meta.className = 'message-meta';
    meta.textContent = time;
    msg.appendChild(meta);

    conversationEl.appendChild(msg);
    conversationEl.scrollTop = conversationEl.scrollHeight;
}

// =============================================================
// Instances
// =============================================================
const recorder = new AudioRecorder();
const streamer = new AudioStreamer();
const mediaHandler = new MediaHandler();

mediaHandler.setVideoElement(videoElement);

let isSessionActive = false;
let isMicMuted = false;

// =============================================================
// WebSocket
// =============================================================
const PROXY_URL = 'ws://localhost:8081';
let ws = null;

function connectWebSocket() {
    ws = new WebSocket(PROXY_URL);

    ws.onopen = () => {
        console.log('✅ WebSocket connectée');
        setConnectionStatus(true);
    };

    ws.onerror = (e) => console.error('❌ WebSocket error', e);

    ws.onclose = () => {
        console.warn('⚠️ WebSocket fermée');
        setConnectionStatus(false);
        isSessionActive = false;
        setStatus('Connection lost. Reconnecting...', '');
        setTimeout(connectWebSocket, 2000);
    };

    ws.onmessage = async (event) => {
        const response = JSON.parse(event.data);

        // Interruption
        if (response.server_content?.interrupted) {
            if (streamer.stop) streamer.stop();
            setStatus('Interrupted. Listening...', 'listening');
            showVoiceIndicator('listening');
            return;
        }

        // Audio response
        const audioData = response.server_content?.model_turn?.parts?.[0]?.inline_data?.data;
        if (audioData) {
            setStatus('Gemini is speaking...', 'speaking');
            showVoiceIndicator('speaking');
            await streamer.receiveAudioChunk(audioData);
        }

        // Text response (for history)
        const textPart = response.server_content?.model_turn?.parts?.find(p => p.text);
        if (textPart?.text) {
            addMessage(textPart.text, 'assistant');
        }

        // User text (input transcription if available)
        const userText = response.server_content?.input_transcription?.text;
        if (userText) {
            addMessage(userText, 'user');
        }

        // Turn complete
        if (response.server_content?.turn_complete) {
            console.log('Gemini finished its turn.');
            if (!streamer.isPlaying) {
                setStatus('Listening...', 'listening');
                showVoiceIndicator('listening');
            }
        }
    };
}

connectWebSocket();

// =============================================================
// Frame capture callback
// =============================================================
mediaHandler.onFrameCaptured((base64Data) => {
    if (!isSessionActive) return;
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            realtimeInput: {
                mediaChunks: [{ mime_type: "image/jpeg", data: base64Data }]
            }
        }));
    }
});

// =============================================================
// Setup helper
// =============================================================
function sendSetupIfNeeded() {
    if (isSessionActive) return;
    ws.send(JSON.stringify({
        setup: {
            model: GEMINI_MODEL,
            generation_config: { response_modalities: ["audio"] }
        }
    }));
    console.log('📡 Setup envoyé');
    isSessionActive = true;
    setStatus('Session active. Listening...', 'listening');
    showVoiceIndicator('listening');
}

// =============================================================
// Mic button
// =============================================================
micButton.addEventListener('click', async () => {
    if (!isSessionActive) {
        setStatus('Starting microphone...', '');

        if (ws.readyState !== WebSocket.OPEN) {
            alert('⚠️ Not connected. Please wait and try again.');
            return;
        }

        try {
            await recorder.start();
        } catch {
            alert('❌ Microphone access denied.');
            return;
        }

        recorder.workletNode.port.onmessage = (event) => {
            if (!isSessionActive) return;
            const base64 = btoa(String.fromCharCode(...new Uint8Array(event.data)));
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    realtimeInput: {
                        mediaChunks: [{ mime_type: "audio/pcm", data: base64 }]
                    }
                }));
            }
        };

        sendSetupIfNeeded();
        micButton.classList.add('active');
        micButton.querySelector('.btn-label').textContent = 'Mute Mic';
        micButton.querySelector('.btn-icon').textContent = '🔇';
    } else {
        isMicMuted = !isMicMuted;
        if (isMicMuted) {
            recorder.mute();
            micButton.querySelector('.btn-label').textContent = 'Unmute';
            micButton.querySelector('.btn-icon').textContent = '🎤';
            setStatus('Mic muted', '');
            showVoiceIndicator('');
        } else {
            recorder.unmute();
            micButton.querySelector('.btn-label').textContent = 'Mute Mic';
            micButton.querySelector('.btn-icon').textContent = '🔇';
            setStatus('Listening...', 'listening');
            showVoiceIndicator('listening');
        }
    }
});

// =============================================================
// Webcam button
// =============================================================
webcamButton.addEventListener('click', async () => {
    if (mediaHandler.isActive()) {
        mediaHandler.stopAll();
        videoContainer.classList.add('hidden');
        webcamButton.classList.remove('active');
        webcamButton.querySelector('.btn-label').textContent = 'Webcam';
        screenButton.classList.remove('active');
        screenButton.querySelector('.btn-label').textContent = 'Screen';
        return;
    }

    if (ws.readyState !== WebSocket.OPEN) {
        alert('⚠️ Not connected.');
        return;
    }

    const success = await mediaHandler.startWebcam();
    if (!success) {
        alert('❌ Webcam access denied.');
        return;
    }

    videoContainer.classList.remove('hidden');
    sendSetupIfNeeded();
    mediaHandler.startFrameCapture();
    webcamButton.classList.add('active');
    webcamButton.querySelector('.btn-label').textContent = 'Stop';
});

// =============================================================
// Screen share button
// =============================================================
screenButton.addEventListener('click', async () => {
    if (mediaHandler.isActive()) {
        mediaHandler.stopAll();
        videoContainer.classList.add('hidden');
        webcamButton.classList.remove('active');
        webcamButton.querySelector('.btn-label').textContent = 'Webcam';
        screenButton.classList.remove('active');
        screenButton.querySelector('.btn-label').textContent = 'Screen';
        return;
    }

    if (ws.readyState !== WebSocket.OPEN) {
        alert('⚠️ Not connected.');
        return;
    }

    const success = await mediaHandler.startScreenShare();
    if (!success) {
        alert('❌ Screen share denied.');
        return;
    }

    videoContainer.classList.remove('hidden');
    sendSetupIfNeeded();
    mediaHandler.startFrameCapture();
    screenButton.classList.add('active');
    screenButton.querySelector('.btn-label').textContent = 'Stop';
});