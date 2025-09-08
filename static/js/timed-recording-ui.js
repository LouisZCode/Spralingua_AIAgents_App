/**
 * TimedRecordingUI - Visual timer interface for voice recording
 * Provides countdown timer and stop button during extended voice input
 */
class TimedRecordingUI {
    constructor(containerElement, config = {}) {
        this.container = containerElement;
        this.config = {
            duration: config.duration || 60000, // Default 1 minute
            style: config.style || 'circular', // 'circular' or 'linear'
            stopButtonText: config.stopButtonText || "I'm Done Speaking",
            onStop: config.onStop || (() => {}),
            onTimeout: config.onTimeout || (() => {}),
            showTranscriptPreview: config.showTranscriptPreview || false
        };
        
        this.originalContent = null;
        this.timerInterval = null;
        this.startTime = null;
        this.remainingTime = this.config.duration;
        this.timerElement = null;
        this.progressElement = null;
    }
    
    show() {
        console.log('⏱️ [TIMED RECORDING UI] Showing timer interface');
        
        // Store original content
        this.originalContent = this.container.innerHTML;
        
        // Replace with timer UI
        this.container.innerHTML = this._buildTimerHTML();
        
        // Get references to elements
        this.timerElement = this.container.querySelector('.timer-text');
        this.progressElement = this.container.querySelector('.progress-fill, .timer-circle-progress');
        
        // Add event listener to stop button
        const stopButton = this.container.querySelector('.stop-recording-button');
        console.log('🔍 [TIMED RECORDING UI] Looking for stop button...');
        console.log('🔍 [TIMED RECORDING UI] Container HTML:', this.container.innerHTML.substring(0, 200));
        
        if (stopButton) {
            console.log('🔘 [TIMED RECORDING UI] Stop button found - disabled state:', stopButton.disabled);
            console.log('🔘 [TIMED RECORDING UI] Stop button HTML:', stopButton.outerHTML);
            console.log('🔘 [TIMED RECORDING UI] Has disabled attribute:', stopButton.hasAttribute('disabled'));
            stopButton.addEventListener('click', (e) => {
                console.log('🖱️ [TIMED RECORDING UI] Stop button click event fired');
                console.log('🖱️ [TIMED RECORDING UI] Button disabled state at click time:', stopButton.disabled);
                
                // Check if button is disabled
                if (stopButton.disabled) {
                    console.log('⚠️ [TIMED RECORDING UI] Stop button is disabled - ignoring click');
                    e.preventDefault();
                    e.stopPropagation();
                    return;
                }
                console.log('🛑 [TIMED RECORDING UI] Stop button clicked - processing stop');
                this.hide();
                this.config.onStop();
            });
        }
        
        // Start countdown
        this._startCountdown();
    }
    
    hide() {
        console.log('⏱️ [TIMED RECORDING UI] Hiding timer interface');
        
        // Stop countdown
        this._stopCountdown();
        
        // Restore original content
        if (this.originalContent) {
            this.container.innerHTML = this.originalContent;
            this.originalContent = null;
        }
    }
    
    _buildTimerHTML() {
        if (this.config.style === 'circular') {
            return this._buildCircularTimer();
        } else {
            return this._buildLinearTimer();
        }
    }
    
    _buildCircularTimer() {
        const timeDisplay = this._formatTime(this.config.duration / 1000);
        
        return `
            <div class="timed-recording-container circular-style">
                <div class="circular-timer">
                    <svg width="120" height="120" viewBox="0 0 120 120">
                        <circle cx="60" cy="60" r="54" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="8"/>
                        <circle class="timer-circle-progress" cx="60" cy="60" r="54" fill="none" 
                                stroke="white" stroke-width="8" 
                                stroke-dasharray="339.292" stroke-dashoffset="0"
                                stroke-linecap="round"/>
                    </svg>
                    <div class="timer-text">${timeDisplay}</div>
                </div>
                <div class="recording-status">
                    <span class="recording-dot"></span>
                    <span class="recording-label">Recording...</span>
                </div>
                <button class="stop-recording-button" disabled>
                    <span class="stop-icon">✓</span>
                    <span>${this.config.stopButtonText}</span>
                </button>
                ${this.config.showTranscriptPreview ? '<div class="transcript-preview"></div>' : ''}
            </div>
        `;
    }
    
