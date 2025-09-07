// Dashboard JavaScript - Language Selection Logic

document.addEventListener('DOMContentLoaded', function() {
    // State management
    let selectedInput = null;
    let selectedTarget = null;
    let selectedLevel = null;
    
    // Check if translation manager exists
    if (typeof translationManager !== 'undefined') {
        // Load saved language preference
        const savedLanguage = localStorage.getItem('userLanguage');
        if (savedLanguage) {
            selectedInput = savedLanguage;
            // Pre-select the saved language
            const savedCard = document.querySelector(`#input-languages .language-card[data-lang="${savedLanguage}"]`);
            if (savedCard) {
                savedCard.classList.add('selected');
            }
        }
    }

    // DOM elements
    const inputLanguages = document.getElementById('input-languages');
    const targetLanguages = document.getElementById('target-languages');
    const levelSelection = document.getElementById('level-selection');
    const continueBtn = document.getElementById('continue-btn');
    const selectionDisplay = document.getElementById('selection-display');
    const errorMessage = document.getElementById('error-message');
    const inputDisplay = document.getElementById('input-display');
    const targetDisplay = document.getElementById('target-display');
    const levelDisplay = document.getElementById('level-display');

    // Handle input language selection
    inputLanguages.addEventListener('click', function(e) {
        const card = e.target.closest('.language-card');
        if (!card) return;

        // Remove previous selection
        inputLanguages.querySelectorAll('.language-card').forEach(c => {
            c.classList.remove('selected');
        });

        // Add selection
        card.classList.add('selected');
        selectedInput = card.dataset.lang;
        
        // Update page language immediately
        if (typeof translationManager !== 'undefined') {
            translationManager.setLanguage(selectedInput);
        }

        // Check for same language conflict
        checkLanguageConflict();
        updateSelectionDisplay();
        checkContinueButton();
    });

    // Handle target language selection
    targetLanguages.addEventListener('click', function(e) {
        const card = e.target.closest('.language-card');
        if (!card) return;

        // Check if same as input language
        if (selectedInput && card.dataset.lang === selectedInput) {
            showError();
            return;
        }

        // Remove previous selection
        targetLanguages.querySelectorAll('.language-card').forEach(c => {
            c.classList.remove('selected');
        });

        // Add selection
        card.classList.add('selected');
        selectedTarget = card.dataset.lang;

        hideError();
        updateSelectionDisplay();
        checkContinueButton();
    });

    // Handle level selection
    levelSelection.addEventListener('click', function(e) {
        const card = e.target.closest('.level-card');
        if (!card) return;

        // Remove previous selection
        levelSelection.querySelectorAll('.level-card').forEach(c => {
            c.classList.remove('selected');
        });

        // Add selection
        card.classList.add('selected');
        selectedLevel = card.dataset.level;

        updateSelectionDisplay();
        checkContinueButton();
    });

    // Check for language conflict
    function checkLanguageConflict() {
        if (selectedInput && selectedTarget && selectedInput === selectedTarget) {
            // Deselect target language
            targetLanguages.querySelectorAll('.language-card').forEach(c => {
                c.classList.remove('selected');
            });
            selectedTarget = null;
            showError();
        }
    }

    // Show error message
    function showError() {
        errorMessage.style.display = 'block';
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 3000);
    }

    // Hide error message
    function hideError() {
        errorMessage.style.display = 'none';
    }

    // Update selection display
    function updateSelectionDisplay() {
        if (selectedInput || selectedTarget || selectedLevel) {
            selectionDisplay.style.display = 'block';
            
            // Get translated language names if translation manager exists
            if (typeof translationManager !== 'undefined') {
                const inputLang = selectedInput ? 
                    translationManager.getText(`lang_${selectedInput}`) : '---';
                const targetLang = selectedTarget ? 
                    translationManager.getText(`lang_${selectedTarget}`) : '---';
                
                inputDisplay.textContent = inputLang;
                targetDisplay.textContent = targetLang;
                levelDisplay.textContent = selectedLevel || '---';
                
                // Update the entire selection text with translation
                const template = translationManager.getText('learning_display');
                if (selectedInput && selectedTarget && selectedLevel) {
                    const formatted = translationManager.formatString(template, {
                        input: inputLang,
                        target: targetLang,
                        level: selectedLevel
                    });
                    document.querySelector('.selection-text').innerHTML = formatted;
                }
            } else {
                // Fallback to English
                inputDisplay.textContent = selectedInput ? 
                    selectedInput.charAt(0).toUpperCase() + selectedInput.slice(1) : '---';
                targetDisplay.textContent = selectedTarget ? 
                    selectedTarget.charAt(0).toUpperCase() + selectedTarget.slice(1) : '---';
                levelDisplay.textContent = selectedLevel || '---';
            }
        } else {
            selectionDisplay.style.display = 'none';
        }
    }

    // Check if continue button should be enabled
    function checkContinueButton() {
        if (selectedInput && selectedTarget && selectedLevel) {
            continueBtn.disabled = false;
        } else {
            continueBtn.disabled = true;
        }
    }

    // Handle continue button click
    continueBtn.addEventListener('click', function() {
        if (selectedInput && selectedTarget && selectedLevel) {
            // Save selections to session/database (will be implemented later)
            console.log('Selections:', {
                input: selectedInput,
                target: selectedTarget,
                level: selectedLevel
            });

            // For now, just show an alert
            alert(`Great! You'll be learning ${selectedTarget} from ${selectedInput} at ${selectedLevel} level.\n\nThis feature will be implemented soon!`);
        }
    });

    // Load previous selections if they exist (to be implemented with backend)
    function loadPreviousSelections() {
        // This will be connected to backend later
        // For now, we'll just leave it empty
    }

    // Initialize
    loadPreviousSelections();
});