// Voice Input Controller for Speech Recognition

class VoiceInput {
    constructor(chatInterface) {
        this.chatInterface = chatInterface;
        
        // Voice input configuration (module-specific overrides)
        this.voiceInputConfig = window.VOICE_INPUT_CONFIG || {};
        console.log('🎙️ Voice Input Config:', this.voiceInputConfig);
        
        // Check VOICE_INPUT_CONFIG for language first, then fall back to default
        if (window.VOICE_INPUT_CONFIG && window.VOICE_INPUT_CONFIG.language) {
            this.language = window.VOICE_INPUT_CONFIG.language;
            console.log('🎙️ Using language from VOICE_INPUT_CONFIG:', this.language);
        } else {
            // No language configured - show error instead of using default
            console.error('❌ No language configured for microphone! VOICE_INPUT_CONFIG.language is missing.');
            this.language = null; // Don't set a default
        }
        
        this.isSupported = this.checkSupport();
        this.isRecording = false;
        this.recognition = null;
        this.audioLevel = 0;
        this.languageSelector = null; // Language selector integration
        this.microphoneButton = null; // Microphone button reference
        this.sendButton = null; // Send button reference for manual send
        
        // Base configuration
        this.config = {
            continuous: false,           // Single utterance mode
            interimResults: true,        // Show partial results
            maxAlternatives: 3,          // Multiple interpretations
            confidenceThreshold: 0.7     // Minimum confidence to accept
        };
        
        // Apply module-specific overrides
        this.applyVoiceInputConfig();
        
        // Timed recording properties
        this.timedRecordingUI = null;
        this.continuousRecordingMode = false;
        this.accumulatedTranscript = [];
        this.recordingTimeout = null;
        this.autoRestartOnSilence = false;
        this.manualStop = false;
        this.isStoppingTimedRecording = false; // Flag to prevent premature clearing
        
        // Timing fix state for async speech recognition
        this.hasPendingResults = false;
        this.lastInterimTimestamp = null;
        this.wasInTimedRecording = false;
        this.stopProcessingTimeout = null;
        this.savedTranscriptForLateResults = '';
        
        // Supported languages (future-ready)
        this.supportedLanguages = {
            'en-US': 'English (US)',
            'en-GB': 'English (UK)',
            'de-DE': 'German (Germany)'
        };
        
        this.init();
    }
    
    /**
     * Apply module-specific voice input configuration
     */
    applyVoiceInputConfig() {
        if (!this.voiceInputConfig) return;
        
        // Apply confidence override if specified
        if (this.voiceInputConfig.confidence_override !== undefined) {
            this.config.confidenceThreshold = this.voiceInputConfig.confidence_override;
            console.log(`🎙️ Confidence threshold overridden to: ${this.config.confidenceThreshold}`);
        }
        
        // Log configuration for debugging
        console.log('🎙️ Voice Input Configuration Applied:', {
            module_type: this.voiceInputConfig.module_type || 'default',
            auto_submit_mode: this.voiceInputConfig.auto_submit_mode || 'confidence',
            confidence_threshold: this.config.confidenceThreshold,
            show_transcript: this.voiceInputConfig.show_transcript !== false,
            allow_editing: this.voiceInputConfig.allow_editing !== false
        });
    }
    
    /**
     * Get default language based on page context
     */
    getDefaultLanguage() {
        // Check for page-specific language configuration
        if (window.LANGUAGE_SELECTOR_CONFIG && window.LANGUAGE_SELECTOR_CONFIG.default) {
            return window.LANGUAGE_SELECTOR_CONFIG.default;
        }
        
        // Check if we're on a German course page
        if (window.location.pathname.includes('/german')) {
            return 'de-DE';
        }
        
        // Default fallback
        return 'en-US';
    }
    
