# README.ai CLI Reference

This document provides a detailed reference for all README.ai command-line interface (CLI) commands and options.

## Global Options

- `-v, --version`: Display the version number and exit
- `--debug`: Enable debug logging for detailed troubleshooting

## Commands

### `generate` - Generate README

The main command to analyze a codebase and generate a README file.

```bash
readmeai generate [OPTIONS] PATH
```

#### Required Arguments
- `PATH`: Path to the directory to analyze
  - Must be a valid directory path
  - Directory must exist and be accessible

#### Optional Arguments
- `--dirs-to-ignore`: Comma-separated list of directories to skip
  - Example: `--dirs-to-ignore "tests,docs,node_modules"`
  - Default: `.git,node_modules,venv,__pycache__,.pytest_cache,dist,build`

- `--files-to-ignore`: Comma-separated list of files to skip
  - Example: `--files-to-ignore "config.json,secrets.env"`
  - Default: Various system files, package locks, compiled files, media files, and documentation

- `--extensions-to-ignore`: File extensions to skip (without dots)
  - Example: `--extensions-to-ignore "py,js,css"`
  - Cannot be used with `--extensions-to-allow`

- `--extensions-to-allow`: Only process files with these extensions
  - Example: `--extensions-to-allow "py,js,ts"`
  - Cannot be used with `--extensions-to-ignore`

- `--additional-context`: Extra context about the project
  - Example: `--additional-context "This is a machine learning project focused on NLP"`

- `--readme-filename`: Output filename
  - Default: `README.md`
  - Example: `--readme-filename "PROJECT_README.md"`

- `--skip-readme-backup`: Skip backing up existing README file
  - No value required
  - Default: false (backup is created)

- `--api`: AI service to use
  - Choices: `gemini`, `anthropic`, `openai`
  - Default: Value from config file or must be specified

- `--ai-model`: Specific model to use
  - Must be a valid model for the chosen API
  - Use `list-models` to see available models
  - Default: Value from config file or must be specified

- `--api-key`: API key for the service
  - Overrides API_KEY environment variable and config file
  - Must be a valid API key for the chosen service

- `--max-retries`: Maximum API retry attempts
  - Default: 3
  - Range: 1-10

- `--retry-delay`: Delay between retries in seconds
  - Default: 2
  - Range: 1-30

- `--max-tokens`: Maximum tokens to generate
  - Default: 2048
  - Range: 100-4096

### `configure` - Set Default Settings

Save API keys and default preferences.

```bash
readmeai configure [OPTIONS]
```

#### Options
- `--api-key`: Set the API key
  - Must be a valid API key for the chosen service

- `--default-api`: Set default AI service
  - Choices: `gemini`, `anthropic`, `openai`

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

```bash
readmeai list-models [OPTIONS]
```

#### Options
- `--api`: Specific API to query
  - Choices: `gemini`, `anthropic`, `openai`
  - Required if no default API is configured

- `--api-key`: API key
  - Optional if configured
  - Must be a valid API key for the chosen service

## Examples

### Basic README Generation
```bash
readmeai generate /path/to/your/project
```

### Generate with Specific AI Service
```bash
readmeai generate /path/to/your/project --api gemini --ai-model gemini-pro
```

### Generate with Custom File Filtering
```bash
readmeai generate /path/to/your/project \
  --dirs-to-ignore "tests,docs" \
  --files-to-ignore "config.json,secrets.env" \
  --extensions-to-allow "py,js,ts"
```

### Generate with Additional Context
```bash
readmeai generate /path/to/your/project \
  --additional-context "This is a machine learning project focused on NLP"
```

### Configure Default Settings
```bash
readmeai configure \
  --api-key YOUR_API_KEY \
  --default-api openai \
  --default-model gpt-4
```

### List Available Models
```bash
readmeai list-models --api gemini
```

## Environment Variables

- `API_KEY`: API key for the selected AI service
  - Used if not provided via command line
  - Example: `export API_KEY='your-api-key'`

## Configuration File

The configuration is stored in `~/.readmeai/config.json` and includes:
- API key
- Default API service
- Default model

## Exit Codes

- `0`: Success
- `1`: Error (invalid input, API failure, etc.)
- `2`: Configuration error
- `3`: File system error
