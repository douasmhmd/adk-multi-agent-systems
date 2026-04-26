// file: frontend/audio-streamer.js

export class AudioStreamer {
    constructor() {
        this.audioContext = new AudioContext({ sampleRate: 24000 });
        this.audioQueue = [];
        this.isPlaying = false;
        this.sourceNode = null;
    }

    async receiveAudioChunk(base64Audio) {
        // 1. Decode base64 and get raw 16-bit PCM data
        const binaryString = atob(base64Audio);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        const int16Array = new Int16Array(bytes.buffer);

        // 2. Convert 16-bit PCM to 32-bit Float
        const float32Array = new Float32Array(int16Array.length);
        for (let i = 0; i < int16Array.length; i++) {
            float32Array[i] = int16Array[i] / 32768.0;
        }

        // 3. Create a playable AudioBuffer
        const audioBuffer = this.audioContext.createBuffer(1, float32Array.length, 24000);
        audioBuffer.getChannelData(0).set(float32Array);

        // 4. Queue and play the audio
        this.audioQueue.push(audioBuffer);
        if (!this.isPlaying) {
            this.isPlaying = true;
            this.playNextChunk();
        }
    }

    playNextChunk() {
        if (this.audioQueue.length === 0) {
            this.isPlaying = false;
            return;
        }
        this.isPlaying = true;
        const audioChunk = this.audioQueue.shift();
        this.sourceNode = this.audioContext.createBufferSource();
        this.sourceNode.buffer = audioChunk;
        this.sourceNode.connect(this.audioContext.destination);
        this.sourceNode.onended = () => {
            this.playNextChunk();
        };
        this.sourceNode.start();
    }

    stop() {
        if (this.sourceNode) {
            try {
                this.sourceNode.stop();
            } catch (e) {
                // Already stopped
            }
            this.sourceNode = null;
        }
        this.audioQueue = [];
        this.isPlaying = false;
    }
}