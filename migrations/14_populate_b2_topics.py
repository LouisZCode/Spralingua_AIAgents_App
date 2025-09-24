# Migration to populate B2 level topics (16 total including 4 tests)
# Based on Linguatec B2 curriculum guide

import sys
import os
import json

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from models.topic_definition import TopicDefinition
from app import app

def create_b2_topics():
    """Create all 16 B2 topics including 4 integrated tests."""

    topics = [
        # Topic 1: Getting Around Town
        {
            'level': 'B2',
            'topic_number': 1,
            'title_key': 'getting_around_town',
            'subtopics': json.dumps(['asking_directions', 'transport_information', 'past_trips', 'travel_apps']),
            'conversation_contexts': json.dumps(['City navigation', 'Transport planning', 'Travel experiences']),
            'llm_prompt_template': """You are discussing urban navigation and travel at B2 level.
Engage in sophisticated discussion about getting around, past travel experiences, and modern navigation tools.
Use complex structures: 'Had I known about the traffic, I would have...', 'By the time I realized...'.
Include idioms: 'off the beaten path', 'take the scenic route', 'hit the road'.
Discuss travel apps critically: 'While the app claims to...', 'The algorithm tends to...'.
Share anecdotes: 'You won't believe what happened when...', 'I'll never forget the time...'.
Use all tenses naturally including past perfect and future perfect.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["I've been exploring some alternative routes lately. The usual way is getting ridiculous.", "Have you tried any of those new navigation apps? I'm torn between convenience and privacy."],
                'german': ['Ich habe letztens einige alternative Routen erkundet. Der übliche Weg wird lächerlich.', 'Hast du eine dieser neuen Navigations-Apps ausprobiert? Ich bin zwischen Komfort und Privatsphäre hin- und hergerissen.'],
                'spanish': ['He estado explorando algunas rutas alternativas últimamente. El camino habitual se está volviendo ridículo.', '¿Has probado alguna de esas nuevas apps de navegación? Estoy entre la conveniencia y la privacidad.'],
                'portuguese': ['Tenho explorado algumas rotas alternativas ultimamente. O caminho habitual está a ficar ridículo.', 'Experimentaste alguma dessas novas apps de navegação? Estou dividido entre conveniência e privacidade.']
            }),
            'required_vocabulary': json.dumps(['navigate', 'commute', 'congestion', 'shortcut', 'detour', 'infrastructure', 'efficient', 'sustainable']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Current transport challenges → Share travel anecdote → Discuss technology impact → Compare old vs new methods → Future of urban transport'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use sophisticated vocabulary and complex grammar. Include idioms and cultural references naturally.',
            'scenario_template': "You're discussing the challenges of modern city navigation with someone who's lived in the city for decades."
        },

        # Topic 2: At a Restaurant
        {
            'level': 'B2',
            'topic_number': 2,
            'title_key': 'at_restaurant_b2',
            'subtopics': json.dumps(['sophisticated_ordering', 'cuisine_preferences', 'restaurant_reviews', 'food_culture']),
            'conversation_contexts': json.dumps(['Fine dining', 'Food criticism', 'Culinary discussion']),
            'llm_prompt_template': """You are having a sophisticated restaurant conversation at B2 level.
Discuss food with nuance, express refined preferences, and engage in culinary critique.
Use subjunctive mood: 'I would suggest that the chef prepare...', 'If I were to recommend...'.
Express subtle criticism: 'While the presentation is impressive, the flavors don't quite...'.
Discuss cuisine authentically: 'The way they've interpreted the traditional recipe...'.
Use food idioms: 'food for thought', 'not my cup of tea', 'acquired taste'.
Make sophisticated comparisons: 'Unlike the Mediterranean approach, this cuisine...'.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["The reviews were quite mixed, but I'm curious about their take on fusion cuisine.", "I've heard their chef trained in Lyon. That should guarantee something special."],
                'german': ['Die Bewertungen waren ziemlich gemischt, aber ich bin neugierig auf ihre Interpretation der Fusionsküche.', 'Ich habe gehört, ihr Koch wurde in Lyon ausgebildet. Das sollte etwas Besonderes garantieren.'],
                'spanish': ['Las reseñas eran bastante mixtas, pero tengo curiosidad por su interpretación de la cocina fusión.', 'He oído que su chef se formó en Lyon. Eso debería garantizar algo especial.'],
                'portuguese': ['As críticas eram bastante mistas, mas estou curioso sobre a interpretação deles da cozinha de fusão.', 'Ouvi dizer que o chef deles treinou em Lyon. Isso deve garantir algo especial.']
            }),
            'required_vocabulary': json.dumps(['palate', 'cuisine', 'ambiance', 'presentation', 'authentic', 'fusion', 'gourmet', 'culinary']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Restaurant atmosphere → Discuss menu sophistication → Share culinary experiences → Critique dishes → Food culture discussion'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use subjunctive mood and sophisticated food vocabulary. Express nuanced opinions.',
            'scenario_template': "You're at an upscale restaurant with a food enthusiast, discussing culinary trends and experiences."
        },

        # Topic 3: At the Doctor
        {
            'level': 'B2',
            'topic_number': 3,
            'title_key': 'at_doctor_b2',
            'subtopics': json.dumps(['complex_symptoms', 'medical_procedures', 'healthcare_systems', 'wellness_philosophy']),
            'conversation_contexts': json.dumps(['Medical consultation', 'Health insurance', 'Wellness discussion']),
            'llm_prompt_template': """You are discussing health and medical care at B2 level.
Describe complex medical situations and discuss healthcare philosophically.
Use medical terminology naturally: 'chronic', 'acute', 'diagnosis', 'prognosis'.
Discuss healthcare systems: 'The way our healthcare system handles...', 'Compared to other countries...'.
Express concern diplomatically: 'I'm somewhat concerned about...', 'What worries me is...'.
Use hypothetical situations: 'Suppose the treatment doesn't work...', 'What if the symptoms persist?'.
Include wellness philosophy: 'I believe in a holistic approach...', 'Prevention is better than cure'.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["I've been experiencing some rather peculiar symptoms lately. Nothing alarming, but concerning.", "The healthcare debate is fascinating. How do you balance accessibility with quality?"],
                'german': ['Ich habe in letzter Zeit einige ziemlich eigenartige Symptome. Nichts Alarmierendes, aber beunruhigend.', 'Die Gesundheitsdebatte ist faszinierend. Wie balanciert man Zugänglichkeit mit Qualität?'],
                'spanish': ['He estado experimentando algunos síntomas bastante peculiares últimamente. Nada alarmante, pero preocupante.', 'El debate sobre la sanidad es fascinante. ¿Cómo equilibras accesibilidad con calidad?'],
                'portuguese': ['Tenho experienciado alguns sintomas bastante peculiares ultimamente. Nada alarmante, mas preocupante.', 'O debate sobre saúde é fascinante. Como equilibras acessibilidade com qualidade?']
            }),
            'required_vocabulary': json.dumps(['symptoms', 'diagnosis', 'treatment', 'prescription', 'specialist', 'chronic', 'preventive', 'wellness']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Describe symptoms sophisticatedly → Discuss treatment options → Healthcare system comparison → Wellness philosophy → Future of medicine'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use medical vocabulary appropriately. Discuss healthcare systems critically.',
            'scenario_template': "You're discussing modern healthcare challenges and personal wellness philosophies with a healthcare professional."
        },

        # Topic 4: TEST CHECKPOINT 1
        {
            'level': 'B2',
            'topic_number': 4,
            'title_key': 'test_checkpoint_1',
            'subtopics': json.dumps(['urban_life', 'dining_culture', 'healthcare']),
            'conversation_contexts': json.dumps(['City Living Discussion']),
            'llm_prompt_template': """You are at a dinner party discussing city living at B2 level.
You will discuss urban transport challenges, share restaurant recommendations, and debate healthcare in cities.
Start with comparing different neighborhoods and transport. Then discuss the local food scene. Finally, talk about access to healthcare in urban areas.
Use sophisticated vocabulary, idioms, and complex grammar structures throughout.
Include cultural references, subjunctive mood, and hypothetical situations.
Demonstrate mastery of all tenses and nuanced opinion expression.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["Living in this city has its challenges, but the cultural diversity makes up for it, don't you think?"],
                'german': ['Das Leben in dieser Stadt hat seine Herausforderungen, aber die kulturelle Vielfalt macht das wett, findest du nicht?'],
                'spanish': ['Vivir en esta ciudad tiene sus desafíos, pero la diversidad cultural lo compensa, ¿no crees?'],
                'portuguese': ['Viver nesta cidade tem os seus desafios, mas a diversidade cultural compensa, não achas?']
            }),
            'required_vocabulary': json.dumps([]),
            'conversation_flow': json.dumps({
                'exchanges': 10,
                'structure': 'Integrated test covering urban navigation, dining culture, and healthcare discussion'
            }),
            'number_of_exchanges': 10,
            'topic_specific_rules': 'TEST: Assess sophisticated discussion of city living, food culture, and healthcare systems.',
            'scenario_template': 'City Living Discussion - Testing topics 1-3'
        },

        # Topic 5: At Work
        {
            'level': 'B2',
            'topic_number': 5,
            'title_key': 'at_work_b2',
            'subtopics': json.dumps(['workplace_dynamics', 'professional_communication', 'leadership', 'career_development']),
            'conversation_contexts': json.dumps(['Professional meeting', 'Career coaching', 'Workplace discussion']),
            'llm_prompt_template': """You are discussing professional life and workplace dynamics at B2 level.
Engage in sophisticated discussion about careers, leadership, and workplace communication.
Use business idioms: 'think outside the box', 'move the needle', 'low-hanging fruit', 'paradigm shift'.
Discuss leadership: 'Effective leaders tend to...', 'The key to motivation is...'.
Express professional opinions: 'From a strategic standpoint...', 'Looking at the bigger picture...'.
Use diplomatic language: 'With all due respect...', 'I see where you're coming from, however...'.
Include remote work discussion: 'The shift to hybrid work has fundamentally...'.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["The workplace dynamics have shifted dramatically. How is your company adapting to the new normal?", "Leadership styles need to evolve. The old command-and-control approach just doesn't cut it anymore."],
                'german': ['Die Arbeitsplatzdynamik hat sich dramatisch verändert. Wie passt sich Ihr Unternehmen an die neue Normalität an?', 'Führungsstile müssen sich entwickeln. Der alte Befehls- und Kontrollansatz funktioniert einfach nicht mehr.'],
                'spanish': ['La dinámica laboral ha cambiado drásticamente. ¿Cómo se está adaptando tu empresa a la nueva normalidad?', 'Los estilos de liderazgo necesitan evolucionar. El viejo enfoque de mando y control ya no funciona.'],
                'portuguese': ['A dinâmica do local de trabalho mudou drasticamente. Como é que a tua empresa se está a adaptar ao novo normal?', 'Os estilos de liderança precisam de evoluir. A velha abordagem de comando e controlo já não funciona.']
            }),
            'required_vocabulary': json.dumps(['leadership', 'strategy', 'stakeholder', 'innovative', 'collaborate', 'delegate', 'mentor', 'performance']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Current work situation → Leadership philosophy → Communication challenges → Career development → Future of work'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use business idioms and diplomatic language. Discuss workplace dynamics sophisticatedly.',
            'scenario_template': "You're at a professional development seminar discussing modern workplace challenges and leadership."
        },

        # Topic 6: At School
        {
            'level': 'B2',
            'topic_number': 6,
            'title_key': 'at_school_b2',
            'subtopics': json.dumps(['higher_education', 'academic_research', 'study_abroad', 'career_paths']),
            'conversation_contexts': json.dumps(['University discussion', 'Academic planning', 'Education debate']),
            'llm_prompt_template': """You are discussing higher education and academic life at B2 level.
Engage in intellectual discussion about education, research, and academic careers.
Use academic vocabulary: 'thesis', 'methodology', 'peer review', 'curriculum', 'pedagogy'.
Discuss education critically: 'The current system fails to...', 'Traditional methods versus...'.
Express academic opinions: 'Research suggests that...', 'The literature indicates...'.
Compare education systems: 'Unlike the American system, European universities...'.
Include online learning: 'The democratization of education through MOOCs...'.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["The whole higher education system needs rethinking. The debt crisis alone is unsustainable.", "I'm considering pursuing a master's abroad. The exposure to different methodologies is invaluable."],
                'german': ['Das gesamte Hochschulsystem muss überdacht werden. Allein die Schuldenkrise ist nicht nachhaltig.', 'Ich überlege, einen Master im Ausland zu machen. Der Kontakt mit verschiedenen Methoden ist unbezahlbar.'],
                'spanish': ['Todo el sistema de educación superior necesita repensarse. Solo la crisis de deuda es insostenible.', 'Estoy considerando hacer un máster en el extranjero. La exposición a diferentes metodologías es invaluable.'],
                'portuguese': ['Todo o sistema de ensino superior precisa ser repensado. Só a crise da dívida é insustentável.', 'Estou a considerar fazer um mestrado no estrangeiro. A exposição a diferentes metodologias é inestimável.']
            }),
            'required_vocabulary': json.dumps(['academic', 'research', 'dissertation', 'scholarship', 'curriculum', 'pedagogy', 'methodology', 'interdisciplinary']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Education system critique → Study abroad benefits → Research interests → Career prospects → Future of education'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use academic vocabulary and critical analysis. Discuss education systems comparatively.',
            'scenario_template': "You're at a university alumni event discussing the value and future of higher education."
        },

        # Topic 7: Shopping
        {
            'level': 'B2',
            'topic_number': 7,
            'title_key': 'shopping_b2',
            'subtopics': json.dumps(['consumer_behavior', 'online_vs_retail', 'brand_culture', 'sustainable_shopping']),
            'conversation_contexts': json.dumps(['Consumer trends', 'Shopping philosophy', 'Retail discussion']),
            'llm_prompt_template': """You are discussing shopping and consumer culture at B2 level.
Analyze shopping habits, consumer behavior, and the impact of retail on society.
Discuss consumption critically: 'The psychology behind impulse buying...', 'Consumer culture has...'.
Compare shopping methods: 'While online shopping offers convenience, the tactile experience...'.
Use economic terms: 'market saturation', 'consumer confidence', 'brand loyalty'.
Include sustainability: 'The environmental cost of fast fashion...', 'Conscious consumerism'.
Express sophisticated preferences: 'I've become increasingly selective about...'.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["The death of retail has been greatly exaggerated. Physical stores offer something algorithms can't replicate.", "I've been trying to be more conscious about my consumption habits. It's harder than it seems."],
                'german': ['Der Tod des Einzelhandels wurde stark übertrieben. Physische Geschäfte bieten etwas, das Algorithmen nicht replizieren können.', 'Ich versuche, bewusster mit meinen Konsumgewohnheiten umzugehen. Es ist schwieriger als es scheint.'],
                'spanish': ['La muerte del comercio minorista ha sido muy exagerada. Las tiendas físicas ofrecen algo que los algoritmos no pueden replicar.', 'He estado tratando de ser más consciente de mis hábitos de consumo. Es más difícil de lo que parece.'],
                'portuguese': ['A morte do retalho foi muito exagerada. As lojas físicas oferecem algo que os algoritmos não podem replicar.', 'Tenho tentado ser mais consciente dos meus hábitos de consumo. É mais difícil do que parece.']
            }),
            'required_vocabulary': json.dumps(['consumer', 'retail', 'e-commerce', 'sustainable', 'brand', 'marketing', 'algorithm', 'personalization']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Shopping evolution → Consumer psychology → Online vs physical → Sustainability concerns → Future of retail'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Analyze consumer culture critically. Use economic and psychological concepts.',
            'scenario_template': "You're discussing the future of retail and conscious consumerism with a marketing professional."
        },

        # Topic 8: TEST CHECKPOINT 2
        {
            'level': 'B2',
            'topic_number': 8,
            'title_key': 'test_checkpoint_2',
            'subtopics': json.dumps(['professional_life', 'education', 'consumer_culture']),
            'conversation_contexts': json.dumps(['Career Fair Networking']),
            'llm_prompt_template': """You are at a career fair networking event at B2 level.
You will discuss workplace trends, the value of education, and how consumer behavior affects businesses.
Start with professional development and workplace changes. Then discuss the role of education in careers. Finally, analyze how shopping trends impact business strategies.
Use business idioms, academic vocabulary, and consumer psychology concepts.
Demonstrate sophisticated argumentation and cultural awareness.
Include hypothetical scenarios and complex comparisons.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["These career fairs have changed so much. It's all about personal branding and digital presence now."],
                'german': ['Diese Karrieremessen haben sich so sehr verändert. Es geht jetzt alles um Personal Branding und digitale Präsenz.'],
                'spanish': ['Estas ferias de empleo han cambiado mucho. Ahora todo es sobre marca personal y presencia digital.'],
                'portuguese': ['Estas feiras de emprego mudaram tanto. Agora é tudo sobre marca pessoal e presença digital.']
            }),
            'required_vocabulary': json.dumps([]),
            'conversation_flow': json.dumps({
                'exchanges': 10,
                'structure': 'Integrated test covering workplace dynamics, education value, and consumer trends'
            }),
            'number_of_exchanges': 10,
            'topic_specific_rules': 'TEST: Assess professional discourse, academic discussion, and consumer analysis.',
            'scenario_template': 'Career Fair Networking - Testing topics 5-7'
        },

        # Topic 9: At the Airport
        {
            'level': 'B2',
            'topic_number': 9,
            'title_key': 'at_airport_b2',
            'subtopics': json.dumps(['travel_logistics', 'airport_experiences', 'customs_procedures', 'travel_stories']),
            'conversation_contexts': json.dumps(['Airport lounge', 'Flight delays', 'Travel planning']),
            'llm_prompt_template': """You are discussing air travel and airport experiences at B2 level.
Share sophisticated travel stories and discuss the complexities of modern air travel.
Use aviation terminology: 'turbulence', 'connecting flight', 'layover', 'priority boarding'.
Share anecdotes: 'I once had a 24-hour delay in Dubai, which turned out to be...'.
Discuss travel philosophically: 'Travel has become commoditized...', 'The romance of flying has...'.
Express frustration elegantly: 'While I understand the security measures, the inefficiency...'.
Include cultural observations: 'What struck me about Japanese airports was...'.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["Air travel has lost its glamour, hasn't it? Though I must admit, some airports are becoming destinations themselves.", "I've collected quite a few airport horror stories over the years. The worst was probably in..."],
                'german': ['Flugreisen haben ihren Glamour verloren, nicht wahr? Obwohl ich zugeben muss, dass einige Flughäfen selbst zu Reisezielen werden.', 'Ich habe im Laufe der Jahre einige Flughafen-Horrorgeschichten gesammelt. Die schlimmste war wahrscheinlich in...'],
                'spanish': ['Los viajes aéreos han perdido su glamour, ¿no? Aunque debo admitir que algunos aeropuertos se están convirtiendo en destinos.', 'He coleccionado bastantes historias de terror de aeropuertos a lo largo de los años. La peor fue probablemente en...'],
                'portuguese': ['As viagens aéreas perderam o seu glamour, não é? Embora deva admitir que alguns aeroportos estão a tornar-se destinos.', 'Colecionei bastantes histórias de terror de aeroportos ao longo dos anos. A pior foi provavelmente em...']
            }),
            'required_vocabulary': json.dumps(['layover', 'customs', 'immigration', 'turbulence', 'boarding', 'lounge', 'connection', 'itinerary']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Travel logistics discussion → Airport horror stories → Cultural differences → Security debate → Future of air travel'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use travel anecdotes and aviation terminology. Discuss travel philosophically.',
            'scenario_template': "You're in an airport lounge during a delay, swapping travel stories with a fellow seasoned traveler."
        },

        # Topic 10: At a Hotel
        {
            'level': 'B2',
            'topic_number': 10,
            'title_key': 'at_hotel_b2',
            'subtopics': json.dumps(['luxury_hotels', 'hotel_complaints', 'hospitality_industry', 'unusual_accommodations']),
            'conversation_contexts': json.dumps(['Hotel lobby', 'Concierge desk', 'Guest complaints']),
            'llm_prompt_template': """You are discussing hotels and hospitality at B2 level.
Engage in sophisticated discussion about accommodation, service standards, and hospitality trends.
Express dissatisfaction diplomatically: 'I'm afraid the room doesn't quite meet expectations...'.
Discuss hospitality: 'The art of hospitality seems to be lost...', 'Japanese omotenashi versus Western service...'.
Share experiences: 'The most extraordinary hotel I've stayed in...', 'I once had a suite upgrade in Paris...'.
Analyze trends: 'The boutique hotel movement...', 'Airbnb's disruption of traditional hospitality...'.
Use hospitality vocabulary: 'concierge', 'amenities', 'turndown service', 'complimentary'.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["The hospitality industry has changed dramatically. Service used to be an art form.", "I'm particularly interested in how hotels are adapting to the experience economy."],
                'german': ['Die Gastgewerbebranche hat sich dramatisch verändert. Service war früher eine Kunstform.', 'Ich bin besonders daran interessiert, wie sich Hotels an die Erlebniswirtschaft anpassen.'],
                'spanish': ['La industria hotelera ha cambiado dramáticamente. El servicio solía ser una forma de arte.', 'Me interesa particularmente cómo los hoteles se están adaptando a la economía de experiencias.'],
                'portuguese': ['A indústria hoteleira mudou drasticamente. O serviço costumava ser uma forma de arte.', 'Estou particularmente interessado em como os hotéis estão a adaptar-se à economia de experiências.']
            }),
            'required_vocabulary': json.dumps(['hospitality', 'amenities', 'concierge', 'boutique', 'luxury', 'accommodation', 'service', 'experience']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Hotel experiences → Service standards → Industry trends → Unusual accommodations → Future of hospitality'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Discuss hospitality sophisticatedly. Express complaints diplomatically.',
            'scenario_template': "You're discussing the evolution of hospitality with a hotel manager at a luxury establishment."
        },

        # Topic 11: Socializing
        {
            'level': 'B2',
            'topic_number': 11,
            'title_key': 'socializing_b2',
            'subtopics': json.dumps(['making_connections', 'conversation_art', 'technology_impact', 'social_dynamics']),
            'conversation_contexts': json.dumps(['Networking event', 'Social gathering', 'Deep conversation']),
            'llm_prompt_template': """You are discussing social dynamics and human connection at B2 level.
Engage in philosophical discussion about relationships, technology's impact on socializing, and human connection.
Discuss social dynamics: 'The paradox of being more connected yet lonelier...', 'Authentic connections versus networking...'.
Use psychological concepts: 'Social anxiety has become...', 'The Dunbar number suggests...'.
Express social observations: 'I've noticed that people tend to...', 'What fascinates me about human behavior is...'.
Include technology critique: 'While social media promised connection, it delivered...'.
Use metaphors: 'Conversation is a lost art', 'We're all islands in a digital sea'.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["Making genuine connections has become increasingly challenging in our digital age, don't you think?", "I find that the art of conversation is becoming extinct. People don't know how to be present anymore."],
                'german': ['Echte Verbindungen zu knüpfen wird in unserem digitalen Zeitalter immer schwieriger, findest du nicht?', 'Ich finde, dass die Kunst der Konversation ausstirbt. Die Leute wissen nicht mehr, wie man präsent ist.'],
                'spanish': ['Hacer conexiones genuinas se ha vuelto cada vez más desafiante en nuestra era digital, ¿no crees?', 'Encuentro que el arte de la conversación se está extinguiendo. La gente ya no sabe estar presente.'],
                'portuguese': ['Fazer conexões genuínas tornou-se cada vez mais desafiador na nossa era digital, não achas?', 'Acho que a arte da conversação está a extinguir-se. As pessoas já não sabem estar presentes.']
            }),
            'required_vocabulary': json.dumps(['connection', 'authentic', 'networking', 'presence', 'empathy', 'vulnerability', 'meaningful', 'superficial']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Modern socializing challenges → Technology impact → Art of conversation → Building connections → Future of relationships'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Discuss social dynamics philosophically. Use psychological and sociological concepts.',
            'scenario_template': "You're at a dinner party having a deep conversation about modern social connections and relationships."
        },

        # Topic 12: TEST CHECKPOINT 3
        {
            'level': 'B2',
            'topic_number': 12,
            'title_key': 'test_checkpoint_3',
            'subtopics': json.dumps(['travel_experiences', 'hospitality', 'social_connections']),
            'conversation_contexts': json.dumps(['International Conference Reception']),
            'llm_prompt_template': """You are at an international conference reception at B2 level.
You will share complex travel experiences, discuss hospitality across cultures, and explore how people connect globally.
Start with comparing international travel experiences. Then discuss hospitality standards worldwide. Finally, explore how global connections are changing.
Use sophisticated travel vocabulary, hospitality concepts, and social psychology.
Include cultural comparisons, philosophical observations, and personal anecdotes.
Demonstrate mastery of all B2 language features.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["These international gatherings always remind me how small the world has become, yet how diverse it remains."],
                'german': ['Diese internationalen Treffen erinnern mich immer daran, wie klein die Welt geworden ist und doch wie vielfältig sie bleibt.'],
                'spanish': ['Estos encuentros internacionales siempre me recuerdan lo pequeño que se ha vuelto el mundo, pero lo diverso que sigue siendo.'],
                'portuguese': ['Estes encontros internacionais sempre me lembram quão pequeno o mundo se tornou, mas quão diverso permanece.']
            }),
            'required_vocabulary': json.dumps([]),
            'conversation_flow': json.dumps({
                'exchanges': 10,
                'structure': 'Integrated test covering travel, hospitality, and global social connections'
            }),
            'number_of_exchanges': 10,
            'topic_specific_rules': 'TEST: Assess sophisticated discussion of travel, hospitality, and human connections.',
            'scenario_template': 'International Conference Reception - Testing topics 9-11'
        },

        # Topic 13: Interacting on Social Media
        {
            'level': 'B2',
            'topic_number': 13,
            'title_key': 'social_media_b2',
            'subtopics': json.dumps(['platform_analysis', 'digital_identity', 'influencer_culture', 'privacy_concerns']),
            'conversation_contexts': json.dumps(['Digital marketing discussion', 'Privacy debate', 'Online culture analysis']),
            'llm_prompt_template': """You are discussing social media's impact on society at B2 level.
Analyze social media critically, discussing digital identity, privacy, and cultural implications.
Use digital terminology: 'algorithm', 'engagement metrics', 'echo chamber', 'viral content'.
Discuss critically: 'The commodification of personal data...', 'Surveillance capitalism has...'.
Express concerns: 'What troubles me about influencer culture...', 'The psychological manipulation through...'.
Include generational differences: 'Digital natives versus digital immigrants...'.
Use metaphors: 'Social media is the new town square', 'We're all performers now'.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["The social media landscape has become a minefield of privacy concerns and psychological manipulation.", "I'm fascinated by how we've all become content creators, whether we realize it or not."],
                'german': ['Die Social-Media-Landschaft ist zu einem Minenfeld von Datenschutzbedenken und psychologischer Manipulation geworden.', 'Ich bin fasziniert davon, wie wir alle zu Content-Erstellern geworden sind, ob wir es merken oder nicht.'],
                'spanish': ['El panorama de las redes sociales se ha convertido en un campo minado de preocupaciones de privacidad y manipulación psicológica.', 'Me fascina cómo todos nos hemos convertido en creadores de contenido, nos demos cuenta o no.'],
                'portuguese': ['O panorama das redes sociais tornou-se um campo minado de preocupações de privacidade e manipulação psicológica.', 'Fascina-me como todos nos tornámos criadores de conteúdo, quer nos apercebamos ou não.']
            }),
            'required_vocabulary': json.dumps(['algorithm', 'privacy', 'influencer', 'engagement', 'viral', 'echo chamber', 'digital footprint', 'authenticity']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Platform evolution → Privacy concerns → Influencer culture → Psychological impact → Future of social media'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Analyze social media critically using technical and sociological concepts.',
            'scenario_template': "You're discussing the dark side of social media with a tech journalist who covers digital culture."
        },

        # Topic 14: Expressing Opinions
        {
            'level': 'B2',
            'topic_number': 14,
            'title_key': 'expressing_opinions_b2',
            'subtopics': json.dumps(['media_influence', 'environmental_issues', 'parenting_philosophies', 'cultural_criticism']),
            'conversation_contexts': json.dumps(['Intellectual debate', 'Opinion piece discussion', 'Cultural commentary']),
            'llm_prompt_template': """You are engaging in sophisticated opinion exchange at B2 level.
Express nuanced opinions on complex topics with supporting arguments and counterarguments.
Use opinion structures: 'While I concede that...nevertheless...', 'One could argue that...however...'.
Support with evidence: 'Recent studies indicate...', 'Historical precedent shows...'.
Express nuance: 'It's not black and white...', 'There are shades of gray here...'.
Include cultural criticism: 'Our society's obsession with...', 'The commodification of...'.
Use rhetorical devices: 'Isn't it ironic that...', 'One might ask...'.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["The media's influence on public opinion is more subtle and insidious than most people realize.", "I've been grappling with the ethics of modern parenting in our hyper-connected world."],
                'german': ['Der Einfluss der Medien auf die öffentliche Meinung ist subtiler und heimtückischer, als die meisten Menschen erkennen.', 'Ich kämpfe mit der Ethik der modernen Erziehung in unserer hypervernetzten Welt.'],
                'spanish': ['La influencia de los medios en la opinión pública es más sutil e insidiosa de lo que la mayoría de la gente se da cuenta.', 'He estado luchando con la ética de la crianza moderna en nuestro mundo hiperconectado.'],
                'portuguese': ['A influência dos media na opinião pública é mais subtil e insidiosa do que a maioria das pessoas percebe.', 'Tenho lutado com a ética da parentalidade moderna no nosso mundo hiperconectado.']
            }),
            'required_vocabulary': json.dumps(['perspective', 'nuanced', 'controversial', 'ethics', 'paradigm', 'discourse', 'ideology', 'critical thinking']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Present controversial topic → Argue position → Consider counterarguments → Find middle ground → Broader implications'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Express sophisticated opinions with nuance. Use evidence and acknowledge complexity.',
            'scenario_template': "You're participating in a salon-style discussion about contemporary social and environmental issues."
        },

        # Topic 15: Common Idioms
        {
            'level': 'B2',
            'topic_number': 15,
            'title_key': 'common_idioms',
            'subtopics': json.dumps(['idiomatic_expressions', 'cultural_sayings', 'metaphorical_language', 'cross_cultural_idioms']),
            'conversation_contexts': json.dumps(['Language exchange', 'Cultural comparison', 'Idiom explanation']),
            'llm_prompt_template': """You are discussing language and idioms at B2 level.
Use idioms naturally and discuss their cultural significance and origins.
Include business idioms: 'cut to the chase', 'ballpark figure', 'touch base', 'circle back'.
Use cultural idioms: 'When in Rome...', 'The grass is always greener...', 'Don't count your chickens...'.
Explain idioms: 'What we mean by that is...', 'The origin of this expression...'.
Compare across cultures: 'Interestingly, in German they say...', 'The French equivalent would be...'.
Create wordplay: 'No pun intended', 'Pardon the expression', 'If you'll forgive the metaphor'.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["They say you can't teach an old dog new tricks, but I'm living proof that's not true.", "I love how idioms reveal cultural values. They're like windows into a society's soul."],
                'german': ['Man sagt, man kann einem alten Hund keine neuen Tricks beibringen, aber ich bin der lebende Beweis, dass das nicht stimmt.', 'Ich liebe es, wie Redewendungen kulturelle Werte offenbaren. Sie sind wie Fenster in die Seele einer Gesellschaft.'],
                'spanish': ['Dicen que perro viejo no aprende trucos nuevos, pero soy la prueba viviente de que eso no es cierto.', 'Me encanta cómo los modismos revelan valores culturales. Son como ventanas al alma de una sociedad.'],
                'portuguese': ['Dizem que cão velho não aprende truques novos, mas eu sou a prova viva de que isso não é verdade.', 'Adoro como os idiomas revelam valores culturais. São como janelas para a alma de uma sociedade.']
            }),
            'required_vocabulary': json.dumps(['idiom', 'expression', 'metaphor', 'literally', 'figuratively', 'proverb', 'saying', 'colloquialism']),
            'conversation_flow': json.dumps({
                'exchanges': 5,
                'structure': 'Use idiom naturally → Explain meaning → Discuss origin → Compare cultures → Create new contexts'
            }),
            'number_of_exchanges': 5,
            'topic_specific_rules': 'Use idioms extensively and naturally. Discuss their cultural significance.',
            'scenario_template': "You're at a language exchange discussing how idioms reflect cultural values and worldviews."
        },

        # Topic 16: FINAL TEST
        {
            'level': 'B2',
            'topic_number': 16,
            'title_key': 'test_final',
            'subtopics': json.dumps(['digital_culture', 'complex_opinions', 'language_mastery']),
            'conversation_contexts': json.dumps(['International Think Tank Discussion']),
            'llm_prompt_template': """You are at an international think tank discussing global issues at B2 level.
You will analyze digital culture's impact, express sophisticated opinions on global challenges, and demonstrate language mastery through idioms and cultural references.
Start by discussing how technology shapes society. Then debate environmental and social challenges. Finally, use idioms to make cultural observations.
Employ all B2 features: complex grammar, nuanced vocabulary, idioms, cultural awareness.
Include hypothetical scenarios, philosophical observations, and rhetorical devices.
This is your final demonstration of B2 mastery.""",
            'word_limit': 70,
            'opening_phrases': json.dumps({
                'english': ["We're at an inflection point in human history. The decisions we make now will echo for generations."],
                'german': ['Wir befinden uns an einem Wendepunkt in der Menschheitsgeschichte. Die Entscheidungen, die wir jetzt treffen, werden für Generationen nachhallen.'],
                'spanish': ['Estamos en un punto de inflexión en la historia humana. Las decisiones que tomemos ahora resonarán por generaciones.'],
                'portuguese': ['Estamos num ponto de inflexão na história humana. As decisões que tomamos agora ecoarão por gerações.']
            }),
            'required_vocabulary': json.dumps([]),
            'conversation_flow': json.dumps({
                'exchanges': 10,
                'structure': 'Integrated test covering digital culture, sophisticated opinions, and language mastery'
            }),
            'number_of_exchanges': 10,
            'topic_specific_rules': 'FINAL TEST: Demonstrate complete B2 mastery including idioms, nuanced opinions, and cultural sophistication.',
            'scenario_template': 'International Think Tank Discussion - Testing topics 13-15'
        }
    ]

    with app.app_context():
        print("Creating B2 topics...")
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
        print(f"\nSuccessfully created {topics_created} B2 topics!")

        # Verify the count
        b2_count = TopicDefinition.query.filter_by(level='B2').count()
        print(f"Total B2 topics in database: {b2_count}")

if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION: Populate B2 Topics (16 total)")
    print("=" * 60)
    create_b2_topics()
    print("\nB2 level is now ready with all 16 topics!")