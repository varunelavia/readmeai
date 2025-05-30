# README.ai - AI-Powered README Generator

A powerful command-line tool that automatically generates comprehensive README.md files for your projects using leading AI services (OpenAI, Anthropic, Google Gemini).

## Table of Contents

- [Features](#features)
- [Tech Stack/Requirements](#tech-stackrequirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Examples](#examples)
- [Commands](#commands)
- [CLI Reference](#commands)
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

### Quick Installation (Linux/macOS)

Run these commands to install README.ai system-wide:

```bash
wget https://raw.githubusercontent.com/varunelavia/readmeai/v1.0.0/readmeai.py
chmod +x readmeai.py
sudo mv readmeai.py /usr/local/bin/readmeai
pip install google-generativeai==0.8.5 anthropic==0.52.1 openai==1.82.1
readmeai --version
```

Now you can run `readmeai` from anywhere in your terminal!

### Get API Keys

To use README.ai, you'll need an API key from one of the supported providers:

- **OpenAI**: [Get API Key](https://platform.openai.com/api-keys)
- **Anthropic**: [Get API Key](https://console.anthropic.com/settings/keys)
- **Google Gemini**: [Get API Key](https://aistudio.google.com/app/apikey)

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

For detailed examples of all available commands and options, see [EXAMPLES.md](EXAMPLES.md).

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

For detailed information about all available commands and options, see the [CLI Reference](CLI-REFERENCE.md).

### `generate` - Generate README

Main command to analyze a codebase and generate a README.

**Arguments:**
- `path`: Path to the directory to analyze (required)
  - Must be a valid directory path
  - Directory must exist and be accessible
- `--dirs-to-ignore`: Comma-separated list of directories to skip
  - Must be a valid comma-separated list
  - Empty lists are not allowed
- `--files-to-ignore`: Comma-separated list of files to skip
  - Must be a valid comma-separated list
  - Empty lists are not allowed
- `--extensions-to-ignore`: File extensions to skip (without dots)
  - Must be a valid comma-separated list
  - Empty lists are not allowed
- `--extensions-to-allow`: Only process files with these extensions
  - Must be a valid comma-separated list
  - Empty lists are not allowed
- `--additional-context`: Extra context about the project
- `--readme-filename`: Output filename (default: README.md)
- `--skip-readme-backup`: Skip backing up existing README file if it exists
- `--api`: AI service to use (gemini/anthropic/openai)
  - Must be one of the supported APIs
- `--ai-model`: Specific model to use
  - Must be a valid model for the chosen API
  - Use `list-models` to see available models
- `--api-key`: API key for the service
  - Must be a valid API key for the chosen service
- `--max-retries`: Maximum API retry attempts (default: 3)
  - Must be between 1 and 10
- `--retry-delay`: Delay between retries in seconds (default: 2)
  - Must be between 1 and 30
- `--max-tokens`: Maximum tokens to generate (default: 2048)
  - Must be between 100 and 4096
- `--debug`: Enable debug logging

### `configure` - Set Default Settings

Save API keys and default preferences.

**Arguments:**
- `--api-key`: Set the API key
  - Must be a valid API key for the chosen service
- `--default-api`: Set default AI service
  - Must be one of the supported APIs (gemini/anthropic/openai)
- `--default-model`: Set default model
  - Must be a valid model for the chosen API
  - Use `list-models` to see available models

### `configure-show` - Display Current Configuration

Show current configuration settings without exposing the API key.

```bash
readmeai configure-show
```

### `configure-reset` - Reset Configuration

Delete the configuration file and start fresh.

```bash
readmeai configure-reset
```

### `list-models` - List Available Models

Display available models for each AI service.

**Arguments:**
- `--api`: Specific API to query
  - Must be one of the supported APIs (gemini/anthropic/openai)
- `--api-key`: API key (optional if configured)
  - Must be a valid API key for the chosen service

## Input Validation

The tool performs comprehensive validation of all inputs:

1. **Path Validation**
   - Ensures the target directory exists
   - Verifies the path is a directory, not a file
   - Checks for proper permissions

2. **List Validation**
   - Validates comma-separated lists for directories, files, and extensions
   - Ensures lists are properly formatted
   - Prevents empty lists

3. **API and Model Validation**
   - Verifies API selection is supported
   - Validates model names against available models
   - Checks API key format and validity

4. **Numeric Parameter Validation**
   - Enforces reasonable ranges for retries, delays, and token limits
   - Prevents invalid numeric inputs
   - Provides clear error messages for out-of-range values

5. **Configuration Validation**
   - Validates API keys before saving
   - Ensures model compatibility with chosen API
   - Maintains configuration file integrity

All validation errors are reported with clear, descriptive messages to help users correct their inputs.

## API Reference

### Supported AI Services

**1. OpenAI**

* **Dashboard Login:** [https://platform.openai.com/login/](https://platform.openai.com/login/)
* **Get API Key:** [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
* **Official Documentation:** [https://platform.openai.com/docs](https://platform.openai.com/docs)
* **Pricing Page:** [https://openai.com/pricing](https://openai.com/pricing)
* **Rate Limits & Quotas:** [https://platform.openai.com/docs/guides/rate-limits](https://platform.openai.com/docs/guides/rate-limits)
* **Usage Dashboard:** [https://platform.openai.com/usage](https://platform.openai.com/usage)

**2. Anthropic (Claude)**

* **Console Login:** [https://console.anthropic.com/](https://console.anthropic.com/)
* **Get API Key:** [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
* **Official Documentation:** [https://docs.anthropic.com/claude/reference/getting-started-with-the-api](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
* **Pricing Page:** [https://www.anthropic.com/pricing](https://www.anthropic.com/pricing) (and often detailed within the console after login)
* **Limits and Quotas:** Typically found within the console or developer documentation after account setup. A general guide can be found at [https://docs.anthropic.com/claude/reference/rate-limits](https://docs.anthropic.com/claude/reference/rate-limits).

**3. Google Gemini**

* **Official Documentation (Gemini API):** [https://ai.google.dev/docs](https://ai.google.dev/docs)
* **Get API Key:** [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
* **Google AI Studio (for API Keys):** [https://aistudio.google.com/](https://aistudio.google.com/)
* **Gemini API Pricing:** [https://ai.google.dev/pricing](https://ai.google.dev/pricing)
* **Gemini API Quotas and Limits:** [https://ai.google.dev/gemini-api/docs/rate-limits](https://ai.google.dev/gemini-api/docs/rate-limits)
* **Google Cloud Free Tier & Always Free Limits (includes some Generative AI):** [https://cloud.google.com/free/docs/free-cloud-features#generative-ai](https://cloud.google.com/free/docs/free-cloud-features#generative-ai)
* **Manage Billing for GCP Projects:** [https://cloud.google.com/billing/docs/how-to/modify-project](https://cloud.google.com/billing/docs/how-to/modify-project)

### Recommended AI Provider: Google Gemini

We recommend using Google Gemini for the following reasons:

* **Large Context Size**: Gemini models can handle significantly larger context windows, allowing for more comprehensive analysis of your codebase.
* **Higher Token Limits**: Supports larger token counts, enabling more detailed README generation without truncation.
* **Competitive Pricing**: Offers a generous free tier and competitive pricing for paid usage.
* **Reliable Performance**: Consistently delivers high-quality results with good response times.

To get started with Gemini:
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create an account or sign in
3. Generate an API key
4. Use the key with README.ai: `readmeai generate --api gemini --ai-model models/gemini-1.5-flash /path/to/project`

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

### Quick Start with Docker

1. **Pull the Image:**
    ```bash
    docker pull readmeai/readmeai:latest 
    # Or specify a version, e.g., readmeai/readmeai:v1.0.0
    ```

2. **Basic Generation (using Environment Variable for API Key):**
    This example uses Gemini. Replace `--api gemini` and the `API_KEY` with your chosen provider and key.

    ```bash
    docker run --rm \
      --user "$(id -u):$(id -g)" \
      -v "/path/to/your/project:/app/project" \
      -e API_KEY="YOUR_CHOSEN_PROVIDER_API_KEY" \
      readmeai/readmeai \
      generate \
      --api gemini \
      --ai-model "gemini-1.5-flash" \
      "/app/project"
    ```

    **Explanation of common Docker flags:**
    * `--rm`: Automatically removes the container when it exits.
    * `--user "$(id -u):$(id -g)"`: Runs the container process with your host user's ID and group ID. Crucial to avoid permission errors when writing the README to your mounted volume.
    * `-v "/path/to/your/project:/app/project"`: Mounts your local project directory to `/app/project` inside the container. The generated README is saved here.
    * `-e API_KEY="YOUR_..."`: Sets the generic `API_KEY` environment variable. The tool uses this key for the provider specified by the `--api` flag.

### Advanced Docker Usage

#### 1. Persistent Configuration

The `readmeai configure` command saves to `~/.readmeai/config.json` inside the container. To make it persistent:

1. Create a directory on your host to store the configuration:
    ```bash
    mkdir -p "$HOME/.config/readmeai_docker_config"
    ```

2. Mount this directory when running readmeai configure:
    ```bash
    docker run --rm -it \
      --user "$(id -u):$(id -g)" \
      -v "$HOME/.config/readmeai_docker_config:/home/readmeai_user/.readmeai" \
      readmeai/readmeai \
      configure --default-api gemini --api-key "YOUR_GEMINI_KEY"
    ```

> **Note:** Correctly mapping `~` for dynamic UIDs in Docker can be tricky. Test the target path (`/root/.readmeai` or a path corresponding to the dynamic user's potential home) for your specific base image.

#### 2. Using Different AI Providers

```bash
# Using OpenAI
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "/path/to/your/project:/app/project" \
  -e API_KEY="YOUR_OPENAI_KEY" \
  readmeai/readmeai \
  generate \
  --api openai \
  --ai-model "gpt-4" \
  "/app/project"

# Using Anthropic
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "/path/to/your/project:/app/project" \
  -e API_KEY="YOUR_ANTHROPIC_KEY" \
  readmeai/readmeai \
  generate \
  --api anthropic \
  --ai-model "claude-3-opus-20240229" \
  "/app/project"
```

#### 3. Advanced Options

```bash
# With file filtering
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "/path/to/your/project:/app/project" \
  -e API_KEY="YOUR_API_KEY" \
  readmeai/readmeai \
  generate \
  --api openai \
  --ai-model "gpt-4" \
  --extensions-to-allow "py,js" \
  --dirs-to-ignore "node_modules,venv" \
  --files-to-ignore "package-lock.json,.env" \
  --additional-context "This is a machine learning project" \
  "/app/project"

# With custom output filename
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "/path/to/your/project:/app/project" \
  -e API_KEY="YOUR_API_KEY" \
  readmeai/readmeai \
  generate \
  --api openai \
  --ai-model "gpt-4" \
  --readme-filename "PROJECT_README.md" \
  "/app/project"
```

#### 4. Listing Available Models

```bash
docker run --rm \
  -e API_KEY="YOUR_PROVIDER_API_KEY" \
  readmeai/readmeai \
  list-models --api <gemini|openai|anthropic>
```

### Building from Source

If you prefer to build the Docker image yourself:

```bash
# Clone the repository
git clone https://github.com/varunelavia/readmeai.git
cd readmeai

# Build the image
docker build -t readmeai .

# Run using the local image
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "/path/to/your/project:/app/project" \
  -e API_KEY="YOUR_API_KEY" \
  readmeai \
  generate \
  --api openai \
  --ai-model "gpt-4" \
  "/app/project"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Built with support from OpenAI, Anthropic, and Google AI