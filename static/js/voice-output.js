// Voice Output Controller for Text-to-Speech

class VoiceOutput {
    constructor(chatInterface) {
        this.chatInterface = chatInterface;
        this.primaryProvider = 'minimax'; // Primary provider
        this.fallbackProvider = 'browser'; // Fallback provider
        this.currentProvider = this.primaryProvider;
        this.isBrowserSupported = this.checkBrowserSupport();
        this.isPlaying = false;
        this.currentUtterance = null;
        this.currentAudio = null;
        this.queue = [];
        
        // Volume management
        this.currentVolume = this.loadVolumePreference() || 0.7;  // Default 70%
        this.isMuted = false;
        
        // Configuration for different providers
        this.config = {
            // Minimax configuration
            minimax: {
                model: 'speech-02-hd',
                voice_id: null,  // Now handled by page-specific window.VOICE_CONFIG
                language: 'English',
                sample_rate: 24000,
                bitrate: 128000
            },
            // Browser TTS configuration
            browser: {
                rate: 1.0,              // Speech rate (0.1 to 10)
                pitch: 1.0,             // Voice pitch (0 to 2)
                volume: 1.0,            // Volume (0 to 1)
                language: 'en-US',      // Language for TTS
                voice: null             // Specific voice (auto-selected if null)
            }
        };
        
        // Supported languages (mapped to provider-specific codes)
        this.supportedLanguages = {
            'en-US': {
                name: 'English (US)',
                minimax: 'English',
                browser: 'en-US'
            },
            'en-GB': {
                name: 'English (UK)', 
                minimax: 'English',
                browser: 'en-GB'
            },
            'de-DE': {
                name: 'German (Germany)',
                minimax: 'German',
                browser: 'de-DE'
            }
        };
        
        // Available voices (populated dynamically for browser TTS)
        this.availableVoices = [];
        
        this.init();
    }
    
    /**
     * Initialize voice output system
     */
    init() {
        // Always set up browser TTS as fallback
        if (this.isBrowserSupported) {
            this.setupBrowserTTS();
        }
        
        console.log(`✅ VoiceOutput initialized with primary: ${this.primaryProvider}, fallback: ${this.fallbackProvider}`);
    }
    
    /**
     * Check if Browser Speech Synthesis API is supported
     */
    checkBrowserSupport() {
        return !!(window.speechSynthesis && window.SpeechSynthesisUtterance);
    }
    
    /**
     * Setup browser TTS with voice detection
     */
    setupBrowserTTS() {
        // Wait for voices to be loaded
        const loadVoices = () => {
            this.availableVoices = speechSynthesis.getVoices();
            this.selectBestVoice();
            console.log(`🔊 Found ${this.availableVoices.length} available voices`);
        };
        
        // Load voices immediately if available
        loadVoices();
        
        // Also listen for voice changes (some browsers load voices asynchronously)
        speechSynthesis.addEventListener('voiceschanged', loadVoices);
    }
    
    /**
     * Select the best voice for current language
     */
    selectBestVoice() {
        if (this.availableVoices.length === 0) {
            console.warn('No voices available yet');
            return;
        }
        
        // Find voices matching current language
        const language = this.config.language || 'en-US'; // Default to English if not set
        const matchingVoices = this.availableVoices.filter(voice => 
            voice.lang.startsWith(language.substring(0, 2))
        );
        
        if (matchingVoices.length > 0) {
            // Prefer local voices, then default to first match
            const localVoice = matchingVoices.find(voice => voice.localService);
            this.config.voice = localVoice || matchingVoices[0];
            
            console.log(`🎭 Selected voice: ${this.config.voice.name} (${this.config.voice.lang})`);
        } else {
            console.warn(`No voices found for language: ${language}`);
        }
    }
    
