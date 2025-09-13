/**
 * ListeningModeManager - Manages blur/reveal functionality for listening comprehension
 * Encourages students to focus on listening before reading text responses
 */
class ListeningModeManager {
    constructor(config = {}) {
        this.config = {
            enabled: config.enabled !== false,
            mode: config.mode || 'always', // 'always', 'delayed', 'adaptive'
            buttonText: config.buttonText || '📖 Let me read what Harry said',
            blurIntensity: config.blurIntensity || 8,
            delaySeconds: config.delaySeconds || 5,
            trackUsage: config.trackUsage !== false,
            minListenTime: config.minListenTime || 0, // Minimum time before allowing reveal
            adaptiveThresholds: config.adaptiveThresholds || {
                beginner: 0,
                intermediate: 3,
                advanced: -1 // Never show
            }
        };
        
        // Analytics tracking
        this.revealStats = {
            totalMessages: 0,
            messagesRevealed: 0,
            averageRevealTime: 0,
            revealTimes: []
        };
        
        // Track message timestamps for delayed reveal
        this.messageTimestamps = new Map();
        
        console.log('📚 ListeningModeManager initialized with config:', this.config);
    }
    
    /**
     * Check if blur should be applied based on configuration
     */
    isEnabled() {
        return this.config.enabled;
    }
    
    /**
     * Apply blur effect to a message element
     * @param {HTMLElement} messageElement - The message content element
     * @param {number} messageIndex - Index of this message in conversation
     * @returns {HTMLElement} The wrapper element containing button and message
     */
    applyBlurToMessage(messageElement, messageIndex = 0) {
        if (!this.isEnabled()) {
            return messageElement;
        }
        
        console.log('🌫️ Applying blur to assistant message');
        
        // Create wrapper for button and message
        const wrapper = document.createElement('div');
        wrapper.className = 'message-blur-wrapper';
        
        // Add blur class to message content
        messageElement.classList.add('listening-blur');
        
        // Create reveal button
        const button = this.createRevealButton(messageIndex);
        
        // Handle different modes
        if (this.config.mode === 'delayed') {
            this.setupDelayedReveal(button, messageIndex);
        } else if (this.config.mode === 'adaptive') {
            this.setupAdaptiveReveal(button, messageIndex);
        } else if (this.config.mode === 'audio-sync') {
            // For audio-sync mode, use the delayed button method
            return this.applyBlurWithDelayedButton(messageElement, messageIndex);
        }
        
        // Add message first, then button (so button overlays on top)
        wrapper.appendChild(messageElement);
        wrapper.appendChild(button);
        
        // Track message for analytics
        this.revealStats.totalMessages++;
        this.messageTimestamps.set(messageIndex, Date.now());
        
        return wrapper;
    }
    
    /**
     * Apply blur with delayed button for audio-sync mode
     * @param {HTMLElement} messageElement - The message content element
     * @param {number} messageIndex - Index of this message in conversation
     * @returns {HTMLElement} The wrapper element with hidden button
     */
    applyBlurWithDelayedButton(messageElement, messageIndex = 0) {
        console.log('🎵 Applying blur with delayed button (audio-sync mode)');
        
        // Create wrapper for button and message
        const wrapper = document.createElement('div');
        wrapper.className = 'message-blur-wrapper';
        
        // Add blur class to message content
        messageElement.classList.add('listening-blur');
        
        // Create button but keep it hidden
        const button = this.createRevealButton(messageIndex);
        button.style.display = 'none';
        button.dataset.delayed = 'true';
        
        // Store reference for later
        wrapper.dataset.buttonRef = messageIndex;
        
        // Add message first, then button (so button overlays on top)
        wrapper.appendChild(messageElement);
        wrapper.appendChild(button);
        
        // Track message for analytics
        this.revealStats.totalMessages++;
        this.messageTimestamps.set(messageIndex, Date.now());
        
        return wrapper;
    }
    
    /**
     * Show the reveal button after audio ends
     * @param {HTMLElement} wrapperElement - The wrapper containing the hidden button
     */
    showRevealButton(wrapperElement) {
        const button = wrapperElement.querySelector('.reveal-text-btn');
        if (button && button.dataset.delayed === 'true') {
            // Update button text to localized "Read"
            const readText = window.translationManager?.getText('read') || 'Read';
            button.innerHTML = readText;
            
            // Show with animation
            button.style.display = 'block';
            button.classList.add('delayed-appear');
            button.dataset.delayed = 'false';
            
            console.log('📖 Read button appeared after audio');
        }
    }
    
