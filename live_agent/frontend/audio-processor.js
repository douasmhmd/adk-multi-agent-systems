// file: frontend/audio-processor.js

class AudioProcessor extends AudioWorkletProcessor {
 // A buffer to hold audio samples before we send them
 buffer = new Int16Array(2048);
 bufferIndex = 0;

 process(inputs) {
   // We only need the first channel of the first input
   const channelData = inputs[0][0];
   if (!channelData) return true; // Guard against empty inputs

   for (let i = 0; i < channelData.length; i++) {
     // 1. Convert from Float32 (-1.0 to 1.0) to Int16 (-32768 to 32767)
     this.buffer[this.bufferIndex++] = channelData[i] * 0x7FFF;

     // 2. If the buffer is full, send it to the main thread for processing.
     if (this.bufferIndex === this.buffer.length) {
       this.port.postMessage(this.buffer.buffer.slice(0)); // Post a copy
       this.bufferIndex = 0; // Reset for the next chunk
     }
   }
   return true; // Indicate that we want to keep processing
 }
}

registerProcessor('audio-processor', AudioProcessor);