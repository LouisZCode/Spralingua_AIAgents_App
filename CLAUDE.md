# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spralingua is a simplified version of GTA-V2, a Flask-based AI-powered language learning platform. This project follows a component-by-component development approach where each part is completed and tested independently before moving to the next.

## Development Philosophy

- **OOP Approach**: Each component is developed as an independent module
- **Component-First**: Finish and test each component completely before moving to the next
- **No Rewrites**: Once a component works, we don't change it unless absolutely necessary
- **Copy & Paste Strategy**: Use commands to copy files from GTA-V2 rather than rewriting

## Development Setup

**IMPORTANT**: This project uses UV for ALL package management and environment operations. Always use UV commands instead of pip/python directly.

```bash
# Install dependencies
uv sync

# Run the development server  
uv run python app.py

# Add new packages
uv add package_name

# Run any Python script
uv run python script.py
```

## Architecture

- **Flask Application**: Simple Flask app structure
- **Template Inheritance**: Uses Jinja2 templates with base.html
- **Static Assets**: CSS and JS files in /static directory
- **Component Structure**: Each major feature as an independent module

## Common Commands

### Development
```bash
# Run development server
uv run python app.py

# Add new dependency
uv add package_name

# Copy files from GTA-V2 (adjust paths as needed)
cp "path/to/GTA-V2/file" "local/destination"
```

### File Operations
- Use `cp` commands to copy files from GTA-V2 project
- Use `mkdir -p` to create directory structures
- Always copy and adapt rather than rewrite from scratch