    /**
     * Speak text using current provider
     * @param {string} text - Text to speak
     * @param {Object} options - Override options for this utterance
     * @returns {Promise<void>}
     */
    async speak(text, options = {}) {
        const cleanText = this.cleanTextForSpeech(text);
        if (!cleanText.trim()) {
            console.warn('Empty text provided for speech');
            return Promise.resolve();
        }
        
        console.log(`🗣️ Speaking: "${cleanText.substring(0, 50)}${cleanText.length > 50 ? '...' : ''}" (provider: ${this.currentProvider})`);
        
        // Add to queue if already playing
        if (this.isPlaying) {
            return new Promise((resolve, reject) => {
                this.queue.push({ text: cleanText, options, resolve, reject });
                console.log(`📋 Added to speech queue (${this.queue.length} items)`);
            });
        }
        
        // Try primary provider first, fallback if it fails
        try {
            if (this.currentProvider === 'minimax') {
                return await this.speakWithMinimax(cleanText, options);
            } else {
                return await this.speakWithBrowser(cleanText, options);
            }
        } catch (error) {
            console.warn(`Primary provider (${this.currentProvider}) failed:`, error);
            
            // Fallback to secondary provider
            if (this.currentProvider === 'minimax' && this.isBrowserSupported) {
                console.log('🔄 Falling back to Browser TTS');
                return await this.speakWithBrowser(cleanText, options);
            } else {
                throw error;
            }
        }
    }
    
    /**
     * Speak text using Minimax API
     * @param {string} text - Cleaned text to speak
     * @param {Object} options - Override options
     * @returns {Promise<void>}
     */
    async speakWithMinimax(text, options = {}) {
        try {
            // Prepare request to Flask backend
            const requestData = {
                text: text,
                language: options.language || this.config.minimax.language
            };
            
            // Use page-specific voice configuration or provided voice_id
            const pageVoiceId = window.VOICE_CONFIG?.voice_id;
            const voiceId = options.voice_id || pageVoiceId;
            
            if (voiceId) {
                requestData.voice_id = voiceId;
                console.log(`🎭 Using voice ID: ${voiceId}`);
            }
            
            // Add character if provided
            if (window.VOICE_CONFIG?.character) {
                requestData.character = window.VOICE_CONFIG.character;
                console.log(`🎭 Using character: ${window.VOICE_CONFIG.character}`);
            }
            
            console.log('🌐 Calling Minimax TTS API...');
            
            // Call Flask TTS endpoint (use configured or default)
            const ttsEndpoint = window.VOICE_CONFIG?.ttsEndpoint || '/api/casual-chat/tts';
            
            // Use fetchWithCredentials if available, otherwise fallback to regular fetch with credentials
            const fetchFn = typeof fetchWithCredentials !== 'undefined' ? fetchWithCredentials : fetch;
            const fetchOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            };
            
            // If using regular fetch, ensure credentials are included
            if (fetchFn === fetch) {
                fetchOptions.credentials = 'include';
            }
            
            const response = await fetchFn(ttsEndpoint, fetchOptions);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }
            
            const data = await response.json();
            
            if (!data.audio_data) {
                throw new Error('No audio data received from API');
            }
            
            console.log('✅ Minimax API response received');
            
            // Convert hex audio data to playable format
            const audioBlob = this.hexToAudioBlob(data.audio_data, 'audio/mp3');
            const audioUrl = URL.createObjectURL(audioBlob);
            
