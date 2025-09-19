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
    continueBtn.addEventListener('click', async function() {
        if (selectedInput && selectedTarget && selectedLevel) {
            // Disable button during save
            continueBtn.disabled = true;
            continueBtn.textContent = typeof translationManager !== 'undefined' ? 
                'Saving...' : 'Saving...';
            
            try {
                // Send selections to backend
                const response = await fetch('/api/save-progress', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        input_language: selectedInput,
                        target_language: selectedTarget,
                        current_level: selectedLevel
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Save selections to localStorage for exercises page
                    localStorage.setItem('selectedInputLanguage', selectedInput);
                    localStorage.setItem('selectedTargetLanguage', selectedTarget);
                    localStorage.setItem('selectedLevel', selectedLevel);

                    // Redirect to exercises page
                    window.location.href = '/exercises';
                } else {
                    // Show error message
                    alert('Failed to save progress: ' + (result.error || 'Unknown error'));
                    // Re-enable button
                    continueBtn.disabled = false;
                    continueBtn.textContent = typeof translationManager !== 'undefined' ? 
                        translationManager.getText('continue_btn') : 'Continue';
                }
            } catch (error) {
                console.error('Error saving progress:', error);
                alert('Network error. Please try again.');
                // Re-enable button
                continueBtn.disabled = false;
                continueBtn.textContent = typeof translationManager !== 'undefined' ? 
                    translationManager.getText('continue_btn') : 'Continue';
            }
        }
    });

    // Load previous selections if they exist
    function loadPreviousSelections() {
        // Check if saved progress exists from backend
        if (window.savedProgress) {
            const { input_language, target_language, current_level } = window.savedProgress;
            
            // Pre-select input language
            if (input_language) {
                const inputCard = document.querySelector(`#input-languages .language-card[data-lang="${input_language}"]`);
                if (inputCard) {
                    inputCard.classList.add('selected');
                    selectedInput = input_language;
                    
                    // Update page language
                    if (typeof translationManager !== 'undefined') {
                        translationManager.setLanguage(input_language);
                    }
                }
            }
            
            // Pre-select target language
            if (target_language) {
                const targetCard = document.querySelector(`#target-languages .language-card[data-lang="${target_language}"]`);
                if (targetCard) {
                    targetCard.classList.add('selected');
                    selectedTarget = target_language;
                }
            }
            
            // Pre-select level
            if (current_level) {
                const levelCard = document.querySelector(`#level-selection .level-card[data-level="${current_level}"]`);
                if (levelCard) {
                    levelCard.classList.add('selected');
                    selectedLevel = current_level;
                }
            }
            
            // Update displays
            updateSelectionDisplay();
            checkContinueButton();
        }
    }

    // Initialize
    loadPreviousSelections();
});