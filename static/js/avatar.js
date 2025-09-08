// Avatar Controller for Lottie-based character animations using bodymovin

class AvatarController {
    constructor(containerId = 'avatar-container', animationFiles = null) {
        this.containerId = containerId; // Store for init method
        this.container = null;
        this.lottieContainer = null;
        this.placeholder = null;
        this.currentState = 'idle';
        this.isInitialized = false;
        this.animationLoaded = false;
        this.currentAnimation = null;
        this.lottieInstance = null;
        this.loadingInstance = null; // Track loading animation for seamless transitions
        
        // Animation states mapping with file paths
        this.states = {
            idle: 'idle',
            thinking: 'thinking',
            speaking: 'speaking',
            listening: 'listening'
        };

        // Animation file mapping - can be overridden by constructor
        this.animationFiles = animationFiles || {
            idle: '/courses/german/static/animations/herr-muller-idle.json',
            thinking: '/courses/german/static/animations/herr-muller-thinking.json',
            speaking: '/courses/german/static/animations/herr-muller-speaking.json',
            listening: '/courses/german/static/animations/herr-muller-idle.json' // Fallback to idle for now
        };
    }

    /**
     * Initialize the avatar controller
     * @param {string} containerId - ID of the HTML container element
     */
    init(containerId = null) {
        try {
            // Use provided containerId or the one from constructor
            const targetContainerId = containerId || this.containerId;
            
            // Check if bodymovin/lottie is available
            if (typeof lottie === 'undefined') {
                console.error('Bodymovin/Lottie library not found. Make sure to include the script.');
                return false;
            }

            this.container = document.getElementById(targetContainerId);
            if (!this.container) {
                console.error('Avatar container not found:', targetContainerId);
                return false;
            }

            // Get Lottie container and placeholder elements
            this.lottieContainer = document.getElementById('avatar-lottie');
            this.placeholder = document.getElementById('avatar-placeholder');
            
            if (!this.lottieContainer) {
                console.error('Lottie container element not found');
                return false;
            }

            console.log('✅ AvatarController initialized successfully with bodymovin');
            console.log('📚 Bodymovin version:', lottie.version);
            this.isInitialized = true;
            
            return true;
        } catch (error) {
            console.error('Error initializing AvatarController:', error);
            return false;
        }
    }

    /**
     * Load a Lottie animation file using bodymovin with seamless transitions
     * @param {string} animationPath - Path to the Lottie JSON file or URL
     */
    loadAnimation(animationPath) {
        if (!this.isInitialized) {
            console.error('AvatarController not initialized');
            return false;
        }

        // Skip if same animation is already loaded
        if (this.currentAnimation === animationPath && this.animationLoaded) {
            console.log('🔄 Animation already loaded:', animationPath);
            return true;
        }

        try {
            console.log('🎬 Loading Lottie animation with seamless transition:', animationPath);
            
            // Cancel any existing loading instance
            if (this.loadingInstance) {
                console.log('🛑 Cancelling previous loading animation');
                this.loadingInstance.destroy();
                this.loadingInstance = null;
            }
            
            // Create a temporary container for the new animation
            const tempContainer = document.createElement('div');
            tempContainer.style.cssText = 'width: 100%; height: 100%; position: absolute; top: 0; left: 0; opacity: 0;';
            this.lottieContainer.appendChild(tempContainer);
            
            // Load new animation in temporary container (invisible)
            this.loadingInstance = lottie.loadAnimation({
                container: tempContainer,
                renderer: 'svg',
                loop: true,
                autoplay: true,
                path: animationPath,
                rendererSettings: {
                    preserveAspectRatio: 'xMidYMid meet'
                }
            });
            
            // Set up event listeners for seamless transition
            this.loadingInstance.addEventListener('DOMLoaded', () => {
                console.log('✅ New animation loaded and ready for seamless switch:', animationPath);
                this._performSeamlessSwitch(animationPath, tempContainer);
            });
            
            this.loadingInstance.addEventListener('data_failed', () => {
                console.error('❌ Animation failed to load:', animationPath);
                // Clean up temp container
                if (tempContainer.parentNode) {
                    tempContainer.parentNode.removeChild(tempContainer);
                }
                this.loadingInstance = null;
                this._handleAnimationError(animationPath);
            });
            
            return true;
        } catch (error) {
            console.error('Error in loadAnimation:', error);
            this._handleAnimationError(animationPath);
            return false;
        }
    }

