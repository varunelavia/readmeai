# README.ai - AI-Powered README Generator

A powerful command-line tool that automatically generates comprehensive README.md files for your projects using leading AI services (OpenAI, Anthropic, Google Gemini).

## Table of Contents

- [Features](#features)
- [Tech Stack/Requirements](#tech-stackrequirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands](#commands)
- [API Reference](#api-reference)
- [File Filtering](#file-filtering)
- [Docker Support](#docker-support)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- 🤖 **Multi-AI Support**: Generate READMEs using OpenAI (GPT-3.5/GPT-4), Anthropic (Claude), or Google Gemini
- 📁 **Smart File Analysis**: Automatically scans your codebase while intelligently filtering out irrelevant files
- 🔧 **Highly Configurable**: Customize file filtering, API settings, and generation parameters
- 🔄 **Retry Mechanism**: Built-in retry logic for API reliability
- 🐳 **Docker Support**: Run in a containerized environment
- 💾 **Configuration Management**: Save and reuse API keys and default settings
- 📋 **Model Discovery**: List available models for each AI service
- 🛡️ **Security First**: API key validation and secure storage options

## Tech Stack/Requirements

- **Python**: 3.10 or higher
- **Dependencies**:
  - `google-generativeai==0.8.5` - Google Gemini API client
  - `anthropic==0.52.1` - Anthropic Claude API client
  - `openai==1.82.1` - OpenAI GPT API client
- **API Keys**: Required for at least one of the supported AI services

## Installation

### Using pip

1. Clone the repository:
```bash
git clone https://github.com/varunelavia/readmeai.git
cd readmeai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the script executable (optional):
```bash
chmod +x readmeai.py
```

### Using Docker

Build the Docker image:
```bash
docker build -t readmeai .
```

## Configuration

### Initial Setup

Configure your preferred API and model:
```bash
./readmeai.py configure --api-key YOUR_API_KEY --default-api openai --default-model gpt-4
```

### API Key Management

API keys can be provided in three ways (in order of priority):

1. **Command-line argument**: `--api-key YOUR_API_KEY`
2. **Environment variable**: `export API_KEY='YOUR_API_KEY'`
3. **Configuration file**: Saved via the `configure` command

Configuration is stored in `~/.readmeai/config.json`.

## Usage

### Basic Usage

Generate a README for your project:
```bash
./readmeai.py generate /path/to/your/project
```

### Advanced Usage

```bash
# Use a specific AI service and model
./readmeai.py generate ./my-project --api gemini --ai-model gemini-pro

# Add custom context
./readmeai.py generate ./my-project --additional-context "This is a machine learning project focused on NLP"

# Ignore specific directories and files
./readmeai.py generate ./my-project --dirs-to-ignore "tests,docs" --files-to-ignore "config.json,secrets.env"

# Only process specific file types
./readmeai.py generate ./my-project --extensions-to-allow "py,js,ts"

# Custom output filename
./readmeai.py generate ./my-project --readme-filename "PROJECT_README.md"
```

### Using Docker

```bash
# Basic usage
docker run -v /path/to/your/project:/app/project -e API_KEY=YOUR_API_KEY readmeai generate /app/project

# With additional options
docker run -v /path/to/your/project:/app/project -e API_KEY=YOUR_API_KEY readmeai generate /app/project --api openai --ai-model gpt-4
```

## Commands

### `generate` - Generate README

Main command to analyze a codebase and generate a README.

**Arguments:**
- `path`: Path to the directory to analyze (required)
- `--dirs-to-ignore`: Comma-separated list of directories to skip
- `--files-to-ignore`: Comma-separated list of files to skip
- `--extensions-to-ignore`: File extensions to skip (without dots)
- `--extensions-to-allow`: Only process files with these extensions
- `--additional-context`: Extra context about the project
- `--readme-filename`: Output filename (default: README.md)
- `--api`: AI service to use (gemini/anthropic/openai)
- `--ai-model`: Specific model to use
- `--api-key`: API key for the service
- `--max-retries`: Maximum API retry attempts (default: 3)
- `--retry-delay`: Delay between retries in seconds (default: 2)
- `--max-tokens`: Maximum tokens to generate (default: 2048)
- `--debug`: Enable debug logging

### `configure` - Set Default Settings

Save API keys and default preferences.

**Arguments:**
- `--api-key`: Set the API key
- `--default-api`: Set default AI service
- `--default-model`: Set default model

### `list-models` - List Available Models

Display available models for each AI service.

**Arguments:**
- `--api`: Specific API to query
- `--api-key`: API key (optional if configured)

## API Reference

### Supported AI Services

1. **OpenAI**
   - Models: GPT-3.5-turbo, GPT-4, GPT-4-turbo
   - [Get API Key](https://platform.openai.com/api-keys)

2. **Anthropic**
   - Models: Claude-3-opus, Claude-3-sonnet, Claude-3-haiku
   - [Get API Key](https://console.anthropic.com/api-keys)

3. **Google Gemini**
   - Models: Gemini-pro, Gemini-pro-vision
   - [Get API Key](https://makersuite.google.com/app/apikey)

## File Filtering

### Default Ignored Directories
- `.git`, `node_modules`, `venv`, `__pycache__`, `.pytest_cache`, `dist`, `build`

### Default Ignored Files
- System files: `.DS_Store`, `Thumbs.db`, `.env*`
- Package locks: `package-lock.json`, `yarn.lock`, `poetry.lock`
- Compiled files: `*.pyc`, `*.exe`, `*.dll`
- Media files: `*.jpg`, `*.png`, `*.mp4`, `*.pdf`
- Documentation: `*.md`, `LICENSE*`, `CHANGELOG*`

### Custom Filtering

You can override defaults or add custom patterns:
```bash
# Ignore additional directories
--dirs-to-ignore "custom_dir,another_dir"

# Ignore specific files
--files-to-ignore "custom.file,another.file"

# Only process Python and JavaScript files
--extensions-to-allow "py,js"
```

## Docker Support

The project includes a multi-stage Dockerfile for efficient containerization:

- **Base image**: Python 3.10-slim
- **Security**: Runs as non-root user
- **Optimization**: Virtual environment with minimal dependencies

### Building and Running

```bash
# Build
docker build -t readmeai .

# Run with mounted volume
docker run -v $(pwd):/app/project -e API_KEY=YOUR_KEY readmeai generate /app/project
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the existing style and includes appropriate tests.

## License

This project is open source. Please add a LICENSE file to specify the license terms.

## Acknowledgements

- Built with support from OpenAI, Anthropic, and Google AI