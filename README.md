# Spralingua - AI-Powered Language Learning Platform

🌐 **[Try Live Demo](https://spralingua.com)** | [![Live Status](https://img.shields.io/badge/status-live-brightgreen)](https://spralingua.com)

![Python](https://img.shields.io/badge/python-3.11+-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)
![PostgreSQL](https://img.shields.io/badge/postgresql-15-blue)
![Claude AI](https://img.shields.io/badge/AI-Claude-purple)
![Deployment](https://img.shields.io/badge/deployment-Railway-blueviolet)

A Flask-based language learning platform that uses AI to provide personalized conversation practice and writing exercises. Built with Anthropic's Claude API for intelligent feedback and Minimax for text-to-speech capabilities.

## Features

### Core Learning Tools
- **Casual Conversation Practice** - Chat with AI characters (Harry & Sally) who adapt to your level
- **Email Writing Exercises** - Practice formal writing with culturally-appropriate scenarios
- **Real-time Language Feedback** - Get instant corrections and suggestions as you learn
- **Voice Input/Output** - Practice speaking and listening with speech recognition and TTS
- **Progress Tracking** - Track your advancement through CEFR levels (A1-B2)

### Language Support
- **Learning Languages**: Spanish, German, Portuguese, English
- **Interface Languages**: Full UI translation in all supported languages
- **Personalization**: Characters address you by name for a more engaging experience

### Smart Features
- **Adaptive Difficulty** - Content adjusts to your current CEFR level
- **Topic-Based Learning** - 12 structured topics per level with specific vocabulary
- **Dual Feedback System** - Quick hints during practice, detailed analysis after
- **Cultural Adaptation** - Letters and conversations reflect authentic cultural contexts

## Tech Stack

### Backend
- **Flask** - Web framework
- **PostgreSQL** - Database for user progress and content
- **SQLAlchemy** - ORM for database operations
- **Anthropic Claude API** - AI conversation and feedback generation
- **Minimax API** - Text-to-speech synthesis

### Frontend
- **Vanilla JavaScript** - No framework dependencies
- **Web Speech API** - Browser-based speech recognition
- **Lottie** - Animated character avatars
- **CSS3** - Modern responsive design with glass morphism effects

## Prerequisites

- Python 3.11+
- PostgreSQL 17
- UV package manager
- Anthropic API key
- Minimax API credentials (optional, for TTS)

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/LouisZCode/spralingua.git
cd spralingua
```

2. **Set up PostgreSQL database**
```sql
CREATE DATABASE spralingua_dev;
CREATE USER dev WITH PASSWORD 'devpass';
GRANT ALL PRIVILEGES ON DATABASE spralingua_dev TO dev;
```

3. **Configure environment variables**
Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your_anthropic_api_key
MINIMAX_API_KEY=your_minimax_api_key
MINIMAX_GROUP_ID=your_minimax_group_id
MINIMAX_VOICE_ID=your_default_voice_id
```

4. **Install dependencies with UV**
```bash
# Install UV if you haven't already
pip install uv

# Install project dependencies
uv sync
```

5. **Run database migrations**
```bash
uv run python migrations/create_user_progress_table.py
uv run python migrations/create_topic_system_tables.py
uv run python migrations/populate_a1_topics.py
uv run python migrations/populate_exercise_types.py
uv run python migrations/01_create_level_rules_table.py
uv run python migrations/02_enhance_topic_definitions.py
uv run python migrations/03_update_topic1_flow.py
uv run python migrations/04_add_scenario_templates.py
uv run python migrations/05_update_topic1_to_5_exchanges.py
uv run python migrations/06_add_exercise_progress.py
uv run python migrations/07_add_completion_popup_tracking.py
```

6. **Start the application**
```bash
uv run python app.py
```

The application will be available at `http://localhost:5001`

## Project Structure

```
spralingua/
├── auth/                   # Authentication system
├── email_writing/          # Email writing exercise module
├── language/               # Language mapping utilities
├── level_rules/            # CEFR level rules and guidelines
├── migrations/             # Database migration scripts
├── models/                 # SQLAlchemy database models
├── progress/               # Progress tracking system
├── prompts/                # AI prompt templates and personalities
├── scenarios/              # Dynamic scenario generation
├── static/                 # CSS, JavaScript, and assets
│   ├── css/                # Stylesheets
│   ├── js/                 # Frontend JavaScript
│   └── animations/         # Lottie animation files
├── templates/              # Jinja2 HTML templates
├── tests/                  # Test management system
├── topics/                 # Topic progression management
├── app.py                  # Main Flask application
├── claude_client.py        # Anthropic API integration
├── minimax_client.py       # Minimax TTS integration
└── database.py             # Database configuration
```

## Development Guidelines

### Windows Compatibility
**CRITICAL**: Never use emoji characters in console output due to Windows encoding limitations. Use text markers instead:
- ✅ → [SUCCESS]
- ❌ → [ERROR]
- ⚠️ → [WARNING]

Emojis ARE allowed in HTML templates for user-facing UI.

### Database Models
All SQLAlchemy models must be imported in `app.py` after database initialization to establish proper relationships.

### CSS Architecture
- Two-layer system: `base.css` (global utilities) + component-specific styles
- Use CSS custom properties for consistent theming
- Purple gradient branding: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`

### Package Management
Always use UV for package management:
```bash
uv add package_name     # Add new dependency
uv sync                 # Install all dependencies
uv run python script.py # Run Python scripts
```

## API Endpoints

### Progress Management
- `POST /api/save-progress` - Save language/level selection
- `GET /api/user-progress` - Get user progress with exercise completion

### Casual Chat
- `POST /api/casual-chat/chat` - Submit message and receive AI response
- `POST /api/casual-chat/tts` - Generate text-to-speech audio
- `POST /api/casual-chat/clear` - Clear conversation history
- `GET /api/casual-chat/scenario` - Get conversation scenario

### Email Writing
- `GET /writing-practice` - Email writing exercise page
- `POST /api/writing-practice/generate` - Generate culturally-adapted letters
- `POST /api/writing-practice/submit` - Submit and evaluate responses

## Features in Development

- Fill the Blanks exercise
- Correct Kevin exercise (error correction practice)
- A2, B1, B2 topic content
- Progress analytics dashboard
- Achievement system
- Additional conversation characters

## Contributing

1. Follow the component-first development approach
2. Maintain Windows compatibility (no console emojis)
3. Use the established CSS design system
4. Test each component independently before integration
5. Follow the existing OOP architecture patterns

6. ## Why I Built This

7. After spending 4+ years as a Talent Partner recruiting for tech companies across the DACH region, I saw firsthand how language barriers limit career opportunities. Many talented professionals struggled to break into international markets simply because they lacked conversational confidence in German or English.

8. Traditional language learning apps focus on gamification and vocabulary drills, but what people actually need is **real conversation practice with immediate, intelligent feedback**. That's where AI shines—you can practice speaking without fear of judgment, get instant corrections, and have conversations that adapt to your actual skill level.

9. Spralingua combines my understanding of what learners need (from recruiting internationally) with modern AI capabilities to create a tool that solves a real problem: helping people gain the language confidence they need to access better career opportunities.

10. ## Technical Challenges Solved

11. ### Multi-Agent Conversation Architecture
12. Built a sophisticated agent orchestration system using **LangGraph** where multiple AI personalities (Harry & Sally) maintain consistent character traits while adapting their language complexity to the user's CEFR level (A1-C2). Each agent has memory of past conversations and adjusts responses based on user progress.

13. ### Sub-Second Response Times
14. Achieved <2s response times for AI-generated feedback by implementing efficient prompt engineering, strategic caching, and optimized Claude API calls. This creates a natural conversation flow rather than the frustrating delays common in AI chat applications.

15. ### Privacy-First Voice AI
16. Integrated real-time voice input/output using Web Speech API and Minimax TTS, allowing users to practice pronunciation. Voice processing happens client-side where possible, minimizing data transmission and protecting user privacy.

17. ### Database-Driven Prompt System
18. Designed a flexible prompt management system stored in PostgreSQL that allows dynamic adjustment of difficulty levels, grammar rules, and cultural context without code changes. This makes it easy to add new languages and customize learning paths.

19. ### Production-Ready Deployment
20. Successfully deployed on Railway with Gunicorn, PostgreSQL, and proper environment configuration. Handles concurrent users with stateful conversation management across multiple workers.

## License

[License information to be added]

## Support

For issues and feature requests, please use the [GitHub Issues](https://github.com/LouisZCode/spralingua/issues) page.

## Acknowledgments

Built as a simplified version of GTA-V2, focusing on core language learning features with clean, maintainable architecture.
