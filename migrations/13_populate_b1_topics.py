# Migration to populate B1 level topics (16 total including 4 tests)
# Based on Linguatec B1 curriculum guide

import sys
import os
import json

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from models.topic_definition import TopicDefinition
from app import app

def create_b1_topics():
    """Create all 16 B1 topics including 4 integrated tests."""

    topics = [
        # Topic 1: Making Small Talk
        {
            'level': 'B1',
            'topic_number': 1,
            'title_key': 'making_small_talk',
            'subtopics': json.dumps(['catching_up', 'weekend_discussions', 'fashion_trends', 'current_events']),
            'conversation_contexts': json.dumps(['Meeting old friend', 'Office water cooler', 'Social gathering']),
            'llm_prompt_template': """You are having a small talk conversation at B1 level.
Engage in natural small talk about various topics - weekend activities, current trends, recent experiences.
Use present perfect: 'Have you seen the new...?', 'I've been meaning to tell you...'.
Include idiomatic expressions: 'Long time no see', 'How have you been keeping?', 'What have you been up to?'.
Discuss fashion, trends, recent events naturally: 'Did you hear about...?', 'I love your dress! Where did you get it?'.
Show interest and keep conversation flowing with follow-up questions and comments.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["Hey! Haven't seen you in ages! How have you been?", "Fancy meeting you here! What have you been up to lately?"],
                'german': ['Hey! Lange nicht gesehen! Wie ist es dir ergangen?', 'Schön, dich hier zu treffen! Was hast du in letzter Zeit so gemacht?'],
                'spanish': ['¡Hey! ¡Hace siglos que no te veo! ¿Cómo has estado?', '¡Qué casualidad encontrarte aquí! ¿Qué has estado haciendo últimamente?'],
                'portuguese': ['Olá! Há quanto tempo! Como tens estado?', 'Que coincidência encontrar-te aqui! O que tens andado a fazer?']
            }),
            'required_vocabulary': json.dumps(['catch up', 'lately', 'been up to', 'ages', 'fashion', 'trend', 'nowadays', 'recently']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Greeting with surprise → Catch up on recent events → Discuss current trends → Share experiences → Make future plans'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use present perfect for recent experiences. Include idiomatic expressions and phrasal verbs naturally.',
            'scenario_template': 'You bump into an old colleague at a coffee shop and catch up on recent events and trends.'
        },

        # Topic 2: At the Store
        {
            'level': 'B1',
            'topic_number': 2,
            'title_key': 'at_the_store',
            'subtopics': json.dumps(['shopping_stories', 'customer_service', 'returning_products', 'buying_souvenirs']),
            'conversation_contexts': json.dumps(['Department store', 'Customer service desk', 'Shopping mall']),
            'llm_prompt_template': """You are discussing shopping experiences and customer service at B1 level.
Share shopping stories and deal with customer service situations.
Use past continuous: 'I was shopping when...', 'While I was looking for...'.
Handle complaints politely: 'I'm afraid this is damaged', 'Could you possibly exchange this?'.
Express dissatisfaction: 'I'm not happy with...', 'This isn't what I ordered'.
Describe products in detail: materials, features, quality issues.
Use conditional: 'If you had a receipt, we could...', 'I would appreciate if...'.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["I'd like to return this item, please.", "Can you help me? I bought this yesterday but..."],
                'german': ['Ich möchte diesen Artikel zurückgeben, bitte.', 'Können Sie mir helfen? Ich habe das gestern gekauft, aber...'],
                'spanish': ['Me gustaría devolver este artículo, por favor.', '¿Puede ayudarme? Compré esto ayer pero...'],
                'portuguese': ['Gostaria de devolver este artigo, por favor.', 'Pode ajudar-me? Comprei isto ontem mas...']
            }),
            'required_vocabulary': json.dumps(['refund', 'exchange', 'receipt', 'faulty', 'customer service', 'complaint', 'warranty', 'quality']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'State problem → Explain situation → Negotiate solution → Reach agreement → Thank or express satisfaction'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Practice polite complaints and conditional sentences. Use past continuous for shopping stories.',
            'scenario_template': "You're at customer service returning a faulty product and explaining what happened."
        },

        # Topic 3: Giving Instructions
        {
            'level': 'B1',
            'topic_number': 3,
            'title_key': 'giving_instructions',
            'subtopics': json.dumps(['using_appliances', 'tech_gadgets', 'life_hacks', 'how_things_work']),
            'conversation_contexts': json.dumps(['Teaching someone', 'Tech support', 'Explaining procedures']),
            'llm_prompt_template': """You are explaining how to use things and giving instructions at B1 level.
Give clear step-by-step instructions for using appliances, gadgets, or explaining life hacks.
Use sequencing: 'First', 'Then', 'After that', 'Finally', 'Make sure to...'.
Include warnings: 'Be careful not to...', 'Never...', 'Always remember to...'.
Explain purpose: 'This is for...', 'You use this when...', 'The point is to...'.
Check understanding: 'Is that clear?', 'Do you follow?', 'Any questions so far?'.
Use imperatives and modal verbs for advice.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["Let me show you how this works. It's actually quite simple.", "I'll explain how to use this. Pay attention to..."],
                'german': ['Ich zeige dir, wie das funktioniert. Es ist eigentlich ganz einfach.', 'Ich erkläre dir, wie man das benutzt. Achte auf...'],
                'spanish': ['Te muestro cómo funciona esto. En realidad es bastante simple.', 'Te explico cómo usar esto. Presta atención a...'],
                'portuguese': ['Deixa-me mostrar-te como isto funciona. É bastante simples.', 'Vou explicar-te como usar isto. Presta atenção a...']
            }),
            'required_vocabulary': json.dumps(['press', 'turn on/off', 'connect', 'plug in', 'settings', 'button', 'screen', 'device']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Introduce device/task → Give step-by-step instructions → Warn about mistakes → Check understanding → Offer tips'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use clear sequencing words and imperatives. Include purpose explanations and safety warnings.',
            'scenario_template': "You're teaching a friend how to use a new smartphone app or kitchen appliance."
        },

        # Topic 4: TEST CHECKPOINT 1
        {
            'level': 'B1',
            'topic_number': 4,
            'title_key': 'test_checkpoint_1',
            'subtopics': json.dumps(['small_talk', 'shopping', 'instructions']),
            'conversation_contexts': json.dumps(['Electronics Store Encounter']),
            'llm_prompt_template': """You are at an electronics store at B1 level.
You will meet an old friend, discuss a recent purchase problem, and explain how to use a gadget.
Start with small talk about what you've both been doing. Then mention a problem with something you bought. Finally, help them understand how to use a new device.
Use present perfect for catching up, past continuous for stories, and clear sequencing for instructions.
Include idiomatic expressions, polite complaints, and technical vocabulary.
Keep the conversation flowing naturally between all topics.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["Oh wow, is that you? I can't believe we're both here looking at electronics!"],
                'german': ['Oh wow, bist du das? Ich kann nicht glauben, dass wir beide hier Elektronik anschauen!'],
                'spanish': ['¡Oh, vaya! ¿Eres tú? ¡No puedo creer que ambos estemos aquí mirando electrónica!'],
                'portuguese': ['Oh, és tu? Não acredito que estamos ambos aqui a ver eletrónica!']
            }),
            'required_vocabulary': json.dumps([]),
            'conversation_flow': json.dumps({
                'exchanges': 10,
                'structure': 'Integrated test covering small talk, shopping experiences, and giving instructions'
            }),
            'number_of_exchanges': 10,
            'topic_specific_rules': 'TEST: Assess small talk, customer service language, and instruction-giving abilities.',
            'scenario_template': 'Electronics Store Encounter - Testing topics 1-3'
        },

        # Topic 5: Talking About Hobbies
        {
            'level': 'B1',
            'topic_number': 5,
            'title_key': 'talking_about_hobbies',
            'subtopics': json.dumps(['hobbies_and_skills', 'free_time_activities', 'unusual_pastimes', 'learning_new_things']),
            'conversation_contexts': json.dumps(['Hobby club', 'Weekend activities', 'New interests']),
            'llm_prompt_template': """You are discussing hobbies and interests at B1 level.
Talk about hobbies you're passionate about and unusual activities you've tried.
Use present perfect continuous: 'I've been learning...', 'How long have you been doing...?'.
Express enthusiasm: 'I'm really into...', 'I'm passionate about...', 'I've gotten hooked on...'.
Describe skill progression: 'I started as a beginner but now...', 'It took me ages to...'.
Discuss unusual hobbies: 'You might find it weird, but...', 'Not many people know about...'.
Use phrasal verbs: take up, give up, get into, carry on.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["I've recently taken up a new hobby that I'm really excited about!", "Have you ever tried anything really unusual in your free time?"],
                'german': ['Ich habe kürzlich ein neues Hobby angefangen, das mich wirklich begeistert!', 'Hast du schon mal etwas wirklich Ungewöhnliches in deiner Freizeit ausprobiert?'],
                'spanish': ['¡Recientemente he empezado un nuevo hobby que me emociona mucho!', '¿Has probado algo realmente inusual en tu tiempo libre?'],
                'portuguese': ['Recentemente comecei um novo hobby que me entusiasma muito!', 'Já experimentaste algo realmente invulgar no teu tempo livre?']
            }),
            'required_vocabulary': json.dumps(['passionate', 'hobby', 'skill', 'practice', 'improve', 'challenge', 'rewarding', 'achievement']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Share current hobby → Discuss how you started → Describe progress → Ask about theirs → Compare experiences'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use present perfect continuous for duration. Express enthusiasm and use hobby-related phrasal verbs.',
            'scenario_template': "You're at a community center talking about the unusual hobby you've recently taken up."
        },

        # Topic 6: Talking About Work
        {
            'level': 'B1',
            'topic_number': 6,
            'title_key': 'talking_about_work',
            'subtopics': json.dumps(['job_responsibilities', 'work_environment', 'career_aspirations', 'ideal_jobs']),
            'conversation_contexts': json.dumps(['Job interview', 'Networking event', 'Career discussion']),
            'llm_prompt_template': """You are discussing work and career at B1 level.
Talk about your job, responsibilities, work environment, and career goals.
Describe responsibilities: 'I'm in charge of...', 'I'm responsible for...', 'My role involves...'.
Discuss work conditions: 'The atmosphere is...', 'My colleagues are...', 'The workload can be...'.
Express aspirations: 'I'm hoping to...', 'My goal is to...', 'I'd like to move into...'.
Use conditional for ideal job: 'My dream job would be...', 'If I could choose...'.
Include work idioms: 'work around the clock', 'think outside the box', 'climb the career ladder'.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["So what exactly do you do in your current role?", "I'm thinking about making a career change. What's your job like?"],
                'german': ['Was genau machst du in deiner aktuellen Position?', 'Ich denke über einen Berufswechsel nach. Wie ist dein Job so?'],
                'spanish': ['¿Qué haces exactamente en tu puesto actual?', 'Estoy pensando en cambiar de carrera. ¿Cómo es tu trabajo?'],
                'portuguese': ['O que fazes exatamente no teu cargo atual?', 'Estou a pensar em mudar de carreira. Como é o teu trabalho?']
            }),
            'required_vocabulary': json.dumps(['responsibilities', 'colleague', 'deadline', 'promotion', 'career', 'manage', 'achieve', 'professional']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Current job description → Daily responsibilities → Work environment → Career goals → Ideal job discussion'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use work-related vocabulary and idioms. Practice conditionals for hypothetical situations.',
            'scenario_template': "You're at a networking event discussing your career path and future aspirations."
        },

        # Topic 7: Going Out
        {
            'level': 'B1',
            'topic_number': 7,
            'title_key': 'going_out',
            'subtopics': json.dumps(['inviting_people', 'making_dinner_plans', 'restaurant_recommendations', 'ordering_food']),
            'conversation_contexts': json.dumps(['Planning evening out', 'Restaurant booking', 'Group dinner']),
            'llm_prompt_template': """You are making plans to go out and discussing restaurants at B1 level.
Invite people and make dinner arrangements with enthusiasm and detail.
Make invitations: 'How about we...?', 'Would you be up for...?', 'I was wondering if you'd like to...'.
Suggest places: 'I've heard great things about...', 'There's this amazing place that...'.
Express preferences: 'I'm in the mood for...', 'I'd rather go somewhere...'.
Make arrangements: 'Shall we book for...?', 'Let's meet at...', 'I'll make a reservation'.
Discuss dietary needs: 'Are you okay with...?', 'Do they cater for vegetarians?'.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["We should definitely go out this weekend! I know a great place.", "Are you free for dinner on Friday? I've been dying to try this new restaurant."],
                'german': ['Wir sollten dieses Wochenende definitiv ausgehen! Ich kenne einen tollen Ort.', 'Hast du am Freitag Zeit zum Abendessen? Ich möchte unbedingt dieses neue Restaurant ausprobieren.'],
                'spanish': ['¡Definitivamente deberíamos salir este fin de semana! Conozco un lugar genial.', '¿Estás libre para cenar el viernes? Me muero por probar este nuevo restaurante.'],
                'portuguese': ['Devíamos definitivamente sair este fim de semana! Conheço um sítio ótimo.', 'Estás livre para jantar na sexta? Estou morto por experimentar este novo restaurante.']
            }),
            'required_vocabulary': json.dumps(['reservation', 'cuisine', 'atmosphere', 'recommend', 'specialty', 'book a table', 'dietary', 'venue']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Suggest going out → Discuss options → Express preferences → Make decision → Confirm arrangements'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use suggestion language and express preferences clearly. Include food and restaurant vocabulary.',
            'scenario_template': "You're organizing a group dinner and discussing where to go and what everyone likes."
        },

        # Topic 8: TEST CHECKPOINT 2
        {
            'level': 'B1',
            'topic_number': 8,
            'title_key': 'test_checkpoint_2',
            'subtopics': json.dumps(['hobbies', 'work_life', 'social_plans']),
            'conversation_contexts': json.dumps(['After-Work Meetup']),
            'llm_prompt_template': """You are at an after-work social event at B1 level.
You will discuss your hobbies, talk about work-life balance, and make plans for the weekend.
Start by talking about how you unwind after work with hobbies. Then discuss your job and work-life balance. Finally, make dinner plans for the weekend.
Use present perfect continuous for hobbies, work vocabulary for career discussion, and suggestion language for making plans.
Include enthusiasm, work idioms, and restaurant vocabulary.
Create natural transitions between all topics.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["Thank goodness it's Friday! I've been looking forward to unwinding all week."],
                'german': ['Gott sei Dank ist Freitag! Ich habe mich die ganze Woche darauf gefreut, zu entspannen.'],
                'spanish': ['¡Gracias a Dios es viernes! He estado esperando relajarme toda la semana.'],
                'portuguese': ['Graças a Deus é sexta! Estive à espera de relaxar a semana toda.']
            }),
            'required_vocabulary': json.dumps([]),
            'conversation_flow': json.dumps({
                'exchanges': 10,
                'structure': 'Integrated test covering hobbies, work discussion, and social planning'
            }),
            'number_of_exchanges': 10,
            'topic_specific_rules': 'TEST: Assess hobby discussion, work vocabulary, and social arrangement skills.',
            'scenario_template': 'After-Work Meetup - Testing topics 5-7'
        },

        # Topic 9: Travel Planning
        {
            'level': 'B1',
            'topic_number': 9,
            'title_key': 'travel_planning',
            'subtopics': json.dumps(['email_arrangements', 'hotel_reviews', 'vacation_planning', 'phone_bookings']),
            'conversation_contexts': json.dumps(['Travel agency', 'Online booking', 'Trip planning']),
            'llm_prompt_template': """You are planning a trip and making travel arrangements at B1 level.
Discuss travel plans in detail, read reviews, and make bookings.
Express preferences: 'I'd prefer to stay somewhere...', 'I'm looking for something...'.
Discuss reviews: 'According to the reviews...', 'People say that...', 'It's rated highly for...'.
Make comparisons: 'This one is better value than...', 'It's more convenient than...'.
Phone booking language: 'I'd like to inquire about...', 'What's included in...?', 'Is it possible to...?'.
Use future perfect: 'By the time we arrive, we'll have...'.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["I'm planning a trip for next month. Have you seen any good deals?", "I need help booking accommodation. The reviews are so mixed!"],
                'german': ['Ich plane eine Reise für nächsten Monat. Hast du gute Angebote gesehen?', 'Ich brauche Hilfe bei der Buchung einer Unterkunft. Die Bewertungen sind so gemischt!'],
                'spanish': ['Estoy planeando un viaje para el próximo mes. ¿Has visto buenas ofertas?', '¡Necesito ayuda para reservar alojamiento. Las reseñas son tan variadas!'],
                'portuguese': ['Estou a planear uma viagem para o próximo mês. Viste algumas boas ofertas?', 'Preciso de ajuda para reservar alojamento. As avaliações são tão mistas!']
            }),
            'required_vocabulary': json.dumps(['accommodation', 'itinerary', 'booking', 'cancellation', 'reviews', 'facilities', 'location', 'availability']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Discuss destination → Compare options → Read reviews → Make decision → Confirm booking'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Practice making comparisons and discussing reviews. Use formal booking language.',
            'scenario_template': "You're planning a vacation with a friend and comparing different hotels and travel options."
        },

        # Topic 10: Understanding Social Media
        {
            'level': 'B1',
            'topic_number': 10,
            'title_key': 'understanding_social_media',
            'subtopics': json.dumps(['types_of_social_media', 'celebrities_online', 'apps_and_features', 'social_media_usage']),
            'conversation_contexts': json.dumps(['Digital literacy discussion', 'App comparison', 'Online trends']),
            'llm_prompt_template': """You are discussing social media and digital platforms at B1 level.
Talk about different social media platforms, their features, and how people use them.
Compare platforms: 'Instagram is better for...while Twitter is...', 'Unlike Facebook,...'.
Discuss features: 'You can...', 'It allows you to...', 'The algorithm shows you...'.
Express opinions: 'I think social media is...', 'The problem with...is...', 'What bothers me is...'.
Talk about celebrities: 'Did you see what [celebrity] posted?', 'They have millions of followers'.
Use passive voice: 'Photos are shared...', 'Content is created by...'.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["Which social media platforms do you use? I'm trying to understand all these new apps.", "Have you seen the latest social media trend? It's everywhere!"],
                'german': ['Welche Social-Media-Plattformen nutzt du? Ich versuche, all diese neuen Apps zu verstehen.', 'Hast du den neuesten Social-Media-Trend gesehen? Er ist überall!'],
                'spanish': ['¿Qué redes sociales usas? Estoy tratando de entender todas estas nuevas aplicaciones.', '¿Has visto la última tendencia en redes sociales? ¡Está en todas partes!'],
                'portuguese': ['Que redes sociais usas? Estou a tentar perceber todas estas novas aplicações.', 'Viste a última tendência nas redes sociais? Está em todo o lado!']
            }),
            'required_vocabulary': json.dumps(['platform', 'followers', 'influencer', 'viral', 'post', 'share', 'algorithm', 'privacy']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Discuss platforms → Compare features → Share opinions → Talk about trends → Privacy concerns'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use comparison language and passive voice. Express opinions about social media impact.',
            'scenario_template': "You're discussing the pros and cons of different social media platforms with a friend."
        },

        # Topic 11: Asking for Clarification
        {
            'level': 'B1',
            'topic_number': 11,
            'title_key': 'asking_for_clarification',
            'subtopics': json.dumps(['phone_clarification', 'offering_help', 'explaining_meanings', 'clarifying_information']),
            'conversation_contexts': json.dumps(['Phone conversation', 'Helping someone', 'Clarifying instructions']),
            'llm_prompt_template': """You are practicing asking for and giving clarification at B1 level.
Master the art of clarifying information in various situations.
Ask for clarification: 'Sorry, could you repeat that?', 'What do you mean by...?', 'Just to clarify...'.
Confirm understanding: 'So what you're saying is...', 'If I understand correctly...', 'Let me get this straight...'.
Give clarification: 'What I meant was...', 'To put it another way...', 'In other words...'.
Phone language: 'The line is bad', 'I can't hear you clearly', 'Could you speak up?'.
Offer help: 'Would you like me to explain?', 'Can I help clarify something?'.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["Sorry, I didn't quite catch that. Could you explain what you mean?", "Let me make sure I understand this correctly..."],
                'german': ['Entschuldigung, das habe ich nicht ganz verstanden. Könntest du erklären, was du meinst?', 'Lass mich sicherstellen, dass ich das richtig verstehe...'],
                'spanish': ['Perdón, no entendí bien. ¿Podrías explicar qué quieres decir?', 'Déjame asegurarme de que entiendo esto correctamente...'],
                'portuguese': ['Desculpa, não percebi bem. Podes explicar o que queres dizer?', 'Deixa-me ter a certeza de que percebo isto corretamente...']
            }),
            'required_vocabulary': json.dumps(['clarify', 'explain', 'understand', 'repeat', 'mean', 'clear', 'confuse', 'specific']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Initial confusion → Ask for clarification → Receive explanation → Confirm understanding → Offer own clarification'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Practice clarification phrases and confirmation language. Use rephrasing techniques.',
            'scenario_template': "You're on a phone call with bad connection trying to understand important information."
        },

        # Topic 12: TEST CHECKPOINT 3
        {
            'level': 'B1',
            'topic_number': 12,
            'title_key': 'test_checkpoint_3',
            'subtopics': json.dumps(['travel', 'social_media', 'clarification']),
            'conversation_contexts': json.dumps(['Virtual Travel Planning Meeting']),
            'llm_prompt_template': """You are in a video call planning a group trip at B1 level.
You will discuss travel arrangements, share social media travel content, and clarify details with connection issues.
Start by discussing travel options you've researched. Then share what you've seen on social media about the destination. Finally, deal with connection problems while clarifying important details.
Use travel vocabulary, social media terms, and clarification language.
Include comparisons, opinions, and polite clarification requests.
Make the conversation flow naturally with realistic video call challenges.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["Can everyone see and hear me okay? Let's plan this amazing trip!"],
                'german': ['Könnt ihr mich alle sehen und hören? Lasst uns diese tolle Reise planen!'],
                'spanish': ['¿Todos pueden verme y oírme bien? ¡Planeemos este viaje increíble!'],
                'portuguese': ['Todos conseguem ver-me e ouvir-me bem? Vamos planear esta viagem incrível!']
            }),
            'required_vocabulary': json.dumps([]),
            'conversation_flow': json.dumps({
                'exchanges': 10,
                'structure': 'Integrated test covering travel planning, social media discussion, and clarification skills'
            }),
            'number_of_exchanges': 10,
            'topic_specific_rules': 'TEST: Assess travel planning, social media vocabulary, and clarification techniques.',
            'scenario_template': 'Virtual Travel Planning Meeting - Testing topics 9-11'
        },

        # Topic 13: Expressing Preferences
        {
            'level': 'B1',
            'topic_number': 13,
            'title_key': 'expressing_preferences',
            'subtopics': json.dumps(['accommodation_preferences', 'free_time_choices', 'technology_preferences', 'lifestyle_choices']),
            'conversation_contexts': json.dumps(['Preference discussion', 'Lifestyle choices', 'Decision making']),
            'llm_prompt_template': """You are discussing preferences and choices at B1 level.
Express and justify your preferences about various aspects of life.
Strong preferences: 'I much prefer...', 'I'd always choose...', 'Nothing beats...'.
Explain reasons: 'The thing is...', 'The reason I prefer...is...', 'What matters to me is...'.
Compare options: 'On the one hand...on the other hand...', 'While I appreciate..., I prefer...'.
Discuss lifestyle: 'I'm more of a...person', 'I tend to...', 'I'm not really into...'.
Use would rather/would prefer: 'I'd rather stay in a hotel than...', 'I'd prefer to...'.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["Are you more of a hotel or hostel person when traveling?", "I'm curious - what's your take on modern technology versus traditional ways?"],
                'german': ['Bist du eher ein Hotel- oder Hostel-Typ beim Reisen?', 'Ich bin neugierig - was hältst du von moderner Technologie versus traditionellen Wegen?'],
                'spanish': ['¿Eres más de hotel o de hostal cuando viajas?', 'Tengo curiosidad: ¿qué opinas sobre la tecnología moderna versus las formas tradicionales?'],
                'portuguese': ['És mais de hotel ou hostel quando viajas?', 'Tenho curiosidade - qual é a tua opinião sobre tecnologia moderna versus formas tradicionais?']
            }),
            'required_vocabulary': json.dumps(['prefer', 'rather', 'choice', 'option', 'lifestyle', 'tendency', 'favor', 'priority']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'State preference → Explain reasoning → Compare alternatives → Ask their view → Find common ground'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': "Practice 'would rather' and 'would prefer'. Justify preferences with clear reasoning.",
            'scenario_template': "You're discussing lifestyle preferences and choices with someone who has very different tastes."
        },

        # Topic 14: Discussing Pop Culture
        {
            'level': 'B1',
            'topic_number': 14,
            'title_key': 'discussing_pop_culture',
            'subtopics': json.dumps(['celebrity_life', 'famous_marriages', 'movies_and_series', 'entertainment_news']),
            'conversation_contexts': json.dumps(['Entertainment discussion', 'Celebrity gossip', 'Movie reviews']),
            'llm_prompt_template': """You are discussing pop culture and entertainment at B1 level.
Talk about celebrities, movies, TV series, and entertainment news.
Discuss celebrities: 'Have you heard about...?', 'Apparently they're...', 'The tabloids say...'.
Express opinions on shows: 'The plot was...', 'The acting was...', 'It's worth watching because...'.
Use reported speech: 'They said that...', 'According to...', 'It's been reported that...'.
Make recommendations: 'You have to see...', 'Don't bother with...', 'If you liked X, you'll love Y'.
Discuss performances: 'She was brilliant in...', 'He totally nailed the role'.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["Did you hear about that celebrity scandal? It's all over the news!", "Have you been watching any good series lately? I need recommendations."],
                'german': ['Hast du von diesem Promi-Skandal gehört? Es ist überall in den Nachrichten!', 'Schaust du in letzter Zeit gute Serien? Ich brauche Empfehlungen.'],
                'spanish': ['¿Escuchaste sobre ese escándalo de celebridades? ¡Está en todas las noticias!', '¿Has estado viendo alguna buena serie últimamente? Necesito recomendaciones.'],
                'portuguese': ['Ouviste falar daquele escândalo de celebridades? Está em todas as notícias!', 'Tens visto alguma boa série ultimamente? Preciso de recomendações.']
            }),
            'required_vocabulary': json.dumps(['celebrity', 'scandal', 'performance', 'series', 'season', 'episode', 'reviews', 'ratings']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Share entertainment news → Discuss celebrities → Review shows/movies → Make recommendations → Debate opinions'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use reported speech for gossip. Express strong opinions about entertainment.',
            'scenario_template': "You're catching up on the latest entertainment news and discussing your favorite shows."
        },

        # Topic 15: Expressing Opinions
        {
            'level': 'B1',
            'topic_number': 15,
            'title_key': 'expressing_opinions',
            'subtopics': json.dumps(['political_issues', 'social_problems', 'controversial_themes', 'personal_beliefs']),
            'conversation_contexts': json.dumps(['Debate', 'Opinion sharing', 'Discussion group']),
            'llm_prompt_template': """You are expressing opinions on various topics at B1 level.
Share and defend your opinions on social issues while respecting different views.
Express opinions: 'In my opinion...', 'I strongly believe that...', 'From my perspective...'.
Agree/Disagree politely: 'I see your point, but...', 'I partly agree, however...', 'That's true to some extent...'.
Support arguments: 'The fact is...', 'Studies show that...', 'It's been proven that...'.
Express uncertainty: 'I'm not entirely sure, but...', 'I could be wrong, but...'.
Conclude: 'All things considered...', 'Taking everything into account...'.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["What's your take on social media's impact on society?", "I've been thinking about environmental issues lately. What's your opinion?"],
                'german': ['Was hältst du vom Einfluss sozialer Medien auf die Gesellschaft?', 'Ich habe in letzter Zeit über Umweltprobleme nachgedacht. Was ist deine Meinung?'],
                'spanish': ['¿Cuál es tu opinión sobre el impacto de las redes sociales en la sociedad?', 'He estado pensando en temas ambientales últimamente. ¿Cuál es tu opinión?'],
                'portuguese': ['Qual é a tua opinião sobre o impacto das redes sociais na sociedade?', 'Tenho pensado em questões ambientais ultimamente. Qual é a tua opinião?']
            }),
            'required_vocabulary': json.dumps(['opinion', 'believe', 'argue', 'perspective', 'controversial', 'debate', 'viewpoint', 'stance']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Present topic → State opinion → Support with reasons → Consider counter-arguments → Reach conclusion'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Practice opinion language and supporting arguments. Show respect for different viewpoints.',
            'scenario_template': "You're in a discussion group talking about current social and environmental issues."
        },

        # Topic 16: FINAL TEST
        {
            'level': 'B1',
            'topic_number': 16,
            'title_key': 'test_final',
            'subtopics': json.dumps(['preferences', 'culture', 'opinions']),
            'conversation_contexts': json.dumps(['International Culture Exchange']),
            'llm_prompt_template': """You are at an international culture exchange event at B1 level.
You will express preferences about lifestyle, discuss pop culture from different countries, and share opinions on global issues.
Start by discussing your lifestyle preferences and cultural differences. Then talk about entertainment from various countries. Finally, share opinions on how culture affects society.
Use preference language, reported speech for cultural news, and opinion expressions.
Include comparisons between cultures, entertainment recommendations, and respectful debate.
Create a sophisticated conversation befitting B1 level.""",
            'word_limit': 60,
            'opening_phrases': json.dumps({
                'english': ["It's fascinating how different cultures approach daily life. What's it like where you're from?"],
                'german': ['Es ist faszinierend, wie verschiedene Kulturen das tägliche Leben angehen. Wie ist es, wo du herkommst?'],
                'spanish': ['Es fascinante cómo las diferentes culturas abordan la vida diaria. ¿Cómo es donde vienes?'],
                'portuguese': ['É fascinante como diferentes culturas abordam a vida quotidiana. Como é de onde vens?']
            }),
            'required_vocabulary': json.dumps([]),
            'conversation_flow': json.dumps({
                'exchanges': 10,
                'structure': 'Integrated test covering preferences, pop culture, and opinion expression'
            }),
            'number_of_exchanges': 10,
            'topic_specific_rules': 'FINAL TEST: Comprehensively assess B1 skills including preferences, cultural discussion, and opinion expression.',
            'scenario_template': 'International Culture Exchange - Testing topics 13-15'
        }
    ]

    with app.app_context():
        print("Creating B1 topics...")
        topics_created = 0

        for topic_data in topics:
            # Check if topic already exists
            existing = TopicDefinition.query.filter_by(
                level=topic_data['level'],
                topic_number=topic_data['topic_number']
            ).first()

            if existing:
                print(f"Topic {topic_data['topic_number']} ({topic_data['title_key']}) already exists, skipping...")
                continue

            # Create new topic
            topic = TopicDefinition(**topic_data)
            db.session.add(topic)
            topics_created += 1

            # Show what we're creating
            if topic_data['topic_number'] in [4, 8, 12, 16]:
                print(f"Created TEST {topic_data['topic_number']}: {topic_data['title_key']}")
            else:
                print(f"Created Topic {topic_data['topic_number']}: {topic_data['title_key']}")

        # Commit all changes
        db.session.commit()
        print(f"\nSuccessfully created {topics_created} B1 topics!")

        # Verify the count
        b1_count = TopicDefinition.query.filter_by(level='B1').count()
        print(f"Total B1 topics in database: {b1_count}")

if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION: Populate B1 Topics (16 total)")
    print("=" * 60)
    create_b1_topics()
    print("\nB1 level is now ready with all 16 topics!")