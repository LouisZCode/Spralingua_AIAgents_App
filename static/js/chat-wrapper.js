/**
 * Minimal ChatInterface wrapper for VoiceInput integration
 * Provides just enough interface to support voice-input.js from GTA-V2
 */
class ChatInterface {
    constructor() {
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.voiceToggleButton = document.getElementById('voice-btn');
        this.isProcessingVoice = false;
    }
    
    /**
     * Handle voice input - called by VoiceInput from GTA-V2
     * @param {string} transcript - The recognized speech text
     * @param {number} confidence - Confidence level (0-1)
     * @param {object} config - Configuration options
     */
    async handleVoiceInput(transcript, confidence, config) {
        console.log('[CHAT WRAPPER] Handling voice input:', transcript, 'confidence:', confidence);
        
        if (!transcript || transcript.trim() === '') {
            console.log('[CHAT WRAPPER] Empty transcript, ignoring');
            return;
        }
        
        // Set the transcript in the input field
        if (this.messageInput) {
            this.messageInput.value = transcript;
        }
        
        // Mark as processing
        this.isProcessingVoice = true;
        
        try {
            // If autoSubmitMode is 'confidence' and we have high confidence, auto-submit
            if (config.autoSubmitMode === 'confidence' && confidence >= 0.7) {
                console.log('[CHAT WRAPPER] Auto-submitting with high confidence');
                // Use the existing sendMessage function from casual_chat.html
                if (typeof window.sendMessage === 'function') {
                    await window.sendMessage(transcript);
                } else {
                    console.error('[CHAT WRAPPER] sendMessage function not found');
                }
            } else {
                console.log('[CHAT WRAPPER] Transcript set in input, user can review before sending');
            }
        } catch (error) {
            console.error('[CHAT WRAPPER] Error processing voice input:', error);
        } finally {
            this.isProcessingVoice = false;
        }
    }
    
    /**
     * Disable voice input (called by VoiceInput during recording)
     */
    disableVoiceInput() {
        if (this.voiceToggleButton) {
            this.voiceToggleButton.disabled = true;
        }
    }
    
    /**
     * Enable voice input (called by VoiceInput after recording)
     */
    enableVoiceInput() {
        if (this.voiceToggleButton) {
            this.voiceToggleButton.disabled = false;
        }
    }
    
    /**
     * Get if currently processing voice
     */
    getIsProcessingVoice() {
        return this.isProcessingVoice;
    }
}

// Export for use in other scripts
window.ChatInterface = ChatInterface;