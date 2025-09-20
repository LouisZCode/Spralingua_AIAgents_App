# LEARNINGS.md - Lessons from Spralingua Development

This document captures important technical lessons learned during the development of Spralingua that will be valuable for future projects.

## 1. Git & GitHub on Windows - Binary File Issue

### The Problem
When working with Git on Windows, text files (especially README.md) may appear empty on GitHub despite having content locally. Git treats them as binary files instead of text.

### Symptoms
- GitHub shows empty file content but file size is correct
- Git commits show `0 insertions, 0 deletions` for text files
- Git log shows files as `Bin 0 -> XXXX bytes`
- Commit messages have warnings about CRLF line endings

### Root Cause
Windows uses CRLF (`\r\n`) line endings while Unix/GitHub expects LF (`\n`). When Git detects mixed or unusual line endings, it may treat the file as binary.

### The Fix
Create a `.gitattributes` file in your project root:

```gitattributes
# Handle line endings automatically
* text=auto

# Force LF line endings for code files
*.md text eol=lf
*.py text eol=lf
*.js text eol=lf
*.css text eol=lf
*.html text eol=lf
*.json text eol=lf
*.yaml text eol=lf

# Mark binary files
*.png binary
*.jpg binary
*.pdf binary
```

### Prevention for Future Projects
1. **Always create `.gitattributes` file at project start** - Don't wait until you have issues
2. **Use UTF-8 encoding** for all text files
3. **Check file status** with `git diff --cached filename` if suspicious
4. **Configure Git globally** (optional): `git config --global core.autocrlf true`

### Key Learning
**Start every Windows project with a proper `.gitattributes` file to avoid encoding headaches later.**

---

## 2. LLM API Context Bleeding

### The Problem
When making rapid sequential calls to the same LLM API client instance (like Claude), responses from one call can "bleed" into another, causing wrong content to appear in the wrong part of the application.

### Real Example from Spralingua
- **Scenario**: Casual chat feature needed two API calls:
  1. Generate conversation response
  2. Generate language learning hint
- **Issue**: Hint JSON data would sometimes appear as the conversation response
- **Impact**: Users would see JSON code instead of natural conversation

### The Quick Fix (Applied)
Added a 0.5 second delay between API calls:
```python
# After conversation response
time.sleep(0.5)
# Then make hint generation call
```

### The Robust Fix (Recommended for Future)
Use separate API client instances for different purposes:

```python
# Instead of one shared client
claude_client = ClaudeClient(api_key)

# Use dedicated clients for different purposes
conversation_client = ClaudeClient(api_key)
hint_client = ClaudeClient(api_key)
feedback_client = ClaudeClient(api_key)

# Or create new instances per request
def get_conversation_response():
    client = ClaudeClient(api_key)  # Fresh instance
    return client.generate(...)

def get_hint():
    client = ClaudeClient(api_key)  # Different instance
    return client.generate(...)
```

### Best Practices for LLM API Calls
1. **Separate Clients**: Use different client instances for different functional areas
2. **Fresh Instances**: Consider creating new client instances per request for complete isolation
3. **Clear Context**: If reusing clients, ensure context is cleared between calls
4. **Rate Limiting**: Implement proper rate limiting instead of sleep() for production
5. **Request IDs**: Use unique request IDs to track and debug context issues
6. **Async Operations**: Consider async/await patterns to better manage concurrent API calls

### Why This Happens
- LLM clients may maintain internal state or context
- Rapid calls can cause race conditions
- Token buffers might not be fully flushed between calls
- Session management in the client library may be stateful

### Key Learning
**Never assume LLM API clients are stateless. Use separate instances for different purposes or implement proper context isolation.**

---

## 3. Voice Input Browser Compatibility

### The Problem
Web Speech API behavior varies across browsers and requires careful configuration handling.

### Lessons Learned
1. **Language codes must be exact**: `de-DE`, not `de` or `german`
2. **Config must load before initialization**: Define `window.VOICE_INPUT_CONFIG` before loading voice-input.js
3. **Mobile Safari quirks**: Requires user interaction to start recording
4. **Chrome auto-stops**: Recording stops after 60 seconds of silence

### Best Practice
```javascript
// Always define config in window scope first
window.VOICE_INPUT_CONFIG = {
    language: 'es-ES',  // Exact locale code
    // ... other config
};
// Then load the voice input script
```

---

## 4. Database Migration Strategy

### The Problem
Complex interdependent database schemas need careful migration ordering.

### Lessons Learned
1. **Number your migrations**: Use prefixes like `01_`, `02_` for execution order
2. **Check before creating**: Always check if tables/columns exist before creating
3. **Import models after DB init**: SQLAlchemy needs all models imported for relationships
4. **Keep migrations idempotent**: Migrations should be safe to run multiple times

### Migration Template
```python
def check_table_exists(engine, table_name):
    query = text("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = :table_name
        );
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"table_name": table_name})
        return result.scalar()

# Always check before creating
if not check_table_exists(engine, 'my_table'):
    Base.metadata.create_all(engine)
    print("[SUCCESS] Table created")
else:
    print("[INFO] Table already exists")
```

---

## 5. Windows Console Encoding

### The Problem
Windows console cannot display Unicode emojis, causing crashes in Python applications.

### The Solution
- Never use emojis in console output
- Use text markers: `[SUCCESS]`, `[ERROR]`, `[INFO]`
- Emojis are safe in HTML templates (browser-rendered)

### Detection Pattern
```python
# This will crash on Windows console
print("✅ Success!")  # BAD

# This works everywhere
print("[SUCCESS] Operation completed")  # GOOD
```

---

## Future Project Checklist

Based on these learnings, here's a checklist for starting new projects:

### Project Setup
- [ ] Create `.gitattributes` file with proper line ending rules
- [ ] Set up UTF-8 encoding for all files
- [ ] Configure Git for Windows line endings if needed

### API Integration
- [ ] Design with separate API client instances for different features
- [ ] Implement request ID tracking for debugging
- [ ] Add proper error handling and retry logic
- [ ] Consider rate limiting from the start

### Database Design
- [ ] Number migration files for clear execution order
- [ ] Make migrations idempotent
- [ ] Test migration rollback procedures
- [ ] Document model import requirements

### Cross-Platform Compatibility
- [ ] Avoid Unicode in console output
- [ ] Test on Windows early and often
- [ ] Document browser requirements for web features
- [ ] Handle platform-specific path separators

### Configuration Management
- [ ] Define window-scoped configs before script loading
- [ ] Use exact locale codes for internationalization
- [ ] Separate development and production configurations
- [ ] Document all environment variables needed

---

## Contributing to This Document

When you encounter a significant technical challenge or discover an important pattern, add it here with:
1. **The Problem**: Clear description of what went wrong
2. **Real Example**: Specific case from the project
3. **The Fix**: What solution was applied
4. **Best Practice**: How to prevent or better handle it in the future
5. **Key Learning**: One-sentence takeaway

This document is meant to save time and prevent repeating mistakes in future projects.