// Hint Display Manager for Casual Chat
// Manages inline hint display above microphone with color coding

class HintDisplay {
    constructor() {
        this.inlineContainer = null;
        this.inlineContent = null;
        this.mobileButton = null;
        this.currentHint = null;
        this.isMobile = false;
        this.isExpanded = false;

        this.init();
    }

    init() {
        // Get DOM elements
        this.inlineContainer = document.getElementById('inline-hint');
        this.inlineContent = document.getElementById('inline-hint-content');
        this.mobileButton = document.getElementById('mobile-hint-btn');

        // Check if mobile
        this.checkMobile();

        // Add resize listener for responsive behavior
        window.addEventListener('resize', () => this.checkMobile());

        // Setup mobile button click handler
        if (this.mobileButton) {
            this.mobileButton.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleMobileHint();
            });
        }

        console.log('[HINT DISPLAY] Initialized');
    }

    checkMobile() {
        this.isMobile = window.innerWidth <= 768;
    }

    show(hintData) {
        console.log('[HINT DISPLAY] show() called with:', hintData);
        console.log('[HINT DISPLAY] Hint type received:', hintData.type);
        console.log('[HINT DISPLAY] Hint phrase:', hintData.phrase);
        console.log('[HINT DISPLAY] Hint text:', hintData.hint);
        console.log('[HINT DISPLAY] Container element:', this.inlineContainer);
        console.log('[HINT DISPLAY] Content element:', this.inlineContent);

        if (!this.inlineContainer || !this.inlineContent) {
            console.warn('[HINT DISPLAY] Container elements not found');
            console.log('[HINT DISPLAY] inlineContainer:', this.inlineContainer);
            console.log('[HINT DISPLAY] inlineContent:', this.inlineContent);
            return false;
        }

        // Store current hint
        this.currentHint = hintData;

        // Determine color class based on type
        let colorClass = 'hint-warning'; // Default
        if (hintData.type === 'praise') {
            colorClass = 'hint-praise';
        } else if (hintData.type === 'error') {
            colorClass = 'hint-error';
        }

        // Get translations
        const tm = window.translationManager;
        const getText = tm ? (key) => tm.getText(key) : (key) => key;

        // Format hint content based on type
        let hintHTML = '';
        let headerText = '';

        if (hintData.type === 'praise') {
            // Praise: Show header and praise text, no phrase
            headerText = getText('hint_well_done');
            hintHTML = `<div class="hint-header hint-header-praise">${headerText}</div>`;
            if (hintData.hint) {
                const praiseLabel = getText('hint_praise_label');
                hintHTML += `<strong>${praiseLabel}</strong> ${hintData.hint}`;
            }
        } else if (hintData.type === 'warning') {
            // Warning: Show header, phrase, and tip
            headerText = getText('hint_warning');
            hintHTML = `<div class="hint-header hint-header-warning">${headerText}</div>`;
            if (hintData.phrase) {
                const phraseLabel = getText('hint_phrase_label');
                hintHTML += `<strong>${phraseLabel}</strong> "${hintData.phrase}"<br>`;
            }
            if (hintData.hint) {
                const tipLabel = getText('hint_tip_label');
                hintHTML += `<strong>${tipLabel}</strong> ${hintData.hint}`;
            }
        } else if (hintData.type === 'error') {
            // Error: Show header, phrase, and correction
            headerText = getText('hint_error');
            hintHTML = `<div class="hint-header hint-header-error">${headerText}</div>`;
            if (hintData.phrase) {
                const phraseLabel = getText('hint_phrase_label');
                hintHTML += `<strong>${phraseLabel}</strong> "${hintData.phrase}"<br>`;
            }
            if (hintData.hint) {
                const correctionLabel = getText('hint_correction_label');
                hintHTML += `<strong>${correctionLabel}</strong> ${hintData.hint}`;
            }
        } else {
            // Fallback: If type is missing or unrecognized, show the hint anyway
            console.warn('[HINT DISPLAY] Unknown hint type:', hintData.type);
            console.log('[HINT DISPLAY] Full hint data:', hintData);

            // Default to warning style and show whatever we have
            colorClass = 'hint-warning';
            if (hintData.phrase) {
                hintHTML += `<strong>Phrase:</strong> "${hintData.phrase}"<br>`;
            }
            if (hintData.hint) {
                hintHTML += `<strong>Tip:</strong> ${hintData.hint}`;
            }

            // If we have nothing to show, display a debug message
            if (!hintHTML) {
                hintHTML = `<em>Hint data received but no content to display</em>`;
                console.error('[HINT DISPLAY] No displayable content in hint data:', hintData);
            }
        }

        console.log('[HINT DISPLAY] Setting HTML content:', hintHTML);
        console.log('[HINT DISPLAY] Hint type:', hintData.type);
        console.log('[HINT DISPLAY] Full hint data:', JSON.stringify(hintData));

        // Set content
        this.inlineContent.innerHTML = hintHTML;

        // Remove all color classes and add the appropriate one
        this.inlineContainer.classList.remove('hint-praise', 'hint-warning', 'hint-error');
        this.inlineContainer.classList.add(colorClass);

        console.log('[HINT DISPLAY] Is mobile?', this.isMobile);
        console.log('[HINT DISPLAY] Window width:', window.innerWidth);

        // Handle mobile vs desktop display
        if (this.isMobile) {
            // Show button instead of full hint on mobile
            console.log('[HINT DISPLAY] Showing mobile button');
            this.showMobileButton();
        } else {
            // Show full hint on desktop
            console.log('[HINT DISPLAY] Setting display to block');
            this.inlineContainer.style.display = 'block';
            console.log('[HINT DISPLAY] Current display style:', this.inlineContainer.style.display);
            console.log('[HINT DISPLAY] Container visible?', this.inlineContainer.offsetHeight > 0);

            // More detailed visibility check
            const computedStyle = window.getComputedStyle(this.inlineContainer);
            console.log('[HINT DISPLAY] Computed display:', computedStyle.display);
            console.log('[HINT DISPLAY] Computed visibility:', computedStyle.visibility);
            console.log('[HINT DISPLAY] Computed opacity:', computedStyle.opacity);
            console.log('[HINT DISPLAY] Container offsetHeight:', this.inlineContainer.offsetHeight);
            console.log('[HINT DISPLAY] Container clientHeight:', this.inlineContainer.clientHeight);
            console.log('[HINT DISPLAY] Container scrollHeight:', this.inlineContainer.scrollHeight);
            console.log('[HINT DISPLAY] Parent element:', this.inlineContainer.parentElement);
            console.log('[HINT DISPLAY] Parent display:', this.inlineContainer.parentElement ? window.getComputedStyle(this.inlineContainer.parentElement).display : 'N/A');

            this.inlineContainer.classList.remove('mobile-collapsed', 'mobile-expanded');
        }

        console.log(`[HINT DISPLAY] Showing hint with type: ${hintData.type}`);
        return true;
    }

    hide() {
        if (this.inlineContainer) {
            this.inlineContainer.style.display = 'none';
        }
        if (this.mobileButton) {
            this.mobileButton.style.display = 'none';
            this.mobileButton.classList.remove('expanded');
        }
        this.isExpanded = false;
        this.currentHint = null;

        console.log('[HINT DISPLAY] Hidden');
    }

    showMobileButton() {
        if (!this.mobileButton) return;

        // Hide full hint, show button
        this.inlineContainer.style.display = 'none';
        this.inlineContainer.classList.add('mobile-collapsed');
        this.mobileButton.style.display = 'block';
        this.isExpanded = false;
        this.mobileButton.classList.remove('expanded');

        // Update button text based on hint type
        const mobileHintText = document.getElementById('mobile-hint-text');
        if (mobileHintText && this.currentHint) {
            if (this.currentHint.type === 'praise') {
                mobileHintText.textContent = 'Great job!';
            } else if (this.currentHint.type === 'error') {
                mobileHintText.textContent = 'Tip available';
            } else {
                mobileHintText.textContent = 'Hint';
            }
        }
    }

    toggleMobileHint() {
        if (!this.inlineContainer || !this.mobileButton) return;

        this.isExpanded = !this.isExpanded;

        if (this.isExpanded) {
            // Show full hint
            this.inlineContainer.classList.remove('mobile-collapsed');
            this.inlineContainer.classList.add('mobile-expanded');
            this.inlineContainer.style.display = 'block';
            this.mobileButton.classList.add('expanded');
        } else {
            // Hide full hint
            this.inlineContainer.classList.add('mobile-collapsed');
            this.inlineContainer.classList.remove('mobile-expanded');
            this.inlineContainer.style.display = 'none';
            this.mobileButton.classList.remove('expanded');
        }
    }

    isVisible() {
        return (this.inlineContainer && this.inlineContainer.style.display !== 'none') ||
               (this.mobileButton && this.mobileButton.style.display !== 'none');
    }
}

// Create global instance
window.hintDisplay = null;

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.hintDisplay = new HintDisplay();
    });
} else {
    window.hintDisplay = new HintDisplay();
}