    /**
     * Perform seamless switch from old animation to new animation
     * @param {string} animationPath - Path of the new animation
     * @param {HTMLElement} tempContainer - Temporary container with loaded animation
     * @private
     */
    _performSeamlessSwitch(animationPath, tempContainer) {
        try {
            console.log('🔄 Performing seamless animation switch to:', animationPath);
            
            // Destroy old animation if it exists
            if (this.lottieInstance) {
                console.log('🗑️ Cleaning up old animation');
                this.lottieInstance.destroy();
            }
            
            // Clear main container (except temp container)
            const children = Array.from(this.lottieContainer.children);
            children.forEach(child => {
                if (child !== tempContainer) {
                    child.remove();
                }
            });
            
            // Move new animation to main position and make visible
            tempContainer.style.cssText = 'width: 100%; height: 100%;'; // Remove opacity and positioning
            
            // Update references
            this.lottieInstance = this.loadingInstance;
            this.loadingInstance = null;
            this.currentAnimation = animationPath;
            this.animationLoaded = true;
            
            // Show the lottie container and hide placeholder
            this._showLottie();
            
            console.log('✨ Seamless animation switch completed successfully');
            
        } catch (error) {
            console.error('Error during seamless switch:', error);
            // Fallback: clean up and show placeholder
            if (tempContainer.parentNode) {
                tempContainer.parentNode.removeChild(tempContainer);
            }
            this.loadingInstance = null;
            this._handleAnimationError(animationPath);
        }
    }

    /**
     * Set the avatar animation state
     * @param {string} state - The state to set (idle, thinking, speaking, listening)
     */
    setState(state) {
        if (!this.isInitialized) {
            console.warn('AvatarController not initialized');
            return;
        }

        if (!this.states[state]) {
            console.warn('Unknown avatar state:', state);
            return;
        }

        console.log('Avatar state changed:', this.currentState, '->', state);
        const previousState = this.currentState;
        this.currentState = state;
        
        // Load the animation for this state if different from current
        const animationPath = this.animationFiles[state];
        if (animationPath && this.currentAnimation !== animationPath) {
            this.loadAnimation(animationPath);
        }
        
        // Update placeholder visual feedback (fallback)
        this._updatePlaceholder(state);
    }

    /**
     * Get the current avatar state
     * @returns {string} Current state
     */
    getCurrentState() {
        return this.currentState;
    }

    /**
     * Check if avatar is initialized
     * @returns {boolean} Initialization status
     */
    isReady() {
        return this.isInitialized;
    }

    /**
     * Show the Lottie animation and hide placeholder
     * @private
     */
    _showLottie() {
        console.log('🎬 Showing Lottie animation:', this.currentAnimation);
        if (this.lottieContainer) {
            this.lottieContainer.style.display = 'block';
            console.log('👁️ Lottie container visibility set to block');
        }
        if (this.placeholder) {
            this.placeholder.style.display = 'none';
            console.log('🫥 Placeholder hidden');
        }
    }

    /**
     * Show the placeholder and hide Lottie animation
     * @private
     */
    _showPlaceholder() {
        if (this.lottieContainer) {
            this.lottieContainer.style.display = 'none';
        }
        if (this.placeholder) {
            this.placeholder.style.display = 'flex';
        }
    }

    /**
     * Update placeholder visual feedback
     * @private
     */
    _updatePlaceholder(state) {
        if (!this.placeholder) return;

        // Add visual feedback for different states
        this.placeholder.className = `avatar-placeholder avatar-${state}`;
        
        const icon = this.placeholder.querySelector('.placeholder-icon');
        const text = this.placeholder.querySelector('.placeholder-text');
        
        if (icon && text) {
            switch (state) {
                case 'thinking':
                    icon.textContent = '🤔';
                    text.textContent = 'Thinking...';
                    break;
                case 'speaking':
                    icon.textContent = '💬';
                    text.textContent = 'Speaking...';
                    break;
                case 'listening':
                    icon.textContent = '👂';
                    text.textContent = 'Listening...';
                    break;
                default:
                    icon.textContent = '👨‍🏫';
                    text.textContent = 'Herr Müller';
            }
        }
    }

    /**
     * Handle animation loading errors with graceful fallback
     * @private
     */
    _handleAnimationError(animationPath) {
        console.warn(`⚠️ Animation failed to load: ${animationPath}`);
        console.warn('🔄 Falling back to placeholder for state:', this.currentState);
        
        this.animationLoaded = false;
        this.currentAnimation = null;
        
        // Destroy failed animation instance
        if (this.lottieInstance) {
            this.lottieInstance.destroy();
            this.lottieInstance = null;
        }
        
        this._showPlaceholder();
        
        // Log helpful message for development
        if (animationPath && animationPath.includes('/static/animations/')) {
            console.info('💡 Make sure your Lottie JSON files are in the /static/animations/ folder');
            console.info('📁 Expected files: herr-muller-idle.json, herr-muller-thinking.json, herr-muller-speaking.json');
        }
    }

    /**
     * Destroy the avatar and clean up resources
     */
    destroy() {
        // Destroy bodymovin animation instances
        if (this.lottieInstance) {
            this.lottieInstance.destroy();
            this.lottieInstance = null;
        }
        
        if (this.loadingInstance) {
            this.loadingInstance.destroy();
            this.loadingInstance = null;
        }
        
        // Clear container
        if (this.lottieContainer) {
            this.lottieContainer.innerHTML = '';
        }
        
        this.container = null;
        this.lottieContainer = null;
        this.placeholder = null;
        this.isInitialized = false;
        this.animationLoaded = false;
        this.currentState = 'idle';
        this.currentAnimation = null;
        
        console.log('🗑️ AvatarController destroyed');
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AvatarController;
}