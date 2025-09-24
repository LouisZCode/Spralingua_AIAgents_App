# Migration to populate A2 level topics (16 total including 4 tests)
# Based on Linguatec A2 curriculum guide

import sys
import os
import json

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from models.topic_definition import TopicDefinition
from app import app

def create_a2_topics():
    """Create all 16 A2 topics including 4 integrated tests."""

    topics = [
        # Topic 1: Morning Routine
        {
            'level': 'A2',
            'topic_number': 1,
            'title_key': 'morning_routine',
            'subtopics': json.dumps(['daily_routine', 'everyday_activities', 'activities_with_friends']),
            'conversation_contexts': json.dumps(['Describing your morning', 'Weekend routines', 'Activities with friends']),
            'llm_prompt_template': """You are having a conversation about daily routines at A2 level.
Discuss morning activities, what you do every day, and weekend activities with friends.
Use past simple and present simple naturally. Include time expressions like 'usually', 'sometimes', 'every day'.
Ask about the user's routine: 'What do you usually do in the morning?', 'What time do you wake up?'
Include vocabulary: get up, have breakfast, brush teeth, take a shower, go to work/school.
Can use past tense: 'Yesterday I woke up late', 'Last weekend I went out with friends'.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ['Good morning! Tell me about your typical day.', 'Hey! What does your morning routine look like?'],
                'german': ['Guten Morgen! Erzähl mir von deinem typischen Tag.', 'Hey! Wie sieht deine Morgenroutine aus?'],
                'spanish': ['¡Buenos días! Cuéntame sobre tu día típico.', '¡Hola! ¿Cómo es tu rutina matutina?'],
                'portuguese': ['Bom dia! Conta-me sobre o teu dia típico.', 'Olá! Como é a tua rotina matinal?']
            }),
            'required_vocabulary': json.dumps(['wake up', 'breakfast', 'usually', 'sometimes', 'every day', 'morning', 'afternoon', 'evening']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Greeting → Ask about routine → Share your routine → Compare weekday vs weekend → Plans for tomorrow'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Practice present simple for routines and past simple for yesterday. Use time expressions naturally.',
            'scenario_template': 'You meet a new colleague at work who asks about your daily routine and how you spend your mornings.'
        },

        # Topic 2: Making Plans
        {
            'level': 'A2',
            'topic_number': 2,
            'title_key': 'making_plans',
            'subtopics': json.dumps(['free_time_activities', 'plans_with_friends', 'going_out']),
            'conversation_contexts': json.dumps(['Weekend plans', 'Meeting friends', 'Leisure activities']),
            'llm_prompt_template': """You are discussing plans and free-time activities at A2 level.
Talk about what you're doing this weekend, making plans with friends, and leisure activities.
Use future with 'going to' and present continuous for plans: 'I'm meeting friends tomorrow', 'We're going to watch a movie'.
Ask: 'What are you doing this weekend?', 'Do you want to come?', 'How about Saturday?'
Include activities: go to the cinema, meet friends, play sports, visit museums, go shopping.
Express opinions: 'That sounds fun!', 'I don't really like...', 'How about we...'""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ['So, any plans for the weekend?', "Let's do something fun this Saturday!"],
                'german': ['Also, hast du Pläne fürs Wochenende?', 'Lass uns am Samstag etwas Lustiges machen!'],
                'spanish': ['¿Tienes planes para el fin de semana?', '¡Hagamos algo divertido este sábado!'],
                'portuguese': ['Tens planos para o fim de semana?', 'Vamos fazer algo divertido este sábado!']
            }),
            'required_vocabulary': json.dumps(['weekend', 'tomorrow', 'next week', 'free time', 'cinema', 'restaurant', 'party', 'sports']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Ask about plans → Suggest activity → Negotiate time/place → Confirm details → Express enthusiasm'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use future forms for plans. Practice making suggestions and responding to invitations.',
            'scenario_template': "It's Friday afternoon and you're making weekend plans with a friend."
        },

        # Topic 3: Where is the Subway?
        {
            'level': 'A2',
            'topic_number': 3,
            'title_key': 'where_is_subway',
            'subtopics': json.dumps(['neighborhood_description', 'giving_directions', 'street_navigation']),
            'conversation_contexts': json.dumps(['Asking for directions', 'Describing locations', 'Finding places']),
            'llm_prompt_template': """You are helping someone with directions and describing the neighborhood at A2 level.
Give and ask for directions using prepositions of place and movement.
Use imperatives for directions: 'Turn left', 'Go straight', 'Take the second right'.
Describe locations: 'It's opposite the bank', 'next to the pharmacy', 'between the café and the bookstore'.
Ask: 'Excuse me, where is...?', 'How do I get to...?', 'Is it far from here?'
Include landmarks: subway station, bus stop, traffic lights, corner, main street.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ['Excuse me, can you help me find the subway?', "I'm looking for the nearest metro station."],
                'german': ['Entschuldigung, können Sie mir helfen, die U-Bahn zu finden?', 'Ich suche die nächste U-Bahn-Station.'],
                'spanish': ['Disculpe, ¿puede ayudarme a encontrar el metro?', 'Busco la estación de metro más cercana.'],
                'portuguese': ['Desculpe, pode ajudar-me a encontrar o metro?', 'Procuro a estação de metro mais próxima.']
            }),
            'required_vocabulary': json.dumps(['turn left/right', 'straight', 'corner', 'traffic lights', 'opposite', 'next to', 'near', 'far']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Ask for help → Give directions → Clarify details → Confirm understanding → Thank'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use imperatives and prepositions of place. Practice giving clear, step-by-step directions.',
            'scenario_template': "You're lost in a new neighborhood and need to find the subway station to get home."
        },

        # Topic 4: TEST CHECKPOINT 1
        {
            'level': 'A2',
            'topic_number': 4,
            'title_key': 'test_checkpoint_1',
            'subtopics': json.dumps(['routines', 'plans', 'directions']),
            'conversation_contexts': json.dumps(['Coffee Shop Meetup']),
            'llm_prompt_template': """You are at a coffee shop meeting a friend at A2 level.
You will discuss your morning routine, make plans for next week, and give directions to a new restaurant.
Start by greeting and talking about how your day has been. Then discuss weekend plans. Finally, explain how to get to a place you both want to visit.
Use present simple for routines, 'going to' for future plans, and imperatives for directions.
Vocabulary should include daily activities, leisure activities, and location/direction words.
Keep the conversation natural and flowing between all three topics.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ["Hey! So good to see you. How's your day been so far?"],
                'german': ['Hey! Schön dich zu sehen. Wie war dein Tag bisher?'],
                'spanish': ['¡Hola! Qué bueno verte. ¿Cómo ha ido tu día?'],
                'portuguese': ['Olá! Que bom ver-te. Como tem sido o teu dia?']
            }),
            'required_vocabulary': json.dumps([]),
            'conversation_flow': json.dumps({
                'exchanges': 10,
                'structure': 'Integrated test covering routines, plans, and directions'
            }),
            'number_of_exchanges': 10,
            'topic_specific_rules': 'TEST: Assess daily routines, making plans, and giving directions in a natural conversation.',
            'scenario_template': 'Coffee Shop Meetup - Testing topics 1-3'
        },

        # Topic 5: This is My Apartment
        {
            'level': 'A2',
            'topic_number': 5,
            'title_key': 'my_apartment',
            'subtopics': json.dumps(['means_of_transport', 'rooms_in_house', 'furniture_and_objects']),
            'conversation_contexts': json.dumps(['Showing your home', 'Describing living spaces', 'Transport to home']),
            'llm_prompt_template': """You are describing your apartment and home at A2 level.
Talk about rooms, furniture, and how you get to your home using different transport.
Use 'there is/are' for describing: 'There's a big sofa in the living room', 'There are two bedrooms'.
Describe locations: 'The kitchen is next to the bathroom', 'My desk is in front of the window'.
Discuss transport: 'I take the bus to get home', 'It's 20 minutes by subway'.
Include: living room, bedroom, kitchen, bathroom, balcony, sofa, table, chair, bed, wardrobe.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ['Welcome to my apartment! Let me show you around.', 'This is where I live. Come in!'],
                'german': ['Willkommen in meiner Wohnung! Ich zeige sie dir.', 'Hier wohne ich. Komm rein!'],
                'spanish': ['¡Bienvenido a mi apartamento! Te lo enseño.', '¡Aquí es donde vivo. Pasa!'],
                'portuguese': ['Bem-vindo ao meu apartamento! Vou mostrar-te.', 'É aqui que vivo. Entra!']
            }),
            'required_vocabulary': json.dumps(['living room', 'bedroom', 'kitchen', 'bathroom', 'furniture', 'comfortable', 'spacious', 'cozy']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Welcome → Tour of rooms → Describe furniture → Favorite room → How to get there'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': "Use 'there is/are' and prepositions of place. Practice describing spaces and objects.",
            'scenario_template': "A friend is visiting your apartment for the first time and you're giving them a tour."
        },

        # Topic 6: I Love Fast Food
        {
            'level': 'A2',
            'topic_number': 6,
            'title_key': 'love_fast_food',
            'subtopics': json.dumps(['meals_of_day', 'food_ingredients', 'favorite_recipes']),
            'conversation_contexts': json.dumps(['Discussing meals', 'Sharing recipes', 'Food preferences']),
            'llm_prompt_template': """You are discussing food, meals, and recipes at A2 level.
Talk about what you eat for different meals and your favorite foods.
Describe ingredients and simple recipes: 'You need eggs, flour, and milk', 'First, you mix...then you cook...'
Use quantifiers: 'some', 'a lot of', 'a little', 'a few'.
Discuss preferences: 'I love pasta', 'I don't like spicy food', 'My favorite meal is...'
Include meals: breakfast, lunch, dinner, snack; and foods: pizza, burger, salad, soup, sandwich.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ["What's your favorite food? I absolutely love pizza!", "Let's talk about food - what did you have for lunch?"],
                'german': ['Was ist dein Lieblingsessen? Ich liebe Pizza!', 'Lass uns über Essen reden - was hattest du zum Mittagessen?'],
                'spanish': ['¿Cuál es tu comida favorita? ¡Me encanta la pizza!', 'Hablemos de comida - ¿qué almorzaste?'],
                'portuguese': ['Qual é a tua comida favorita? Adoro pizza!', 'Vamos falar de comida - o que almoçaste?']
            }),
            'required_vocabulary': json.dumps(['breakfast', 'lunch', 'dinner', 'delicious', 'ingredients', 'recipe', 'cook', 'prepare']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Favorite foods → Typical meals → Share a recipe → Food preferences → Restaurant recommendations'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Practice food vocabulary, quantifiers, and sequencing words for recipes.',
            'scenario_template': "You're at a food festival with a friend, trying different foods and sharing your favorites."
        },

        # Topic 7: Ordering Dinner
        {
            'level': 'A2',
            'topic_number': 7,
            'title_key': 'ordering_dinner',
            'subtopics': json.dumps(['restaurant_ordering', 'food_preferences', 'cooking_at_home']),
            'conversation_contexts': json.dumps(['At a restaurant', 'Ordering takeaway', 'Dinner decisions']),
            'llm_prompt_template': """You are in a restaurant ordering food at A2 level.
Practice ordering meals, asking about dishes, and expressing preferences.
Use polite forms: 'I would like...', 'Could I have...?', 'May I see the menu?'
Ask about food: 'What does it come with?', 'Is it spicy?', 'What do you recommend?'
Express preferences: 'I prefer...', 'I'm allergic to...', 'No onions, please'.
Include: starter, main course, dessert, drinks, bill, tip.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ['Good evening! Table for two, please.', "Hi! We'd like to order dinner."],
                'german': ['Guten Abend! Einen Tisch für zwei, bitte.', 'Hallo! Wir möchten zu Abend essen.'],
                'spanish': ['¡Buenas noches! Mesa para dos, por favor.', '¡Hola! Queremos cenar.'],
                'portuguese': ['Boa noite! Mesa para dois, por favor.', 'Olá! Gostaríamos de jantar.']
            }),
            'required_vocabulary': json.dumps(['menu', 'order', 'recommend', 'bill', 'tip', 'starter', 'main course', 'dessert']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Get seated → Read menu → Order food → Dietary requirements → Ask for bill'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use polite restaurant language and practice making specific requests.',
            'scenario_template': "You're at a new restaurant with a friend, ordering dinner and trying their specialties."
        },

        # Topic 8: TEST CHECKPOINT 2
        {
            'level': 'A2',
            'topic_number': 8,
            'title_key': 'test_checkpoint_2',
            'subtopics': json.dumps(['home_and_food', 'meals_and_restaurants', 'descriptions']),
            'conversation_contexts': json.dumps(['Dinner Party Planning']),
            'llm_prompt_template': """You are planning a dinner party at your apartment at A2 level.
You will describe your apartment, plan the menu, and discuss ordering some items from a restaurant.
Start by describing where the party will be. Then discuss what food to prepare and what to order. Finally, make the arrangements.
Use 'there is/are' for descriptions, food vocabulary, and polite ordering language.
Include details about rooms, furniture, ingredients, and restaurant dishes.
Keep the conversation flowing naturally through all topics.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ["I'm so excited about the dinner party at my place this weekend!"],
                'german': ['Ich freue mich so auf die Dinnerparty bei mir am Wochenende!'],
                'spanish': ['¡Estoy muy emocionado por la cena en mi casa este fin de semana!'],
                'portuguese': ['Estou tão entusiasmado com o jantar em minha casa neste fim de semana!']
            }),
            'required_vocabulary': json.dumps([]),
            'conversation_flow': json.dumps({
                'exchanges': 10,
                'structure': 'Integrated test covering apartment, food, and ordering'
            }),
            'number_of_exchanges': 10,
            'topic_specific_rules': 'TEST: Assess describing spaces, food discussion, and ordering in an integrated scenario.',
            'scenario_template': 'Dinner Party Planning - Testing topics 5-7'
        },

        # Topic 9: I Got Sick
        {
            'level': 'A2',
            'topic_number': 9,
            'title_key': 'got_sick',
            'subtopics': json.dumps(['describing_feelings', 'symptoms', 'doctor_visit']),
            'conversation_contexts': json.dumps(['Feeling unwell', 'At the doctor', 'Calling in sick']),
            'llm_prompt_template': """You are discussing health and sickness at A2 level.
Describe how you feel and talk about symptoms and doctor visits.
Use body parts: head, stomach, throat, back. Symptoms: headache, fever, cough, pain.
Express feelings: 'I feel terrible', 'My head hurts', 'I have a sore throat'.
At doctor: 'I've been feeling sick since yesterday', 'It started on Monday'.
Give advice: 'You should rest', 'Take this medicine twice a day'.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ["I don't feel very well today.", "You don't look well. Are you okay?"],
                'german': ['Mir geht es heute nicht gut.', 'Du siehst nicht gut aus. Geht es dir gut?'],
                'spanish': ['No me siento muy bien hoy.', 'No te ves bien. ¿Estás bien?'],
                'portuguese': ['Não me sinto muito bem hoje.', 'Não pareces bem. Estás bem?']
            }),
            'required_vocabulary': json.dumps(['headache', 'fever', 'cough', 'medicine', 'doctor', 'rest', 'feel better', 'sick']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Describe symptoms → When it started → Suggest seeing doctor → Get advice → Thank for help'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Practice health vocabulary, present perfect for duration, and giving advice with should.',
            'scenario_template': "You're calling your boss to explain you can't come to work because you're sick."
        },

        # Topic 10: I Exercise Daily
        {
            'level': 'A2',
            'topic_number': 10,
            'title_key': 'exercise_daily',
            'subtopics': json.dumps(['getting_medicine', 'staying_healthy', 'healthy_habits']),
            'conversation_contexts': json.dumps(['Fitness routine', 'Health habits', 'Lifestyle choices']),
            'llm_prompt_template': """You are discussing exercise and healthy lifestyle at A2 level.
Talk about exercise routines, healthy habits, and staying fit.
Use frequency adverbs: 'I always/usually/sometimes/never...'.
Discuss activities: 'I go jogging every morning', 'I do yoga twice a week'.
Compare habits: 'I used to eat junk food, but now I eat healthy'.
Give suggestions: 'You should try swimming', 'Why don't you join a gym?'
Include: exercise, gym, running, swimming, yoga, healthy food, sleep well.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ['Do you exercise regularly? I just started going to the gym.', 'How do you stay healthy?'],
                'german': ['Trainierst du regelmäßig? Ich habe gerade angefangen, ins Fitnessstudio zu gehen.', 'Wie bleibst du gesund?'],
                'spanish': ['¿Haces ejercicio regularmente? Acabo de empezar a ir al gimnasio.', '¿Cómo te mantienes saludable?'],
                'portuguese': ['Fazes exercício regularmente? Acabei de começar a ir ao ginásio.', 'Como te manténs saudável?']
            }),
            'required_vocabulary': json.dumps(['exercise', 'gym', 'healthy', 'fitness', 'workout', 'diet', 'sleep', 'energy']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Current routine → Benefits noticed → Compare past habits → Share tips → Make exercise plans'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use frequency adverbs and present perfect. Practice giving health advice.',
            'scenario_template': "You meet someone at the gym who asks about your fitness routine and healthy lifestyle."
        },

        # Topic 11: I Want to Go to Japan
        {
            'level': 'A2',
            'topic_number': 11,
            'title_key': 'want_go_japan',
            'subtopics': json.dumps(['travel_destinations', 'travel_arrangements', 'describing_trips']),
            'conversation_contexts': json.dumps(['Dream vacations', 'Travel planning', 'Past trips']),
            'llm_prompt_template': """You are discussing travel plans and destinations at A2 level.
Talk about places you want to visit and travel experiences.
Use 'would like to' for wishes: 'I'd like to visit Japan', 'I want to see the temples'.
Discuss plans: 'I'm planning to go next year', 'I'm saving money for the trip'.
Describe past trips: 'I went to Paris last summer', 'We stayed in a nice hotel'.
Include: passport, visa, flight, hotel, sightseeing, culture, food, souvenirs.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ["I've always wanted to go to Japan. Have you been there?", "Where's your dream vacation destination?"],
                'german': ['Ich wollte schon immer nach Japan. Warst du schon dort?', 'Was ist dein Traumreiseziel?'],
                'spanish': ['Siempre he querido ir a Japón. ¿Has estado allí?', '¿Cuál es tu destino de vacaciones soñado?'],
                'portuguese': ['Sempre quis ir ao Japão. Já lá estiveste?', 'Qual é o teu destino de férias de sonho?']
            }),
            'required_vocabulary': json.dumps(['travel', 'vacation', 'tourist', 'sightseeing', 'culture', 'adventure', 'explore', 'visit']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Dream destination → Why interested → Travel plans → Previous trips → Travel tips'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Practice conditional would like, future plans, and past simple for experiences.',
            'scenario_template': "You're at a travel agency discussing your dream vacation to Japan."
        },

        # Topic 12: TEST CHECKPOINT 3
        {
            'level': 'A2',
            'topic_number': 12,
            'title_key': 'test_checkpoint_3',
            'subtopics': json.dumps(['health', 'fitness', 'travel']),
            'conversation_contexts': json.dumps(['Wellness Retreat Planning']),
            'llm_prompt_template': """You are planning a wellness retreat vacation at A2 level.
You will discuss feeling stressed (health), your exercise goals, and planning a healthy travel destination.
Start by talking about recent stress and health. Then discuss fitness goals. Finally, plan a wellness vacation together.
Use health vocabulary, exercise terms, and travel planning language.
Include symptoms, healthy habits, and destination details.
Make the conversation flow naturally between all topics.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ["I've been so stressed lately. I think I need a wellness vacation!"],
                'german': ['Ich war in letzter Zeit so gestresst. Ich brauche einen Wellness-Urlaub!'],
                'spanish': ['He estado tan estresado últimamente. ¡Creo que necesito unas vacaciones de bienestar!'],
                'portuguese': ['Tenho estado tão stressado ultimamente. Acho que preciso de umas férias de bem-estar!']
            }),
            'required_vocabulary': json.dumps([]),
            'conversation_flow': json.dumps({
                'exchanges': 10,
                'structure': 'Integrated test covering health, exercise, and travel'
            }),
            'number_of_exchanges': 10,
            'topic_specific_rules': 'TEST: Assess health discussion, fitness habits, and travel planning in an integrated scenario.',
            'scenario_template': 'Wellness Retreat Planning - Testing topics 9-11'
        },

        # Topic 13: Let's Take a Trip
        {
            'level': 'A2',
            'topic_number': 13,
            'title_key': 'lets_take_trip',
            'subtopics': json.dumps(['hotel_check_in', 'luggage_issues', 'past_trip_stories']),
            'conversation_contexts': json.dumps(['At hotel reception', 'Airport situations', 'Sharing experiences']),
            'llm_prompt_template': """You are at a hotel checking in and discussing travel at A2 level.
Practice hotel vocabulary and sharing past travel experiences.
Check-in language: 'I have a reservation', 'Here's my confirmation', 'What time is breakfast?'
Describe past trips: 'Last year I went to...', 'The hotel was amazing', 'We had some problems with...'
Use past simple and past continuous: 'I was staying at...when...', 'While we were traveling...'
Include: reservation, key card, luggage, reception, check-out, facilities.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ['Hello, I have a reservation for tonight.', 'Hi! We just arrived from the airport.'],
                'german': ['Hallo, ich habe eine Reservierung für heute Nacht.', 'Hallo! Wir sind gerade vom Flughafen angekommen.'],
                'spanish': ['Hola, tengo una reserva para esta noche.', '¡Hola! Acabamos de llegar del aeropuerto.'],
                'portuguese': ['Olá, tenho uma reserva para esta noite.', 'Olá! Acabámos de chegar do aeroporto.']
            }),
            'required_vocabulary': json.dumps(['reservation', 'check-in', 'luggage', 'room key', 'reception', 'facilities', 'view', 'floor']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Check-in process → Room preferences → Ask about facilities → Share past experience → Get recommendations'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Practice hotel vocabulary and past tenses for travel stories.',
            'scenario_template': "You're checking into a hotel after a long journey and chatting with the receptionist."
        },

        # Topic 14: Meeting Someone New
        {
            'level': 'A2',
            'topic_number': 14,
            'title_key': 'meeting_someone_new',
            'subtopics': json.dumps(['self_introduction', 'describing_people', 'family_and_friends']),
            'conversation_contexts': json.dumps(['Social gathering', 'New neighbor', 'Work event']),
            'llm_prompt_template': """You are meeting someone new at a social event at A2 level.
Practice extended introductions and describing people in your life.
Introduce yourself with details: 'I work as...', 'I've been living here for...', 'Originally I'm from...'.
Describe people: 'My sister is tall and friendly', 'My best friend is really funny'.
Use present perfect: 'I've known him for 5 years', 'We've been friends since school'.
Ask about others: 'Do you have siblings?', 'What does your partner do?'""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ["Hi, I don't think we've met. I'm...", "Nice to meet you! Are you new to the neighborhood?"],
                'german': ['Hallo, ich glaube, wir kennen uns noch nicht. Ich bin...', 'Schön dich kennenzulernen! Bist du neu in der Gegend?'],
                'spanish': ['Hola, creo que no nos conocemos. Soy...', '¡Encantado de conocerte! ¿Eres nuevo en el barrio?'],
                'portuguese': ['Olá, acho que não nos conhecemos. Sou...', 'Prazer em conhecer-te! És novo no bairro?']
            }),
            'required_vocabulary': json.dumps(['introduce', 'personality', 'appearance', 'relationship', 'colleague', 'neighbor', 'friendly', 'outgoing']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Introduction → Background info → Ask about them → Describe family/friends → Find common interests'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Practice present perfect for duration and describing personality traits.',
            'scenario_template': "You're at a neighborhood barbecue meeting new neighbors for the first time."
        },

        # Topic 15: Make a Reservation
        {
            'level': 'A2',
            'topic_number': 15,
            'title_key': 'make_reservation',
            'subtopics': json.dumps(['favorite_places', 'travel_booking', 'describing_town']),
            'conversation_contexts': json.dumps(['Booking restaurants', 'Travel arrangements', 'Local recommendations']),
            'llm_prompt_template': """You are making reservations and discussing favorite places at A2 level.
Practice making bookings and describing places in your town.
Make reservations: 'I'd like to book a table for...', 'Is it available on...?', 'Can I reserve...?'
Describe places: 'It's the best restaurant in town', 'They have amazing views', 'It's always crowded'.
Give recommendations: 'You should try...', 'I recommend...', 'Don't miss...'.
Use superlatives: 'the best', 'the most popular', 'the nicest'.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ["I'd like to make a reservation for this weekend.", "Can you recommend a good restaurant in town?"],
                'german': ['Ich möchte eine Reservierung für dieses Wochenende machen.', 'Kannst du ein gutes Restaurant in der Stadt empfehlen?'],
                'spanish': ['Me gustaría hacer una reserva para este fin de semana.', '¿Puedes recomendar un buen restaurante en la ciudad?'],
                'portuguese': ['Gostaria de fazer uma reserva para este fim de semana.', 'Podes recomendar um bom restaurante na cidade?']
            }),
            'required_vocabulary': json.dumps(['reservation', 'book', 'available', 'recommend', 'popular', 'atmosphere', 'location', 'special']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Request reservation → Specify details → Ask about place → Get recommendations → Confirm booking'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Practice making polite requests and using superlatives for recommendations.',
            'scenario_template': "You're calling to make a reservation at a popular restaurant for a special occasion."
        },

        # Topic 16: FINAL TEST
        {
            'level': 'A2',
            'topic_number': 16,
            'title_key': 'test_final',
            'subtopics': json.dumps(['travel_experiences', 'meeting_people', 'local_places']),
            'conversation_contexts': json.dumps(['Tourist Information Center']),
            'llm_prompt_template': """You are at a tourist information center in a new city at A2 level.
You will share your travel experiences, meet the helpful staff member, and get recommendations for local places.
Start by explaining your trip so far. Then get to know the staff member. Finally, ask for and make reservations at recommended places.
Use past tenses for experiences, present perfect for duration, and polite booking language.
Include travel stories, personal descriptions, and local recommendations.
Create a natural conversation that flows through all topics.""",
            'word_limit': 50,
            'opening_phrases': json.dumps({
                'english': ["Hi! I just arrived in town yesterday and I need some local recommendations."],
                'german': ['Hallo! Ich bin gestern in der Stadt angekommen und brauche einige lokale Empfehlungen.'],
                'spanish': ['¡Hola! Llegué ayer a la ciudad y necesito algunas recomendaciones locales.'],
                'portuguese': ['Olá! Cheguei ontem à cidade e preciso de algumas recomendações locais.']
            }),
            'required_vocabulary': json.dumps([]),
            'conversation_flow': json.dumps({
                'exchanges': 10,
                'structure': 'Integrated test covering travel, introductions, and reservations'
            }),
            'number_of_exchanges': 10,
            'topic_specific_rules': 'FINAL TEST: Assess travel stories, meeting people, and making arrangements comprehensively.',
            'scenario_template': 'Tourist Information Center - Testing topics 13-15'
        }
    ]

    with app.app_context():
        print("Creating A2 topics...")
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
        print(f"\nSuccessfully created {topics_created} A2 topics!")

        # Verify the count
        a2_count = TopicDefinition.query.filter_by(level='A2').count()
        print(f"Total A2 topics in database: {a2_count}")

if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION: Populate A2 Topics (16 total)")
    print("=" * 60)
    create_a2_topics()
    print("\nA2 level is now ready with all 16 topics!")