    /**
     * Create the reveal button
     */
    createRevealButton(messageIndex) {
        const button = document.createElement('button');
        button.className = 'reveal-text-btn';
        button.innerHTML = this.config.buttonText;
        button.setAttribute('data-message-index', messageIndex);
        
        // Add click handler
        button.addEventListener('click', (e) => {
            const messageContent = e.target.parentElement.querySelector('.message-content');
            this.handleReveal(messageContent, button, messageIndex);
        });
        
        return button;
    }
    
    /**
     * Handle reveal button click
     */
    handleReveal(messageElement, button, messageIndex) {
        console.log('👁️ Revealing message text');
        
        // Calculate time before reveal
        const messageTime = this.messageTimestamps.get(messageIndex);
        const revealTime = messageTime ? (Date.now() - messageTime) / 1000 : 0;
        
        // Remove blur with smooth transition
        messageElement.classList.remove('listening-blur');
        messageElement.style.filter = 'blur(0)';
        
        // Hide button with fade effect
        button.style.opacity = '0';
        button.style.pointerEvents = 'none';
        setTimeout(() => {
            button.style.display = 'none';
        }, 300);
        
        // Track usage
        if (this.config.trackUsage) {
            this.trackRevealUsage(messageIndex, revealTime);
        }
    }
    
    /**
     * Track reveal button usage for analytics
     */
    trackRevealUsage(messageIndex, revealTime) {
        this.revealStats.messagesRevealed++;
        this.revealStats.revealTimes.push(revealTime);
        
        // Calculate average reveal time
        const sum = this.revealStats.revealTimes.reduce((a, b) => a + b, 0);
        this.revealStats.averageRevealTime = sum / this.revealStats.revealTimes.length;
        
        // Log analytics
        console.log(`📊 Message ${messageIndex} revealed after ${revealTime.toFixed(1)}s`);
        console.log(`📊 Reveal rate: ${this.revealStats.messagesRevealed}/${this.revealStats.totalMessages} (${(this.revealStats.messagesRevealed/this.revealStats.totalMessages*100).toFixed(0)}%)`);
        console.log(`📊 Average reveal time: ${this.revealStats.averageRevealTime.toFixed(1)}s`);
    }
    
    /**
     * Setup delayed reveal for button
     */
    setupDelayedReveal(button, messageIndex) {
        // Initially hide button
        button.style.display = 'none';
        
        // Show after delay
        setTimeout(() => {
            button.style.display = 'block';
            button.style.animation = 'fadeIn 0.3s ease-in';
            console.log(`⏱️ Reveal button available after ${this.config.delaySeconds}s delay`);
        }, this.config.delaySeconds * 1000);
    }
    
    /**
     * Setup adaptive reveal based on user level
     */
    setupAdaptiveReveal(button, messageIndex) {
        // Get user level from session or default to beginner
        const userLevel = window.userLevel || 'beginner';
        const delay = this.config.adaptiveThresholds[userLevel];
        
        if (delay < 0) {
            // Never show button for advanced users
            button.style.display = 'none';
            console.log('🎓 Advanced mode: No reveal button available');
        } else if (delay > 0) {
            // Delayed reveal for intermediate
            this.config.delaySeconds = delay;
            this.setupDelayedReveal(button, messageIndex);
        }
        // delay === 0 means show immediately (beginner)
    }
    
    /**
     * Get current analytics/statistics
     */
    getStats() {
        return {
            ...this.revealStats,
            revealPercentage: this.revealStats.totalMessages > 0 
                ? (this.revealStats.messagesRevealed / this.revealStats.totalMessages * 100).toFixed(1)
                : 0
        };
    }
    
    /**
     * Reset statistics (for new conversation)
     */
    resetStats() {
        this.revealStats = {
            totalMessages: 0,
            messagesRevealed: 0,
            averageRevealTime: 0,
            revealTimes: []
        };
        this.messageTimestamps.clear();
        console.log('📊 Listening mode statistics reset');
    }
}

// Export for use in other scripts
window.ListeningModeManager = ListeningModeManager;
console.log('✅ ListeningModeManager loaded and ready');