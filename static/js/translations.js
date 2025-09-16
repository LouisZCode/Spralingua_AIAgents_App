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
        messages_in_language: "{count}/{total} messages in {language} sent",
        conversation_complete_language: "Conversation in {language} complete! Great job!",
        harry_description: "Cheerful snowboard instructor who loves parties and sports",
        sally_description: "Thoughtful librarian who finds beauty in melancholy",
        chat_partner_placeholder: "Chat Partner",
        practicing_label: "Practicing:",
        
        // Microphone UI
        done_speaking: "I'm Done Speaking",
        recording_status: "Recording...",
        
        // Listening mode
        read: "Read",

        // Feedback UI Labels
        feedback_phrase: "Phrase",
        feedback_hint: "Hint",
        feedback_error: "Error",
        feedback_correction: "Correction",
        feedback_explanation: "Explanation",
        feedback_strengths: "Strengths",
        feedback_focus_areas: "Areas to Focus",
        feedback_overall: "Overall Feedback",
        feedback_score: "Score",
        feedback_top_mistakes: "Top Mistakes",
        feedback_well_done: "Well Done",

        // Hint Display Labels
        hint_well_done: "Well Done!",
        hint_warning: "Suggestion",
        hint_error: "Correction",
        hint_phrase_label: "Phrase:",
        hint_praise_label: "Praise:",
        hint_tip_label: "Tip:",
        hint_correction_label: "Correction:",

        // Feedback Categories
        feedback_cat_grammar: "Grammar",
        feedback_cat_vocabulary: "Vocabulary",
        feedback_cat_tense: "Tense",
        feedback_cat_structure: "Structure",
        feedback_cat_gender: "Gender",
        feedback_cat_speaking: "Speaking",
        feedback_cat_ser_estar: "Ser vs Estar",
        feedback_cat_contractions: "Contractions",
        feedback_cat_articles: "Articles",
        feedback_cat_prepositions: "Prepositions",

        // Comprehensive feedback section headings
        feedback_common_mistakes: "Common Mistakes:",
        feedback_error_label: "Error:",
        feedback_correction_label: "Correction:",
        feedback_your_strengths: "Your Strengths:",
        feedback_areas_focus: "Areas to Focus On:",
        feedback_overall: "Overall:"
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
        messages_in_language: "{count}/{total} Nachrichten auf {language} gesendet",
        conversation_complete_language: "Gespräch auf {language} abgeschlossen! Gut gemacht!",
        harry_description: "Fröhlicher Snowboardlehrer, der Partys und Sport liebt",
        sally_description: "Nachdenkliche Bibliothekarin, die Schönheit in der Melancholie findet",
        chat_partner_placeholder: "Chatpartner",
        practicing_label: "Übe:",
        
        // Microphone UI
        done_speaking: "Fertig mit Sprechen",
        recording_status: "Aufnahme läuft...",
        
        // Listening mode
        read: "Lesen",

        // Feedback UI Labels
        feedback_phrase: "Phrase",
        feedback_hint: "Hinweis",
        feedback_error: "Fehler",
        feedback_correction: "Korrektur",
        feedback_explanation: "Erklärung",
        feedback_strengths: "Stärken",
        feedback_focus_areas: "Übungsbereiche",
        feedback_overall: "Gesamtfeedback",
        feedback_score: "Punktzahl",
        feedback_top_mistakes: "Hauptfehler",
        feedback_well_done: "Gut gemacht",

        // Hint Display Labels
        hint_well_done: "Gut gemacht!",
        hint_warning: "Hinweis",
        hint_error: "Korrektur",
        hint_phrase_label: "Phrase:",
        hint_praise_label: "Lob:",
        hint_tip_label: "Tipp:",
        hint_correction_label: "Korrektur:",

        // Feedback Categories
        feedback_cat_grammar: "Grammatik",
        feedback_cat_vocabulary: "Wortschatz",
        feedback_cat_tense: "Zeitform",
        feedback_cat_structure: "Satzbau",
        feedback_cat_gender: "Geschlecht",
        feedback_cat_speaking: "Sprechen",
        feedback_cat_ser_estar: "Ser vs Estar",
        feedback_cat_contractions: "Kontraktionen",
        feedback_cat_articles: "Artikel",
        feedback_cat_prepositions: "Präpositionen",

        // Comprehensive feedback section headings
        feedback_common_mistakes: "Häufige Fehler:",
        feedback_error_label: "Fehler:",
        feedback_correction_label: "Korrektur:",
        feedback_your_strengths: "Deine Stärken:",
        feedback_areas_focus: "Übungsbereiche:",
        feedback_overall: "Gesamt:"
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
        messages_in_language: "{count}/{total} mensajes en {language} enviados",
        conversation_complete_language: "¡Conversación en {language} completada! ¡Buen trabajo!",
        harry_description: "Alegre instructor de snowboard que ama las fiestas y los deportes",
        sally_description: "Bibliotecaria reflexiva que encuentra belleza en la melancolía",
        chat_partner_placeholder: "Compañero de Chat",
        practicing_label: "Practicando:",
        
        // Microphone UI
        done_speaking: "Terminé de Hablar",
        recording_status: "Grabando...",
        
        // Listening mode
        read: "Leer",

        // Feedback UI Labels
        feedback_phrase: "Frase",
        feedback_hint: "Consejo",
        feedback_error: "Error",
        feedback_correction: "Corrección",
        feedback_explanation: "Explicación",
        feedback_strengths: "Fortalezas",
        feedback_focus_areas: "Áreas de Enfoque",
        feedback_overall: "Comentario General",
        feedback_score: "Puntuación",
        feedback_top_mistakes: "Errores Principales",
        feedback_well_done: "Bien Hecho",

        // Hint Display Labels
        hint_well_done: "¡Bien Hecho!",
        hint_warning: "Sugerencia",
        hint_error: "Corrección",
        hint_phrase_label: "Frase:",
        hint_praise_label: "Elogio:",
        hint_tip_label: "Consejo:",
        hint_correction_label: "Corrección:",

        // Feedback Categories
        feedback_cat_grammar: "Gramática",
        feedback_cat_vocabulary: "Vocabulario",
        feedback_cat_tense: "Tiempo verbal",
        feedback_cat_structure: "Estructura",
        feedback_cat_gender: "Género",
        feedback_cat_speaking: "Conversación",
        feedback_cat_ser_estar: "Ser vs Estar",
        feedback_cat_contractions: "Contracciones",
        feedback_cat_articles: "Artículos",
        feedback_cat_prepositions: "Preposiciones",

        // Comprehensive feedback section headings
        feedback_common_mistakes: "Errores Comunes:",
        feedback_error_label: "Error:",
        feedback_correction_label: "Corrección:",
        feedback_your_strengths: "Tus Fortalezas:",
        feedback_areas_focus: "Áreas de Enfoque:",
        feedback_overall: "General:"
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
        messages_in_language: "{count}/{total} mensagens em {language} enviadas",
        conversation_complete_language: "Conversa em {language} concluída! Bom trabalho!",
        harry_description: "Alegre instrutor de snowboard que adora festas e esportes",
        sally_description: "Bibliotecária reflexiva que encontra beleza na melancolia",
        chat_partner_placeholder: "Parceiro de Chat",
        practicing_label: "Praticando:",
        
        // Microphone UI
        done_speaking: "Terminei de Falar",
        recording_status: "Gravando...",
        
        // Listening mode
        read: "Ler",

        // Feedback UI Labels
        feedback_phrase: "Frase",
        feedback_hint: "Dica",
        feedback_error: "Erro",
        feedback_correction: "Correção",
        feedback_explanation: "Explicação",
        feedback_strengths: "Pontos Fortes",
        feedback_focus_areas: "Áreas de Foco",
        feedback_overall: "Feedback Geral",
        feedback_score: "Pontuação",
        feedback_top_mistakes: "Principais Erros",
        feedback_well_done: "Muito Bem",

        // Hint Display Labels
        hint_well_done: "Muito Bem!",
        hint_warning: "Sugestão",
        hint_error: "Correção",
        hint_phrase_label: "Frase:",
        hint_praise_label: "Elogio:",
        hint_tip_label: "Dica:",
        hint_correction_label: "Correção:",

        // Feedback Categories
        feedback_cat_grammar: "Gramática",
        feedback_cat_vocabulary: "Vocabulário",
        feedback_cat_tense: "Tempo verbal",
        feedback_cat_structure: "Estrutura",
        feedback_cat_gender: "Gênero",
        feedback_cat_speaking: "Conversação",
        feedback_cat_ser_estar: "Ser vs Estar",
        feedback_cat_contractions: "Contrações",
        feedback_cat_articles: "Artigos",
        feedback_cat_prepositions: "Preposições",

        // Comprehensive feedback section headings
        feedback_common_mistakes: "Erros Comuns:",
        feedback_error_label: "Erro:",
        feedback_correction_label: "Correção:",
        feedback_your_strengths: "Seus Pontos Fortes:",
        feedback_areas_focus: "Áreas de Foco:",
        feedback_overall: "Geral:"
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

// Make it accessible globally via window object
window.translationManager = translationManager;

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        translationManager.init();
    });
} else {
    translationManager.init();
}