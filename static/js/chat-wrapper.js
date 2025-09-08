/**
 * ChatInterface wrapper for Voice Input/Output integration
 * Bridges GTA-V2 voice systems with Spralingua's chat functionality
 */
class ChatInterface {
    constructor() {
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.voiceToggleButton = document.getElementById('voice-btn');
        this.isProcessingVoice = false;
        
        // Initialize VoiceOutput for TTS
        this.voiceOutput = null;
        this.initializeVoiceOutput();
    }
    
    /**
     * Initialize VoiceOutput system
     */
    initializeVoiceOutput() {
        if (typeof VoiceOutput !== 'undefined') {
            this.voiceOutput = new VoiceOutput(this);
            console.log('[CHAT WRAPPER] VoiceOutput initialized');
        } else {
            console.warn('[CHAT WRAPPER] VoiceOutput not available');
        }
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
    
    /**
     * Play TTS for assistant response
     * @param {string} text - Text to speak
     * @param {string} character - Character name for voice selection
     */
    async playAssistantResponse(text, character) {
        if (!this.voiceOutput) {
            console.warn('[CHAT WRAPPER] VoiceOutput not initialized');
            return;
        }
        
        try {
            console.log('[CHAT WRAPPER] Playing TTS for:', character);
            
            // Avatar will change to speaking when audio actually starts playing
            // (handled by voice-output.js onplay event)
            
            // Play the speech
            await this.voiceOutput.speak(text);
            
            // Return avatar to idle state
            if (window.avatarController && window.avatarController.isReady()) {
                window.avatarController.setState('idle');
            }
            
        } catch (error) {
            console.error('[CHAT WRAPPER] Error playing TTS:', error);
            // Ensure avatar returns to idle even on error
            if (window.avatarController && window.avatarController.isReady()) {
                window.avatarController.setState('idle');
            }
        }
    }
    
    /**
     * Handle TTS loading state
     * Called by VoiceOutput when TTS starts/ends loading
     */
    showTTSLoading() {
        console.log('[CHAT WRAPPER] TTS loading...');
        // Could show a loading indicator if needed
    }
    
    hideTTSLoading() {
        console.log('[CHAT WRAPPER] TTS loading complete');
        // Hide loading indicator if shown
    }
    
    /**
     * Set avatar state - called by VoiceOutput
     * @param {string} state - Avatar state (idle, thinking, speaking)
     */
    setAvatarState(state) {
        if (window.avatarController && window.avatarController.isReady()) {
            window.avatarController.setState(state);
        }
    }
}

// Export for use in other scripts
window.ChatInterface = ChatInterface;