    _buildLinearTimer() {
        const timeDisplay = this._formatTime(this.config.duration / 1000);
        
        return `
            <div class="timed-recording-container linear-style">
                <div class="timer-header">
                    <span class="timer-icon">⏱️</span>
                    <span class="timer-text">${timeDisplay}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 100%"></div>
                </div>
                <div class="recording-status">
                    <span class="recording-dot"></span>
                    <span class="recording-label">Recording your response...</span>
                </div>
                <button class="stop-recording-button" disabled>
                    <span class="stop-icon">✓</span>
                    <span>${this.config.stopButtonText}</span>
                </button>
                ${this.config.showTranscriptPreview ? '<div class="transcript-preview"></div>' : ''}
            </div>
        `;
    }
    
    _startCountdown() {
        this.startTime = Date.now();
        
        // Update immediately
        this._updateTimer();
        
        // Update every 100ms for smooth animation
        this.timerInterval = setInterval(() => {
            this._updateTimer();
        }, 100);
    }
    
    _stopCountdown() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }
    
    _updateTimer() {
        const elapsed = Date.now() - this.startTime;
        this.remainingTime = Math.max(0, this.config.duration - elapsed);
        
        // Update time display
        if (this.timerElement) {
            this.timerElement.textContent = this._formatTime(this.remainingTime / 1000);
        }
        
        // Update progress
        const progress = (this.remainingTime / this.config.duration) * 100;
        
        if (this.config.style === 'circular' && this.progressElement) {
            // For circular timer, adjust stroke-dashoffset
            const circumference = 2 * Math.PI * 54; // radius = 54
            const offset = circumference * (1 - progress / 100);
            this.progressElement.style.strokeDashoffset = offset;
        } else if (this.config.style === 'linear' && this.progressElement) {
            // For linear timer, adjust width
            this.progressElement.style.width = `${progress}%`;
        }
        
        // Check if time is up
        if (this.remainingTime === 0) {
            console.log('⏱️ [TIMED RECORDING UI] Time is up!');
            this._stopCountdown();
            this.config.onTimeout();
        }
    }
    
    /**
     * Enable the stop button (called when speech processing is complete)
     */
    enableStopButton() {
        console.log('🔓 [TIMED RECORDING UI] enableStopButton() called');
        console.log('📍 [TIMED RECORDING UI] Container exists:', !!this.container);
        
        const stopButton = this.container.querySelector('.stop-recording-button');
        console.log('🔍 [TIMED RECORDING UI] Stop button found:', !!stopButton);
        
        if (stopButton) {
            console.log('🔓 [TIMED RECORDING UI] Current disabled state:', stopButton.disabled);
            stopButton.disabled = false;
            stopButton.removeAttribute('disabled');  // Extra insurance
            
            // Force style update
            stopButton.style.cursor = 'pointer';
            stopButton.classList.remove('disabled');
            
            console.log('✅ [TIMED RECORDING UI] Stop button enabled - new disabled state:', stopButton.disabled);
            console.log('✅ [TIMED RECORDING UI] Stop button classes:', stopButton.className);
        } else {
            console.error('❌ [TIMED RECORDING UI] Stop button not found in container!');
        }
    }
    
    /**
     * Disable the stop button (called during active speech processing)
     */
    disableStopButton() {
        console.log('🔒 [TIMED RECORDING UI] disableStopButton() called - active speech detected');
        
        const stopButton = this.container.querySelector('.stop-recording-button');
        
        if (stopButton) {
            console.log('🔒 [TIMED RECORDING UI] Disabling stop button during active speech');
            stopButton.disabled = true;
            stopButton.setAttribute('disabled', 'disabled');
            
            // Update styles to show disabled state
            stopButton.style.cursor = 'not-allowed';
            stopButton.classList.add('disabled');
            
            console.log('🔒 [TIMED RECORDING UI] Stop button disabled to prevent interrupting speech');
        }
    }
    
    _formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
    
    updateTranscriptPreview(text) {
        if (this.config.showTranscriptPreview) {
            const previewElement = this.container.querySelector('.transcript-preview');
            if (previewElement) {
                previewElement.textContent = text;
            }
        }
    }
}

// Export for use in other scripts
window.TimedRecordingUI = TimedRecordingUI;