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
        back_to_dashboard: "Back to Language Selection",
        back_to_exercises: "Back to Exercises",
        
        // Selection Display
        learning_display: "Learning {target} from {input} at {level} level",
        
        // Error Messages (kept in English for devs)
        same_language_error: "You cannot select the same language for both input and target!",
        
        // Exercises Page
        learning_hub: "Learning Hub",
        learning_journey: "Your personalized language learning journey",
        practice_modules: "Practice Modules",
        conversation_practice: "Conversation Practice",
        writing_practice: "Writing Practice",
        casual_chat: "Casual Chat",
        everyday_conversations: "Everyday conversations",
        email_writing: "Email Writing",
        professional_emails: "Professional emails",
        fill_blanks: "Fill the Blanks",
        grammar_practice: "Grammar practice",
        ready_practice: "Ready to practice",
        
        // Casual Chat Page
        casual_conversation_practice: "Casual Conversation Practice",
        practice_everyday: "Practice everyday conversations in a relaxed setting. Let's chat about daily life, hobbies, and interests!",
        start_chatting: "Start Chatting",
        choose_partner: "Choose Your Conversation Partner",
        select_practice_today: "Select who you'd like to practice with today:",
        chat_with_harry: "Chat with Harry",
        chat_with_sally: "Chat with Sally",
        surprise_me: "Surprise Me!",
        ai_chat_partner: "AI Chat Partner",
        messages_sent: "messages sent",
        harry_description: "Cheerful snowboard instructor who loves parties and sports",
        sally_description: "Thoughtful librarian who finds beauty in melancholy",
        chat_partner_placeholder: "Chat Partner",
        practicing_label: "Practicing:"
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
        back_to_dashboard: "Zurück zur Sprachauswahl",
        back_to_exercises: "Zurück zu Übungen",
        
        // Selection Display
        learning_display: "Lerne {target} von {input} auf {level} Niveau",
        
        // Error Messages
        same_language_error: "You cannot select the same language for both input and target!",
        
        // Exercises Page
        learning_hub: "Lernzentrum",
        learning_journey: "Deine personalisierte Sprachlernreise",
        practice_modules: "Übungsmodule",
        conversation_practice: "Konversationsübung",
        writing_practice: "Schreibübung",
        casual_chat: "Lockerer Chat",
        everyday_conversations: "Alltagsgespräche",
        email_writing: "E-Mail schreiben",
        professional_emails: "Professionelle E-Mails",
        fill_blanks: "Lücken füllen",
        grammar_practice: "Grammatikübung",
        ready_practice: "Bereit zum Üben",
        
        // Casual Chat Page
        casual_conversation_practice: "Lockere Konversationsübung",
        practice_everyday: "Übe Alltagsgespräche in entspannter Atmosphäre. Lass uns über das tägliche Leben, Hobbys und Interessen plaudern!",
        start_chatting: "Chat starten",
        choose_partner: "Wähle deinen Gesprächspartner",
        select_practice_today: "Wähle aus, mit wem du heute üben möchtest:",
        chat_with_harry: "Mit Harry chatten",
        chat_with_sally: "Mit Sally chatten",
        surprise_me: "Überrasche mich!",
        ai_chat_partner: "KI-Chatpartner",
        messages_sent: "Nachrichten gesendet",
        harry_description: "Fröhlicher Snowboardlehrer, der Partys und Sport liebt",
        sally_description: "Nachdenkliche Bibliothekarin, die Schönheit in der Melancholie findet",
        chat_partner_placeholder: "Chatpartner",
        practicing_label: "Übe:"
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
        back_to_dashboard: "Volver a Selección de Idioma",
        back_to_exercises: "Volver a Ejercicios",
        
        // Selection Display
        learning_display: "Aprendiendo {target} desde {input} en nivel {level}",
        
        // Error Messages
        same_language_error: "You cannot select the same language for both input and target!",
        
        // Exercises Page
        learning_hub: "Centro de Aprendizaje",
        learning_journey: "Tu viaje personalizado de aprendizaje de idiomas",
        practice_modules: "Módulos de Práctica",
        conversation_practice: "Práctica de Conversación",
        writing_practice: "Práctica de Escritura",
        casual_chat: "Chat Casual",
        everyday_conversations: "Conversaciones cotidianas",
        email_writing: "Escribir Correos",
        professional_emails: "Correos profesionales",
        fill_blanks: "Llenar los Espacios",
        grammar_practice: "Práctica de gramática",
        ready_practice: "Listo para practicar",
        
        // Casual Chat Page
        casual_conversation_practice: "Práctica de Conversación Casual",
        practice_everyday: "Practica conversaciones cotidianas en un ambiente relajado. ¡Hablemos sobre la vida diaria, pasatiempos e intereses!",
        start_chatting: "Empezar a Chatear",
        choose_partner: "Elige tu Compañero de Conversación",
        select_practice_today: "Selecciona con quién te gustaría practicar hoy:",
        chat_with_harry: "Chatear con Harry",
        chat_with_sally: "Chatear con Sally",
        surprise_me: "¡Sorpréndeme!",
        ai_chat_partner: "Compañero de Chat IA",
        messages_sent: "mensajes enviados",
        harry_description: "Alegre instructor de snowboard que ama las fiestas y los deportes",
        sally_description: "Bibliotecaria reflexiva que encuentra belleza en la melancolía",
        chat_partner_placeholder: "Compañero de Chat",
        practicing_label: "Practicando:"
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
        back_to_dashboard: "Voltar para Seleção de Idioma",
        back_to_exercises: "Voltar para Exercícios",
        
        // Selection Display
        learning_display: "Aprendendo {target} de {input} no nível {level}",
        
        // Error Messages
        same_language_error: "You cannot select the same language for both input and target!",
        
        // Exercises Page
        learning_hub: "Centro de Aprendizagem",
        learning_journey: "Sua jornada personalizada de aprendizado de idiomas",
        practice_modules: "Módulos de Prática",
        conversation_practice: "Prática de Conversação",
        writing_practice: "Prática de Escrita",
        casual_chat: "Bate-papo Casual",
        everyday_conversations: "Conversas do dia a dia",
        email_writing: "Escrever E-mails",
        professional_emails: "E-mails profissionais",
        fill_blanks: "Preencher as Lacunas",
        grammar_practice: "Prática de gramática",
        ready_practice: "Pronto para praticar",
        
        // Casual Chat Page
        casual_conversation_practice: "Prática de Conversação Casual",
        practice_everyday: "Pratique conversas do dia a dia em um ambiente descontraído. Vamos conversar sobre a vida diária, hobbies e interesses!",
        start_chatting: "Começar a Conversar",
        choose_partner: "Escolha seu Parceiro de Conversa",
        select_practice_today: "Selecione com quem você gostaria de praticar hoje:",
        chat_with_harry: "Conversar com Harry",
        chat_with_sally: "Conversar com Sally",
        surprise_me: "Me Surpreenda!",
        ai_chat_partner: "Parceiro de Chat IA",
        messages_sent: "mensagens enviadas",
        harry_description: "Alegre instrutor de snowboard que adora festas e esportes",
        sally_description: "Bibliotecária reflexiva que encontra beleza na melancolia",
        chat_partner_placeholder: "Parceiro de Chat",
        practicing_label: "Praticando:"
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