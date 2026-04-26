// file: frontend/media-handler.js

export class MediaHandler {
    constructor() {
        this.stream = null;              // le flux vidéo actif (webcam ou écran)
        this.videoElement = null;        // l'élément <video> qui affiche le flux
        this.canvas = null;              // canvas caché pour capturer les frames
        this.captureInterval = null;     // le timer setInterval pour les snapshots
        this.onFrame = null;             // callback appelé à chaque frame capturée
    }

    // Attach the video element where the stream will be displayed
    setVideoElement(videoElement) {
        this.videoElement = videoElement;
    }

    // Register the callback to receive captured frames
    onFrameCaptured(callback) {
        this.onFrame = callback;
    }

    // Start the user's webcam
    async startWebcam() {
        try {
            // Stop any existing stream first
            this.stopAll();

            // Ask for webcam access
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480 },
                audio: false  // audio is handled separately by AudioRecorder
            });

            // Attach the stream to the video element
            if (this.videoElement) {
                this.videoElement.srcObject = this.stream;
                this.videoElement.classList.remove('hidden');
            }

            console.log('📹 Webcam started');
            return true;
        } catch (error) {
            console.error('❌ Failed to start webcam:', error);
            return false;
        }
    }

    // Start screen sharing
    async startScreenShare() {
        try {
            // Stop any existing stream first
            this.stopAll();

            // Ask the user to pick a window / screen / tab
            this.stream = await navigator.mediaDevices.getDisplayMedia({
                video: true,
                audio: false
            });

            // Attach the stream to the video element
            if (this.videoElement) {
                this.videoElement.srcObject = this.stream;
                this.videoElement.classList.remove('hidden');
            }

            // If the user stops sharing via the browser UI, clean up
            this.stream.getVideoTracks()[0].onended = () => {
                console.log('🖥️ Screen share ended by user');
                this.stopAll();
            };

            console.log('🖥️ Screen share started');
            return true;
        } catch (error) {
            console.error('❌ Failed to start screen share:', error);
            return false;
        }
    }

    // Start capturing frames from the video at 1 fps
    startFrameCapture() {
        if (!this.videoElement || !this.stream) {
            console.warn('Cannot start frame capture: no video stream active');
            return;
        }

        // Create a hidden canvas in memory (not in the DOM)
        this.canvas = document.createElement('canvas');
        const ctx = this.canvas.getContext('2d');

        // Start the periodic capture
        this.captureInterval = setInterval(() => {
            if (!this.videoElement.videoWidth) return;  // video not ready yet

            // Match canvas size to video size
            this.canvas.width = this.videoElement.videoWidth;
            this.canvas.height = this.videoElement.videoHeight;

            // Draw the current video frame onto the canvas
            ctx.drawImage(this.videoElement, 0, 0, this.canvas.width, this.canvas.height);

            // Convert to JPEG Base64 (quality 0.7 for smaller size)
            const dataUrl = this.canvas.toDataURL('image/jpeg', 0.7);

            // Strip the "data:image/jpeg;base64," prefix, keep only the pure Base64
            const base64Data = dataUrl.split(',')[1];

            // Send the frame via the callback
            if (this.onFrame) {
                this.onFrame(base64Data);
            }
        }, 1000);  // 1000 ms = 1 frame per second

        console.log('📸 Frame capture started (1 fps)');
    }

    // Stop the periodic frame capture
    stopFrameCapture() {
        if (this.captureInterval) {
            clearInterval(this.captureInterval);
            this.captureInterval = null;
            console.log('📸 Frame capture stopped');
        }
    }

    // Stop everything: stream, video display, frame capture
    stopAll() {
        // Stop frame capture
        this.stopFrameCapture();

        // Stop all tracks of the stream
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }

        // Hide and clear the video element
        if (this.videoElement) {
            this.videoElement.srcObject = null;
            this.videoElement.classList.add('hidden');
        }

        console.log('⏹️ Media stopped');
    }

    // Check if a stream is currently active
    isActive() {
        return this.stream !== null;
    }
}