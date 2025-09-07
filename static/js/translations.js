// Multilingual Translation System for Spralingua

const translations = {
    english: {
        // Navigation
        nav_dashboard: "Dashboard",
        nav_logout: "Logout",
        nav_login: "Login",
        nav_signup: "Sign up",
        
        // Dashboard Headers
        welcome: "Welcome back!",
        choose_path: "Choose your learning path",
        
        // Language Selection
        i_speak: "I speak...",
        i_want_learn: "I want to learn...",
        my_level: "My current level is...",
        
        // Languages
        lang_english: "English",
        lang_german: "German",
        lang_spanish: "Spanish",
        lang_portuguese: "Portuguese",
        
        // Level Descriptions
        level_a1: "A1",
        level_a2: "A2",
        level_b1: "B1",
        level_b2: "B2",
        a1_desc: "Beginner - Basic phrases and vocabulary",
        a2_desc: "Elementary - Simple everyday conversations",
        b1_desc: "Intermediate - Can handle most situations",
        b2_desc: "Upper-Intermediate - Fluent in complex topics",
        
        // Buttons
        continue_btn: "Continue",
        
        // Selection Display
        learning_display: "Learning {target} from {input} at {level} level",
        
        // Error Messages (kept in English for devs)
        same_language_error: "You cannot select the same language for both input and target!"
    },
    
    german: {
        // Navigation
        nav_dashboard: "Dashboard",
        nav_logout: "Abmelden",
        nav_login: "Anmelden",
        nav_signup: "Registrieren",
        
        // Dashboard Headers
        welcome: "Willkommen zurück!",
        choose_path: "Wähle deinen Lernpfad",
        
        // Language Selection
        i_speak: "Ich spreche...",
        i_want_learn: "Ich möchte lernen...",
        my_level: "Mein aktuelles Niveau ist...",
        
        // Languages
        lang_english: "Englisch",
        lang_german: "Deutsch",
        lang_spanish: "Spanisch",
        lang_portuguese: "Portugiesisch",
        
        // Level Descriptions
        level_a1: "A1",
        level_a2: "A2",
        level_b1: "B1",
        level_b2: "B2",
        a1_desc: "Anfänger - Grundlegende Phrasen und Vokabeln",
        a2_desc: "Grundstufe - Einfache Alltagsgespräche",
        b1_desc: "Mittelstufe - Kann die meisten Situationen bewältigen",
        b2_desc: "Obere Mittelstufe - Fließend in komplexen Themen",
        
        // Buttons
        continue_btn: "Weiter",
        
        // Selection Display
        learning_display: "Lerne {target} von {input} auf {level} Niveau",
        
        // Error Messages
        same_language_error: "You cannot select the same language for both input and target!"
    },
    
    spanish: {
        // Navigation
        nav_dashboard: "Panel",
        nav_logout: "Cerrar sesión",
        nav_login: "Iniciar sesión",
        nav_signup: "Registrarse",
        
        // Dashboard Headers
        welcome: "¡Bienvenido de nuevo!",
        choose_path: "Elige tu camino de aprendizaje",
        
        // Language Selection
        i_speak: "Yo hablo...",
        i_want_learn: "Quiero aprender...",
        my_level: "Mi nivel actual es...",
        
        // Languages
        lang_english: "Inglés",
        lang_german: "Alemán",
        lang_spanish: "Español",
        lang_portuguese: "Portugués",
        
        // Level Descriptions
        level_a1: "A1",
        level_a2: "A2",
        level_b1: "B1",
        level_b2: "B2",
        a1_desc: "Principiante - Frases básicas y vocabulario",
        a2_desc: "Elemental - Conversaciones cotidianas simples",
        b1_desc: "Intermedio - Puede manejar la mayoría de situaciones",
        b2_desc: "Intermedio alto - Fluido en temas complejos",
        
        // Buttons
        continue_btn: "Continuar",
        
        // Selection Display
        learning_display: "Aprendiendo {target} desde {input} en nivel {level}",
        
        // Error Messages
        same_language_error: "You cannot select the same language for both input and target!"
    },
    
    portuguese: {
        // Navigation
        nav_dashboard: "Painel",
        nav_logout: "Sair",
        nav_login: "Entrar",
        nav_signup: "Cadastrar-se",
        
        // Dashboard Headers
        welcome: "Bem-vindo de volta!",
        choose_path: "Escolha seu caminho de aprendizagem",
        
        // Language Selection
        i_speak: "Eu falo...",
        i_want_learn: "Quero aprender...",
        my_level: "Meu nível atual é...",
        
        // Languages
        lang_english: "Inglês",
        lang_german: "Alemão",
        lang_spanish: "Espanhol",
        lang_portuguese: "Português",
        
        // Level Descriptions
        level_a1: "A1",
        level_a2: "A2",
        level_b1: "B1",
        level_b2: "B2",
        a1_desc: "Iniciante - Frases básicas e vocabulário",
        a2_desc: "Elementar - Conversas cotidianas simples",
        b1_desc: "Intermediário - Pode lidar com a maioria das situações",
        b2_desc: "Intermediário superior - Fluente em tópicos complexos",
        
        // Buttons
        continue_btn: "Continuar",
        
        // Selection Display
        learning_display: "Aprendendo {target} de {input} no nível {level}",
        
        // Error Messages
        same_language_error: "You cannot select the same language for both input and target!"
    }
};

// Translation Manager Class
class TranslationManager {
    constructor() {
        this.currentLanguage = localStorage.getItem('userLanguage') || 'english';
        this.translations = translations;
    }
    
    // Set and save language preference
    setLanguage(language) {
        if (this.translations[language]) {
            this.currentLanguage = language;
            localStorage.setItem('userLanguage', language);
            this.updatePageText();
        }
    }
    
    // Get current language
    getCurrentLanguage() {
        return this.currentLanguage;
    }
    
    // Get a specific translation
    getText(key) {
        return this.translations[this.currentLanguage][key] || 
               this.translations['english'][key] || 
               key;
    }
    
    // Update all elements with data-translate attribute
    updatePageText() {
        const elements = document.querySelectorAll('[data-translate]');
        elements.forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.getText(key);
            
            if (translation) {
                // Check if it's a placeholder attribute or text content
                if (element.hasAttribute('placeholder')) {
                    element.placeholder = translation;
                } else if (element.hasAttribute('aria-label')) {
                    element.setAttribute('aria-label', translation);
                } else {
                    element.textContent = translation;
                }
            }
        });
        
        // Update any dynamic content
        this.updateDynamicContent();
    }
    
    // Update dynamic content like selection display
    updateDynamicContent() {
        // This will be called from dashboard.js for dynamic updates
    }
    
    // Format string with placeholders
    formatString(template, values) {
        let result = template;
        for (const [key, value] of Object.entries(values)) {
            result = result.replace(`{${key}}`, value);
        }
        return result;
    }
    
    // Initialize on page load
    init() {
        // Load saved language and update page
        this.updatePageText();
    }
}

// Create global instance
const translationManager = new TranslationManager();

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        translationManager.init();
    });
} else {
    translationManager.init();
}