            // Play audio
            return await this.playAudioFromUrl(audioUrl);
            
        } catch (error) {
            console.error('Minimax TTS error:', error);
            throw error;
        }
    }
    
    /**
     * Speak text using Browser TTS
     * @param {string} text - Cleaned text to speak
     * @param {Object} options - Override options
     * @returns {Promise<void>}
     */
    speakWithBrowser(text, options = {}) {
        return new Promise((resolve, reject) => {
            try {
                if (!this.isBrowserSupported) {
                    throw new Error('Browser TTS not supported');
                }
                
                // Create utterance with current configuration
                const utterance = new SpeechSynthesisUtterance(text);
                
                // Apply configuration
                utterance.rate = options.rate || this.config.browser.rate;
                utterance.pitch = options.pitch || this.config.browser.pitch;
                utterance.volume = this.isMuted ? 0 : (options.volume || this.currentVolume);
                utterance.lang = options.language || this.config.browser.language;
                
                // Set voice if available
                if (this.config.browser.voice) {
                    utterance.voice = this.config.browser.voice;
                }
                
                // Set up event handlers
                utterance.onstart = () => this.handleSpeechStart(utterance);
                utterance.onend = () => this.handleSpeechEnd(utterance, resolve);
                utterance.onerror = (event) => this.handleSpeechError(event, reject);
                
                // Store current utterance and start speaking
                this.currentUtterance = utterance;
                this.isPlaying = true;
                
                // Avatar state will be handled by onstart event
                
                speechSynthesis.speak(utterance);
                
            } catch (error) {
                console.error('Error creating speech utterance:', error);
                reject(error);
            }
        });
    }
    
    /**
     * Convert hex string to audio blob
     * @param {string} hexData - Hex encoded audio data
     * @param {string} mimeType - MIME type for the audio
     * @returns {Blob} - Audio blob
     */
    hexToAudioBlob(hexData, mimeType) {
        // Convert hex string to byte array
        const bytes = new Uint8Array(hexData.length / 2);
        for (let i = 0; i < hexData.length; i += 2) {
            bytes[i / 2] = parseInt(hexData.substr(i, 2), 16);
        }
        
        return new Blob([bytes], { type: mimeType });
    }
    
    /**
     * Play audio from URL
     * @param {string} audioUrl - URL to audio file
     * @returns {Promise<void>}
     */
    playAudioFromUrl(audioUrl) {
        return new Promise((resolve, reject) => {
            try {
                const audio = new Audio(audioUrl);
                this.currentAudio = audio;
                
                // Apply volume setting
                audio.volume = this.isMuted ? 0 : this.currentVolume;
                
                this.isPlaying = true;
                
                // Avatar state will be handled by onstart event
                
                // Set up event handlers
                audio.onplay = () => this.handleAudioStart();
                audio.onended = () => this.handleAudioEnd(resolve);
                audio.onerror = (event) => this.handleAudioError(event, reject);
                
                // Start playing
                audio.play();
                
                // Clean up blob URL after use
                audio.onended = () => {
                    URL.revokeObjectURL(audioUrl);
                    this.handleAudioEnd(resolve);
                };
                
            } catch (error) {
                console.error('Error playing audio:', error);
                reject(error);
            }
        });
    }
    
    /**
     * Handle audio start event (for Minimax audio)
     */
    handleAudioStart() {
        console.log('🎵 Audio started');
        
        // Change avatar to speaking when audio actually starts
        if (window.avatarController && window.avatarController.isReady()) {
            window.avatarController.setState('speaking');
        }
        
        // Dispatch custom event for UI updates
        const event = new CustomEvent('voiceOutputStateChange', {
            detail: { state: 'speaking', isPlaying: true }
        });
        document.dispatchEvent(event);
    }
    
    /**
     * Handle audio end event (for Minimax audio)
     */
    handleAudioEnd(resolve) {
        console.log('🔇 Audio ended');
        this.isPlaying = false;
        this.currentAudio = null;
        
        // Return avatar to idle state
        if (window.avatarController && window.avatarController.isReady()) {
            window.avatarController.setState('idle');
        }
        
        // Dispatch custom event
        const event = new CustomEvent('voiceOutputStateChange', {
            detail: { state: 'idle', isPlaying: false }
        });
        document.dispatchEvent(event);
        
        // Resolve the promise
        resolve();
        
        // Process next item in queue
        this.processQueue();
    }
    
    /**
     * Handle audio error event (for Minimax audio)
     */
    handleAudioError(event, reject) {
        console.error('Audio playback error:', event);
        this.isPlaying = false;
        this.currentAudio = null;
        
        // Return avatar to idle state
        if (window.avatarController && window.avatarController.isReady()) {
            window.avatarController.setState('idle');
        }
        
        // Show error to user
        if (this.chatInterface.showError) {
            this.chatInterface.showError('Audio playback failed');
        }
        
        reject(new Error('Audio playback failed'));
        
        // Continue with queue despite error
        this.processQueue();
    }
    
    /**
     * Handle speech start event
     */
    handleSpeechStart(utterance) {
        console.log('🎤 Speech started');
        
        // Change avatar to speaking when browser TTS starts
        if (window.avatarController && window.avatarController.isReady()) {
            window.avatarController.setState('speaking');
        }
        
        // Dispatch custom event for UI updates
        const event = new CustomEvent('voiceOutputStateChange', {
            detail: { state: 'speaking', isPlaying: true }
        });
        document.dispatchEvent(event);
    }
    
    /**
     * Handle speech end event
     */
    handleSpeechEnd(utterance, resolve) {
        console.log('🔇 Speech ended');
        this.isPlaying = false;
        this.currentUtterance = null;
        
        // Return avatar to idle state
        if (window.avatarController && window.avatarController.isReady()) {
            window.avatarController.setState('idle');
        }
        
        // Dispatch custom event
        const event = new CustomEvent('voiceOutputStateChange', {
            detail: { state: 'idle', isPlaying: false }
        });
        document.dispatchEvent(event);
        
        // Resolve the promise
        resolve();
        
        // Process next item in queue
        this.processQueue();
    }
    
    /**
     * Handle speech error event
     */
    handleSpeechError(event, reject) {
        console.error('Speech synthesis error:', event.error);
        this.isPlaying = false;
        this.currentUtterance = null;
        
        // Return avatar to idle state
        if (window.avatarController && window.avatarController.isReady()) {
            window.avatarController.setState('idle');
        }
        
        // Show error to user
        if (this.chatInterface.showError) {
            this.chatInterface.showError(`Speech error: ${event.error}`);
        }
        
        reject(new Error(`Speech synthesis failed: ${event.error}`));
        
        // Continue with queue despite error
        this.processQueue();
    }
    
    /**
     * Process next item in speech queue
     */
    processQueue() {
        if (this.queue.length === 0) {
            return;
        }
        
        const nextItem = this.queue.shift();
        console.log(`📤 Processing next speech item (${this.queue.length} remaining)`);
        
        this.speak(nextItem.text, nextItem.options)
            .then(nextItem.resolve)
            .catch(nextItem.reject);
    }
    
    /**
     * Stop current speech and clear queue
     */
    stop() {
        console.log('🛑 Stopping speech output');
        
        // Stop current speech/audio
        if (this.isPlaying) {
            // Stop browser TTS
            if (this.currentUtterance) {
                speechSynthesis.cancel();
                this.currentUtterance = null;
            }
            
            // Stop Minimax audio
            if (this.currentAudio) {
                this.currentAudio.pause();
                this.currentAudio.currentTime = 0;
                this.currentAudio = null;
            }
            
            this.isPlaying = false;
            
            // Return avatar to idle
            if (this.chatInterface.setAvatarState) {
                this.chatInterface.setAvatarState('idle');
            }
        }
        
        // Clear queue
        this.queue.forEach(item => {
            item.reject(new Error('Speech cancelled'));
        });
        this.queue = [];
        
        console.log('✅ Speech output stopped and queue cleared');
    }
    
    /**
     * Clean text for speech synthesis
     * @param {string} text - Raw text that may contain HTML or special characters
     * @returns {string} - Cleaned text suitable for speech
     */
    cleanTextForSpeech(text) {
        // Remove HTML tags
        let cleaned = text.replace(/<[^>]*>/g, ' ');
        
        // Replace multiple whitespace with single space
        cleaned = cleaned.replace(/\s+/g, ' ');
        
        // Remove or replace special characters that might cause issues
        cleaned = cleaned.replace(/[<>]/g, '');
        
        return cleaned.trim();
    }
    
    /**
     * Set language for speech synthesis
     * @param {string} langCode - Language code (e.g., 'en-US', 'de-DE')
     */
    setLanguage(langCode) {
        if (!this.supportedLanguages[langCode]) {
            console.error(`Unsupported language code: ${langCode}`);
            return false;
        }
        
        this.config.language = langCode;
        this.selectBestVoice(); // Re-select voice for new language
        
        console.log(`🌐 TTS language changed to ${this.supportedLanguages[langCode]}`);
        return true;
    }
    
    /**
     * Get current language
     */
    getCurrentLanguage() {
        return {
            code: this.config.language,
            name: this.supportedLanguages[this.config.language]
        };
    }
    
    /**
     * Get list of available voices for current language
     */
    getAvailableVoices() {
        const language = this.config.language || 'en-US';
        return this.availableVoices.filter(voice => 
            voice.lang.startsWith(language.substring(0, 2))
        );
    }
    
    /**
     * Set specific voice
     * @param {SpeechSynthesisVoice} voice - Voice to use
     */
    setVoice(voice) {
        if (voice && this.availableVoices.includes(voice)) {
            this.config.voice = voice;
            console.log(`🎭 Voice changed to: ${voice.name}`);
            return true;
        }
        return false;
    }
    
    /**
     * Adjust speech rate
     * @param {number} rate - Speech rate (0.1 to 10, default 1.0)
     */
    setRate(rate) {
        if (rate >= 0.1 && rate <= 10) {
            this.config.rate = rate;
            console.log(`⚡ Speech rate set to: ${rate}`);
            return true;
        }
        return false;
    }
    
    /**
     * Check if TTS is currently playing
     */
    isCurrentlyPlaying() {
        return this.isPlaying;
    }
    
    /**
     * Get queue length
     */
    getQueueLength() {
        return this.queue.length;
    }
    
    /**
     * Set volume level
     * @param {number} volume - Volume level (0 to 1)
     */
    setVolume(volume) {
        // Clamp volume between 0 and 1
        this.currentVolume = Math.max(0, Math.min(1, volume));
        
        // Apply to current audio if playing
        if (this.currentAudio) {
            this.currentAudio.volume = this.isMuted ? 0 : this.currentVolume;
        }
        
        // Update browser TTS config
        this.config.browser.volume = this.isMuted ? 0 : this.currentVolume;
        
        // Save preference
        this.saveVolumePreference(this.currentVolume);
        
        console.log(`🔊 Volume set to: ${Math.round(this.currentVolume * 100)}%`);
    }
    
    /**
     * Toggle mute state
     */
    toggleMute() {
        this.isMuted = !this.isMuted;
        
        // Apply to current audio if playing
        if (this.currentAudio) {
            this.currentAudio.volume = this.isMuted ? 0 : this.currentVolume;
        }
        
        // Update browser TTS config
        this.config.browser.volume = this.isMuted ? 0 : this.currentVolume;
        
        console.log(`🔇 Mute ${this.isMuted ? 'enabled' : 'disabled'}`);
        return this.isMuted;
    }
    
    /**
     * Get current volume level
     * @returns {number} Volume level (0 to 1)
     */
    getVolume() {
        return this.currentVolume;
    }
    
    /**
     * Check if muted
     * @returns {boolean} Mute state
     */
    isMutedState() {
        return this.isMuted;
    }
    
    /**
     * Save volume preference to localStorage
     * @param {number} volume - Volume level to save
     */
    saveVolumePreference(volume) {
        try {
            localStorage.setItem('voiceOutputVolume', volume.toString());
        } catch (e) {
            console.warn('Failed to save volume preference:', e);
        }
    }
    
    /**
     * Load volume preference from localStorage
     * @returns {number|null} Saved volume or null
     */
    loadVolumePreference() {
        try {
            const saved = localStorage.getItem('voiceOutputVolume');
            return saved ? parseFloat(saved) : null;
        } catch (e) {
            console.warn('Failed to load volume preference:', e);
            return null;
        }
    }
    
    /**
     * Destroy voice output and clean up resources
     */
    destroy() {
        this.stop();
        console.log('🗑️ VoiceOutput destroyed');
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoiceOutput;
}

// Make VoiceOutput available in browser global scope
window.VoiceOutput = VoiceOutput;