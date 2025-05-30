# README.ai Examples

This document provides comprehensive examples for using README.ai with different AI providers and commands.

## Basic Usage Examples

### 1. Generate README with Different AI Providers

#### Using Google Gemini (Recommended)
```bash
# Basic usage with Gemini
readmeai generate /path/to/project --api gemini --ai-model gemini-pro

# With API key from environment variable
export API_KEY="your-gemini-api-key"
readmeai generate /path/to/project --api gemini --ai-model gemini-pro

# With service account authentication
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
readmeai generate /path/to/project --api gemini --ai-model gemini-pro

# Skip README backup
readmeai generate /path/to/project --api gemini --ai-model gemini-pro --skip-readme-backup
```

#### Using OpenAI
```bash
# Basic usage with OpenAI
readmeai generate /path/to/project --api openai --ai-model gpt-4

# With API key from environment variable
export API_KEY="your-openai-api-key"
readmeai generate /path/to/project --api openai --ai-model gpt-4

# With custom output filename
readmeai generate /path/to/project --api openai --ai-model gpt-4 --readme-filename "PROJECT_README.md"
```

#### Using Anthropic Claude
```bash
# Basic usage with Claude
readmeai generate /path/to/project --api anthropic --ai-model claude-3-opus-20240229

# With API key from environment variable
export API_KEY="your-anthropic-api-key"
readmeai generate /path/to/project --api anthropic --ai-model claude-3-opus-20240229
```

### 2. Advanced Generation Options

```bash
# Add custom context
readmeai generate /path/to/project \
  --api gemini \
  --ai-model gemini-pro \
  --additional-context "This is a machine learning project focused on NLP"

# Filter specific file types
readmeai generate /path/to/project \
  --api gemini \
  --ai-model gemini-pro \
  --extensions-to-allow "py,js,ts"

# Ignore specific directories and files
readmeai generate /path/to/project \
  --api gemini \
  --ai-model gemini-pro \
  --dirs-to-ignore "tests,docs,node_modules" \
  --files-to-ignore "config.json,secrets.env"

# Customize generation parameters
readmeai generate /path/to/project \
  --api gemini \
  --ai-model gemini-pro \
  --max-retries 5 \
  --retry-delay 3 \
  --max-tokens 4096
```

## Configuration Examples

### 1. Configure Default Settings

```bash
# Set default API and model
readmeai configure --default-api gemini --default-model gemini-pro

# Set API key
readmeai configure --api-key "your-api-key"

# Set both API key and defaults
readmeai configure \
  --default-api gemini \
  --default-model gemini-pro \
  --api-key "your-api-key"
```

### 2. View and Reset Configuration

```bash
# Show current configuration
readmeai configure-show

# Reset configuration
readmeai configure-reset
```

## Model Discovery Examples

```bash
# List available Gemini models
readmeai list-models --api gemini

# List available OpenAI models
readmeai list-models --api openai

# List available Anthropic models
readmeai list-models --api anthropic

# List models with API key
readmeai list-models --api gemini --api-key "your-api-key"
```

## Docker Usage Examples

### 1. Basic Docker Usage

```bash
# Using Gemini
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "/path/to/your/project:/app/project" \
  -e API_KEY="your-gemini-api-key" \
  readmeai/readmeai \
  generate \
  --api gemini \
  --ai-model gemini-pro \
  "/app/project"

# Using OpenAI
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "/path/to/your/project:/app/project" \
  -e API_KEY="your-openai-api-key" \
  readmeai/readmeai \
  generate \
  --api openai \
  --ai-model gpt-4 \
  "/app/project"
```

### 2. Docker with Advanced Options

```bash
# With file filtering
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "/path/to/your/project:/app/project" \
  -e API_KEY="your-api-key" \
  readmeai/readmeai \
  generate \
  --api gemini \
  --ai-model gemini-pro \
  --extensions-to-allow "py,js" \
  --dirs-to-ignore "node_modules,venv" \
  --files-to-ignore "package-lock.json,.env" \
  --additional-context "This is a machine learning project" \
  "/app/project"

# With persistent configuration
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "/path/to/your/project:/app/project" \
  -v "$HOME/.config/readmeai_docker_config:/home/readmeai_user/.readmeai" \
  -e API_KEY="your-api-key" \
  readmeai/readmeai \
  generate \
  --api gemini \
  --ai-model gemini-pro \
  "/app/project"
```

### 3. Docker Configuration Commands

```bash
# Configure defaults
docker run --rm -it \
  --user "$(id -u):$(id -g)" \
  -v "$HOME/.config/readmeai_docker_config:/home/readmeai_user/.readmeai" \
  readmeai/readmeai \
  configure \
  --default-api gemini \
  --default-model gemini-pro \
  --api-key "your-api-key"

# Show configuration
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "$HOME/.config/readmeai_docker_config:/home/readmeai_user/.readmeai" \
  readmeai/readmeai \
  configure-show

# List models
docker run --rm \
  -e API_KEY="your-api-key" \
  readmeai/readmeai \
  list-models \
  --api gemini
```

## Best Practices

1. **API Key Management**
   - Use environment variables for API keys in production
   - Consider using service account authentication for Gemini in production environments
   - Keep your API keys secure and never commit them to version control

2. **File Filtering**
   - Use `--extensions-to-allow` when you only want to analyze specific file types
   - Use `--dirs-to-ignore` to exclude build artifacts and dependencies
   - Use `--files-to-ignore` to exclude sensitive or irrelevant files

3. **Generation Parameters**
   - Adjust `--max-tokens` based on your project size
   - Use `--max-retries` and `--retry-delay` to handle API rate limits
   - Add `--additional-context` for better README generation

4. **Docker Usage**
   - Always use `--user "$(id -u):$(id -g)"` to avoid permission issues
   - Mount a volume for persistent configuration
   - Use `--rm` to clean up containers after use