    /**
     * Initialize voice input system
     */
    init() {
        if (!this.isSupported) {
            console.warn('Speech recognition not supported in this browser');
            return;
        }
        
        this.setupRecognition();
        this.setupMicrophoneButton();
        // Send button removed - using GTA-V2's simpler approach
        this.initializeLanguageSelector();
        console.log('✅ VoiceInput initialized successfully');
    }
    
    /**
     * Setup microphone button handling (proper OOP encapsulation)
     */
    setupMicrophoneButton() {
        this.microphoneButton = document.getElementById('voice-btn');
        if (!this.microphoneButton) {
            console.warn('Microphone button not found');
            return;
        }
        
        // Add click handler with event propagation stopped
        this.microphoneButton.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent bubbling to document
            this.handleMicrophoneClick();
        });
        
        console.log('🎤 Microphone button configured');
    }
    
    /**
     * Refresh microphone button handler after DOM changes
     * Public method called by ChatInterface after DOM restoration
     */
    refreshMicrophoneButton() {
        console.log('🔄 [VOICE INPUT] Refreshing microphone button handler...');
        this.setupMicrophoneButton();
        console.log('✅ [VOICE INPUT] Microphone button handler restored');
    }
    
    // Send button methods removed - using GTA-V2's simpler approach
    
    /**
     * Handle microphone button click - show language selector or start recording
     */
    handleMicrophoneClick() {
        console.log('🎤 Microphone button clicked');

        // Hide inline hint when microphone is clicked
        if (window.hintDisplay) {
            window.hintDisplay.hide();
            console.log('🎤 Hiding inline hint on microphone click');
        }

        if (this.isRecording) {
            // Stop recording if currently recording
            this.stopRecording();
            return;
        }

        // Show language selector if available, otherwise start recording directly
        if (this.languageSelector) {
            console.log('🌐 Showing language selector');
            this.languageSelector.show();
        } else {
            console.log('🎤 Starting recording directly (no language selector)');
            this.startRecording();
        }
    }
    
    /**
     * Initialize language selector if available
     */
    initializeLanguageSelector() {
        // Check if LanguageSelector class is available
        if (typeof LanguageSelector === 'undefined') {
            console.log('ℹ️ LanguageSelector not available - using direct voice input');
            return;
        }
        
        try {
            // Get configuration from page
            const config = window.LANGUAGE_SELECTOR_CONFIG || {
                available: ['de-DE', 'en-US'],
                default: 'de-DE'
            };
            
            // Create language selector
            this.languageSelector = new LanguageSelector(this, config);
            console.log('🌐 LanguageSelector integrated successfully');
            
        } catch (error) {
            console.error('Error initializing LanguageSelector:', error);
            this.languageSelector = null;
        }
    }
    
    /**
     * Check if Web Speech API is supported
     */
    checkSupport() {
        return !!(window.SpeechRecognition || window.webkitSpeechRecognition);
    }
    
    /**
     * Setup speech recognition with proper configuration
     */
    setupRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        // Check if language is configured
        if (!this.language) {
            console.error('❌ Cannot setup speech recognition: No language configured');
            // Show error to user
            if (this.chatInterface && this.chatInterface.showError) {
                this.chatInterface.showError('Microphone error: No language selected. Please refresh the page.');
            }
            return;
        }
        
        // Configure recognition
        this.recognition.lang = this.language;
        this.recognition.continuous = this.config.continuous;
        this.recognition.interimResults = this.config.interimResults;
        this.recognition.maxAlternatives = this.config.maxAlternatives;
        
        // Set up event listeners
        this.recognition.onstart = () => this.handleStart();
        this.recognition.onresult = (event) => this.handleResult(event);
        this.recognition.onerror = (event) => this.handleError(event);
        this.recognition.onend = () => this.handleEnd();
        
        console.log(`🎤 Speech recognition configured for language: ${this.language}`);
    }
    
    /**
     * Start recording voice input
     */
    startRecording() {
        if (!this.isSupported) {
            console.error('Speech recognition not supported');
            this.chatInterface.showError('Voice input is not supported in this browser');
            return false;
        }
        
        if (this.isRecording) {
            console.warn('Already recording');
            return false;
        }
        
        // Check if timed recording is configured
        if (this.voiceInputConfig.recording_mode === 'timed') {
            return this.startTimedRecording();
        }
        
        try {
            console.log('🎤 Starting voice recording...');
            this.recognition.start();
            return true;
        } catch (error) {
            console.error('Error starting voice recording:', error);
            this.handleError({ error: 'not-allowed' });
            return false;
        }
    }
    
    /**
     * Start timed recording with visual feedback
     */
    startTimedRecording() {
        console.log('⏱️ Starting timed recording mode');
        console.log('🔍 Checking TimedRecordingUI availability:', typeof TimedRecordingUI);
        
        // Initialize timed UI if TimedRecordingUI is available
        if (typeof TimedRecordingUI !== 'undefined') {
            // Use the voice-only-wrapper as container for better positioning
            const inputArea = document.querySelector('.voice-only-wrapper');
            if (inputArea) {
                console.log('📱 Initializing TimedRecordingUI with container:', inputArea);
                
                // Timer will replace the voice wrapper content
                console.log('🎤 Voice controls will be replaced by timer UI');
                
                this.timedRecordingUI = new TimedRecordingUI(inputArea, {
                    duration: this.voiceInputConfig.max_duration || 30000,  // Default to 30 seconds
                    style: this.voiceInputConfig.timer_style || 'circular',
                    stopButtonText: this.voiceInputConfig.stop_button_text || "Stop Recording",
                    recordingLabel: this.voiceInputConfig.recording_label || "Recording...",
                    onStop: () => this.stopTimedRecording(),
                    onTimeout: () => this.handleRecordingTimeout(),
                    showTranscriptPreview: this.voiceInputConfig.show_transcript_preview || false
                });
                this.timedRecordingUI.show();
            } else {
                console.error('❌ Could not find .voice-only-wrapper element for timer UI');
            }
        } else {
            console.warn('⚠️ TimedRecordingUI not loaded, falling back to standard recording');
        }
        
        // Set continuous mode flags
        this.continuousRecordingMode = true;
        this.accumulatedTranscript = [];
        this.manualStop = false;
        this.autoRestartOnSilence = this.voiceInputConfig.auto_restart_on_silence !== false;
        
        // Configure recognition for continuous mode
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        
        // Start recording
        try {
            console.log('🎤 Starting continuous voice recording...');
            this.recognition.start();
            
            // Set timeout for maximum duration
            const maxDuration = this.voiceInputConfig.max_duration || 30000;  // Default to 30 seconds
            this.recordingTimeout = setTimeout(() => {
                this.handleRecordingTimeout();
            }, maxDuration);
            
            return true;
        } catch (error) {
            console.error('Error starting timed recording:', error);
            this.handleError({ error: 'not-allowed' });
            if (this.timedRecordingUI) {
                this.timedRecordingUI.hide();
            }
            return false;
        }
    }
    
    /**
     * Stop timed recording
     */
    stopTimedRecording() {
        console.log('🛑 Stop button clicked - preparing to stop recording');
        console.log(`📊 Current state: ${this.accumulatedTranscript.length} segments accumulated`);
        
        // Mark that we're stopping but DON'T set continuousRecordingMode = false yet
        // This allows speech results to continue accumulating during the delay
        this.manualStop = true;
        this.isStoppingTimedRecording = true; // Prevent clearing during stop process
        
        // Add short delay to collect any final speech segments
        console.log('⏳ Adding 200ms delay to collect final speech segments...');
        setTimeout(() => {
            console.log(`📊 After delay: ${this.accumulatedTranscript.length} segments accumulated`);
            // NOW set the flags that stop accumulation
            this.continuousRecordingMode = false;
            this.wasInTimedRecording = true; // Mark that we were in timed recording
            this.continueStopTimedRecording();
        }, 200); // 200ms delay
    }
    
    continueStopTimedRecording() {
        
        // Clear timeout
        if (this.recordingTimeout) {
            clearTimeout(this.recordingTimeout);
            this.recordingTimeout = null;
        }
        
        // Stop recognition
        if (this.recognition && this.isRecording) {
            this.recognition.stop();
        }
        
        // Check if we should wait for pending results
        const recentActivity = this.lastInterimTimestamp && (Date.now() - this.lastInterimTimestamp) < 1000;
        
        if (this.hasPendingResults || recentActivity) {
            console.log('⏳ Pending results detected - delaying processing...');
            
            // Save current transcript state
            this.savedTranscriptForLateResults = this.accumulatedTranscript.join(' ');
            
            // Delay processing to wait for final results
            this.stopProcessingTimeout = setTimeout(() => {
                this.finalizeTimedRecording();
            }, 300); // 300ms delay for pending results
        } else {
            // No pending results, process immediately
            this.finalizeTimedRecording();
        }
    }
    
    /**
     * Finalize timed recording after any pending results
     */
    finalizeTimedRecording() {
        console.log('🎯 Finalizing timed recording');
        
        // Combine saved transcript with any accumulated segments
        let finalTranscript = '';
        if (this.savedTranscriptForLateResults) {
            finalTranscript = this.savedTranscriptForLateResults;
        } else if (this.accumulatedTranscript.length > 0) {
            finalTranscript = this.accumulatedTranscript.join(' ');
        }
        
        if (finalTranscript) {
            console.log(`💾 Processing final transcript: "${finalTranscript}"`);
            // Process the transcript
            this.processContinuousTranscript(finalTranscript);
        } else {
            console.log('⚠️ No transcript to process');
        }
        
        // Clear timing fix state
        this.wasInTimedRecording = false;
        this.savedTranscriptForLateResults = '';
        this.hasPendingResults = false;
        
        // Clear the stopping flag and transcript now that we're done
        this.isStoppingTimedRecording = false;
        this.accumulatedTranscript = [];
        
        // Hide UI and refresh DOM references
        if (this.timedRecordingUI) {
            // Small delay to ensure transcript processing completes
            setTimeout(() => {
                console.log('🎭 Hiding timer UI after transcript processing...');
                this.timedRecordingUI.hide();
                this.timedRecordingUI = null;
                
                // Voice wrapper content will be restored by TimedRecordingUI.hide()
                console.log('🎤 Voice controls restored');
                
                // Refresh ChatInterface DOM references after UI restoration
                console.log('🔄 Preparing to refresh DOM references...');
                
                // Small delay to ensure DOM is restored
                setTimeout(() => {
                    console.log('🔍 Checking for ChatInterface instance...');
                    console.log('  - this.chatInterface exists:', !!this.chatInterface);
                    console.log('  - window.chatInterface exists:', !!window.chatInterface);
                    
                    // Try both this.chatInterface and window.chatInterface
                    const chatInterface = this.chatInterface || window.chatInterface;
                    
                    if (chatInterface) {
                        console.log('✅ ChatInterface found, checking for refresh method...');
                        console.log('  - refreshElementReferences exists:', typeof chatInterface.refreshElementReferences === 'function');
                        
                        if (typeof chatInterface.refreshElementReferences === 'function') {
                            try {
                                console.log('🔄 Calling refreshElementReferences...');
                                chatInterface.refreshElementReferences();
                                console.log('✅ DOM refresh completed successfully');
                                
                                // Check module configuration before restoring transcript
                                const shouldShowTranscript = this.voiceInputConfig.show_transcript !== false;
                                const autoSubmitMode = this.voiceInputConfig.auto_submit_mode || 'confidence';
                                
                                if (shouldShowTranscript && finalTranscript) {
                                    // Module wants transcript shown - restore it
                                    const restoredInput = document.getElementById('message-input');
                                    if (restoredInput) {
                                        restoredInput.value = finalTranscript;
                                        console.log(`✅ Restored transcript to input: "${finalTranscript}"`);
                                        
                                        // Trigger auto-resize for the textarea
                                        if (chatInterface && typeof chatInterface.autoResizeTextarea === 'function') {
                                            chatInterface.autoResizeTextarea();
                                            console.log('📏 Triggered textarea auto-resize');
                                        }
                                        
                                        // Focus the input to show cursor
                                        restoredInput.focus();
                                        
                                        // Move cursor to end of text
                                        restoredInput.setSelectionRange(finalTranscript.length, finalTranscript.length);
                                    }
                                } else if (!shouldShowTranscript && autoSubmitMode === 'always' && finalTranscript) {
                                    // Module wants auto-submit without showing - trigger submission
                                    console.log('🚀 Auto-submitting transcript without showing in input');
                                    const messageInput = document.getElementById('message-input');
                                    const chatForm = document.getElementById('chat-form');
                                    
                                    if (messageInput && chatForm && finalTranscript) {
                                        // Temporarily set the value for submission
                                        messageInput.value = finalTranscript;
                                        
                                        // Trigger form submission
                                        const submitEvent = new Event('submit', { bubbles: true, cancelable: true });
                                        chatForm.dispatchEvent(submitEvent);
                                        
                                        // Clear the input after a brief delay
                                        setTimeout(() => {
                                            messageInput.value = '';
                                        }, 100);
                                    }
                                } else {
                                    console.log('📝 Module configuration: no action needed for transcript');
                                }
                            } catch (error) {
                                console.error('❌ Error refreshing DOM references:', error);
                            }
                        } else {
                            console.warn('⚠️ refreshElementReferences method not found on ChatInterface');
                        }
                    } else {
                        console.warn('⚠️ ChatInterface instance not found - cannot refresh DOM references');
                        console.log('  - Try refreshing the page if the microphone stops working');
                    }
                }, 100);
            }, 50); // Reduced delay - transcript processing should be done
        }
    }
    
    /**
     * Process late-arriving transcript from timed recording
     */
    processLateTimedTranscript() {
        console.log('📥 Processing late-arriving timed transcript');
        
        if (!this.savedTranscriptForLateResults) {
            console.warn('⚠️ No late transcript to process');
            return;
        }
        
        // Try to restore to input box
        const messageInput = document.getElementById('message-input');
        if (messageInput && this.voiceInputConfig.show_transcript !== false) {
            messageInput.value = this.savedTranscriptForLateResults;
            console.log(`✅ Late transcript restored to input: "${this.savedTranscriptForLateResults}"`);
            
            // Trigger auto-resize
            const chatInterface = this.chatInterface || window.chatInterface;
            if (chatInterface && typeof chatInterface.autoResizeTextarea === 'function') {
                chatInterface.autoResizeTextarea();
            }
            
            // Focus and position cursor
            messageInput.focus();
            messageInput.setSelectionRange(this.savedTranscriptForLateResults.length, this.savedTranscriptForLateResults.length);
        }
        
        // Clear the saved transcript
        this.savedTranscriptForLateResults = '';
        this.wasInTimedRecording = false;
    }
    
    // DELETE EVERYTHING BELOW THIS LINE UNTIL THE NEXT METHOD DECLARATION
    
    /**
     * Handle recording timeout - auto-send on timer expiry
     */
    handleRecordingTimeout() {
        console.log('⏱️ Recording timeout reached - auto-sending');
        
        // Check if auto-submit on timer is enabled
        if (this.voiceInputConfig.auto_submit_mode === 'timer_only' || 
            this.voiceInputConfig.auto_submit_mode === 'always') {
            
            // Check if we have any chunks to send
            if (this.accumulatedTranscript.length > 0) {
                const fullTranscript = this.accumulatedTranscript.join(' ');
                console.log(`⏱️ Auto-sending on timer expiry: "${fullTranscript}"`);
                
                // Process the transcript (this will send it)
                this.processContinuousTranscript(fullTranscript);
                
                // Clear accumulated transcript
                this.accumulatedTranscript = [];
                
            }
        }
        
        // Stop the recording
        this.stopTimedRecording();
    }
    
    /**
     * Stop recording voice input
     */
    stopRecording() {
        if (!this.isRecording) {
            return;
        }
        
        console.log('🛑 Stopping voice recording...');
        this.recognition.stop();
    }
    
    /**
     * Handle recording start
     */
    handleStart() {
        console.log('🎙️ Voice recording started');
        this.isRecording = true;
        
        // Update avatar to listening state
        if (this.chatInterface.setAvatarState) {
            this.chatInterface.setAvatarState('listening');
        }
        
        // Add recording-active class to controls container for timer centering
        const controlsContainer = document.querySelector('.voice-only-controls');
        if (controlsContainer) {
            controlsContainer.classList.add('recording-active');
        }
        
        // Update microphone button state
        this.updateMicrophoneButton('recording');
        
        // Update UI
        this.updateUI('recording');
    }
    
    /**
     * Handle speech recognition results
     */
    handleResult(event) {
        let transcript = '';
        let confidence = 0;
        let isFinal = false;
        
        // Extract transcript and confidence from results
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const result = event.results[i];
            transcript += result[0].transcript;
            confidence = result[0].confidence;
            isFinal = result.isFinal;
        }
        
        console.log(`🎤 Speech result: "${transcript}" (confidence: ${confidence?.toFixed(2) || 'unknown'})`);
        
        // Track pending results for timing fix
        if (!isFinal) {
            this.hasPendingResults = true;
            this.lastInterimTimestamp = Date.now();
        } else {
            this.hasPendingResults = false;
        }
        
        // Handle continuous recording mode
        if (this.continuousRecordingMode) {
            // Handle interim results - disable button during active speech
            if (!isFinal && this.timedRecordingUI) {
                // Disable button while speech is being processed
                if (this.accumulatedTranscript.length > 0) {
                    // Only disable if we already have at least one segment (button was enabled)
                    console.log('🎤 [VOICE INPUT] Interim speech detected - disabling button during processing');
                    console.log('🔍 [DEBUG] Checking disableStopButton exists?', typeof this.timedRecordingUI.disableStopButton);
                    
                    try {
                        if (typeof this.timedRecordingUI.disableStopButton === 'function') {
                            this.timedRecordingUI.disableStopButton();
                        } else {
                            console.error('❌ disableStopButton is not a function!');
                        }
                    } catch (error) {
                        console.error('❌ Error calling disableStopButton:', error);
                    }
                }
            }
            
            if (isFinal && transcript.trim()) {
                // Add to accumulated transcript
                this.accumulatedTranscript.push(transcript.trim());
                console.log(`📝 Accumulated transcript segments: ${this.accumulatedTranscript.length}`);
                
                // Enable stop button after segment is complete
                if (this.timedRecordingUI) {
                    console.log('🔓 [VOICE INPUT] Final segment accumulated - enabling stop button');
                    console.log('🔍 [DEBUG] timedRecordingUI type:', typeof this.timedRecordingUI);
                    console.log('🔍 [DEBUG] timedRecordingUI constructor:', this.timedRecordingUI.constructor.name);
                    console.log('🔍 [DEBUG] enableStopButton exists?', typeof this.timedRecordingUI.enableStopButton);
                    
                    try {
                        if (typeof this.timedRecordingUI.enableStopButton === 'function') {
                            this.timedRecordingUI.enableStopButton();
                        } else {
                            console.error('❌ enableStopButton is not a function!');
                            console.log('Available methods:', Object.getOwnPropertyNames(Object.getPrototypeOf(this.timedRecordingUI)));
                        }
                    } catch (error) {
                        console.error('❌ Error calling enableStopButton:', error);
                    }
                }
                
                // Update preview if configured
                if (this.timedRecordingUI && this.voiceInputConfig.show_transcript_preview) {
                    const fullTranscript = this.accumulatedTranscript.join(' ');
                    this.timedRecordingUI.updateTranscriptPreview(fullTranscript);
                }
            }
            // CRITICAL FIX: Always return when in continuous mode to prevent fall-through
            return;
        }
        
        // Check if this is a late-arriving result from timed recording
        if (this.wasInTimedRecording && isFinal && transcript.trim()) {
            console.log('🔄 Late-arriving result from timed recording detected');
            // Add to saved transcript
            if (this.savedTranscriptForLateResults) {
                this.savedTranscriptForLateResults += ' ' + transcript.trim();
            } else {
                this.savedTranscriptForLateResults = transcript.trim();
            }
            // Process the updated transcript
            this.processLateTimedTranscript();
            return;
        }
        
        // Standard recording mode
        if (isFinal && confidence >= this.config.confidenceThreshold) {
            this.processTranscript(transcript, confidence);
        } else if (isFinal) {
            console.warn(`Low confidence transcript rejected: ${confidence?.toFixed(2)}`);
            this.showLowConfidenceMessage(transcript, confidence);
        }
    }
    
    /**
     * Handle speech recognition errors
     */
    handleError(event) {
        console.error('Speech recognition error:', event.error);
        
        let errorMessage = 'Voice input error occurred';
        
        switch (event.error) {
            case 'not-allowed':
                errorMessage = 'Microphone permission denied. Please allow microphone access and try again.';
                break;
            case 'no-speech':
                errorMessage = 'No speech detected. Please try speaking again.';
                break;
            case 'network':
                errorMessage = 'Network error occurred. Please check your connection.';
                break;
            case 'audio-capture':
                errorMessage = 'No microphone found. Please check your audio settings.';
                break;
            default:
                errorMessage = `Voice input error: ${event.error}`;
        }
        
        this.chatInterface.showError(errorMessage);
        this.updateUI('error');
    }
    
    /**
     * Handle recording end
     */
    handleEnd() {
        console.log('🔇 Voice recording ended');
        
        // Remove recording-active class from controls container
        const controlsContainer = document.querySelector('.voice-only-controls');
        if (controlsContainer) {
            controlsContainer.classList.remove('recording-active');
        }
        
        // Handle continuous recording mode
        if (this.continuousRecordingMode && this.autoRestartOnSilence && !this.manualStop) {
            console.log('🔄 Auto-restarting recording after silence...');
            // Restart recording after a short delay
            setTimeout(() => {
                if (this.continuousRecordingMode && !this.manualStop) {
                    try {
                        this.recognition.start();
                        console.log('✅ Recording restarted');
                    } catch (error) {
                        console.error('Error restarting recording:', error);
                    }
                }
            }, 100);
            return; // Don't update UI states
        }
        
        this.isRecording = false;
        
        // Return avatar to idle state
        if (this.chatInterface.setAvatarState) {
            this.chatInterface.setAvatarState('idle');
        }
        
        // Update microphone button state
        this.updateMicrophoneButton('idle');
        
        this.updateUI('idle');
    }
    
    /**
     * Process successful transcript
     */
    processTranscript(transcript, confidence) {
        console.log(`✅ Processing transcript: "${transcript}"`);
        
        // Clean up transcript
        const cleanTranscript = transcript.trim();
        
        if (cleanTranscript.length === 0) {
            console.warn('Empty transcript received');
            return;
        }
        
        // Check if module configuration affects behavior
        const shouldShowTranscript = this.voiceInputConfig.show_transcript !== false;
        const shouldAllowEditing = this.voiceInputConfig.allow_editing !== false;
        
        // Pass configuration along with transcript
        this.chatInterface.handleVoiceInput(cleanTranscript, confidence, {
            autoSubmitMode: this.voiceInputConfig.auto_submit_mode || 'confidence',
            showTranscript: shouldShowTranscript,
            allowEditing: shouldAllowEditing
        });
    }
    
    /**
     * Process accumulated transcript from continuous recording
     */
    processContinuousTranscript(providedTranscript = null) {
        let fullTranscript = '';
        
        // Use provided transcript or accumulated segments
        if (providedTranscript) {
            fullTranscript = providedTranscript;
            console.log(`📝 Processing provided transcript: "${fullTranscript}"`);
        } else if (this.accumulatedTranscript.length > 0) {
            fullTranscript = this.accumulatedTranscript.join(' ');
            console.log(`📝 Processing accumulated transcript (${this.accumulatedTranscript.length} segments): "${fullTranscript}"`);
        } else {
            console.warn('No transcript to process');
            return;
        }
        
        // Check if module configuration affects behavior
        const shouldShowTranscript = this.voiceInputConfig.show_transcript !== false;
        const shouldAllowEditing = this.voiceInputConfig.allow_editing !== false;
        
        // Pass configuration along with full transcript
        this.chatInterface.handleVoiceInput(fullTranscript, 1.0, {
            autoSubmitMode: this.voiceInputConfig.auto_submit_mode || 'confidence',
            showTranscript: shouldShowTranscript,
            allowEditing: shouldAllowEditing,
            isAccumulated: true  // Flag to indicate this is accumulated transcript
        });
        
        // DEFENSIVE: Clear accumulated transcript AFTER processing to ensure availability
        // But NOT if we're in the middle of stopping (to prevent premature clearing)
        if (!this.isStoppingTimedRecording) {
            this.accumulatedTranscript = [];
        }
    }
    
    /**
     * Show low confidence message to user
     */
    showLowConfidenceMessage(transcript, confidence) {
        const message = `I heard "${transcript}" but I'm not confident (${(confidence * 100).toFixed(0)}%). Try speaking more clearly or use the text input.`;
        console.warn(message);
        // Could show this as a temporary message in UI
    }
    
    /**
     * Update microphone button appearance (proper OOP encapsulation)
     */
    updateMicrophoneButton(state) {
        if (!this.microphoneButton) return;
        
        switch (state) {
            case 'recording':
                this.microphoneButton.classList.add('recording');
                this.microphoneButton.title = 'Click to stop recording';
                this.microphoneButton.textContent = '🔴';
                break;
                
            case 'idle':
            case 'error':
            default:
                this.microphoneButton.classList.remove('recording');
                this.microphoneButton.title = 'Click to speak';
                this.microphoneButton.textContent = '🎤';
                break;
        }
    }
    
    /**
     * Set language for speech recognition
     */
    setLanguage(langCode) {
        if (!this.supportedLanguages[langCode]) {
            console.error(`Unsupported language code: ${langCode}`);
            return false;
        }
        
        this.language = langCode;
        
        if (this.recognition) {
            this.recognition.lang = langCode;
            console.log(`🌐 Language changed to ${this.supportedLanguages[langCode]}`);
        }
        
        return true;
    }
    
    /**
     * Update UI elements based on recording state
     */
    updateUI(state) {
        // This will be implemented when we add the UI elements
        console.log(`🎨 UI state: ${state}`);
        
        // Dispatch custom event for UI updates (for backward compatibility)
        const event = new CustomEvent('voiceInputStateChange', {
            detail: { state, isRecording: this.isRecording }
        });
        document.dispatchEvent(event);
    }
    
    
    /**
     * Get current language
     */
    getCurrentLanguage() {
        return {
            code: this.language,
            name: this.supportedLanguages[this.language]
        };
    }
    
    /**
     * Get list of supported languages
     */
    getSupportedLanguages() {
        return { ...this.supportedLanguages };
    }
    
    /**
     * Check if voice input is currently supported and available
     */
    isAvailable() {
        return this.isSupported && !this.isRecording;
    }
    
    /**
     * Destroy voice input and clean up resources
     */
    destroy() {
        if (this.recognition) {
            this.recognition.abort();
            this.recognition = null;
        }
        
        this.isRecording = false;
        console.log('🗑️ VoiceInput destroyed');
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoiceInput;
}