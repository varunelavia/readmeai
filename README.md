# readmeai: AI-Powered README Generator

[![Docker Pulls](https://img.shields.io/docker/pulls/readmeai/readmeai)](https://hub.docker.com/r/readmeai/readmeai)

This command-line tool leverages the power of AI to automatically generate comprehensive and informative `README.md` files for your code repositories. Analyze your project's structure and content to create a tailored README, saving you time and effort.  Currently supports Google Gemini, with planned support for Anthropic and OpenAI.

## Features

* **Automated README Generation:** Analyzes your codebase to generate a structured `README.md` file.
* **Intelligent Content:** Identifies the project type, programming languages, frameworks, and key features.
* **Customizable:** Provides options to ignore specific directories and files, and add additional context.
* **Multiple AI API Support:** Supports Google Gemini, and designed for future integration with Anthropic and OpenAI.
* **Dockerized:** Easily run within a Docker container for consistent and isolated execution.
* **Configurable:** Allows saving default API keys and model preferences.
* **Model Discovery:** Lists available models for supported APIs.

## Tech Stack

* **Python 3.10:** Core programming language.
* **Google Generative AI:** AI service for README generation.
* **Anthropic (Planned):** Future support for Anthropic AI models.
* **OpenAI (Planned):** Future support for OpenAI models.
* **Docker:** Containerization technology for deployment and distribution.

## Requirements

* Python 3.10+ (if running locally)
* Docker (recommended)
* API Key for chosen AI service (Google Gemini, Anthropic, or OpenAI).

## Installation

### Using Docker (Recommended)

1.  Pull the latest image from Docker Hub:

    ```bash
    docker pull readmeai/readmeai
    ```

2.  Run the tool:

    ```bash
    docker run -v $(pwd):/app readmeai/readmeai generate . --api gemini --ai-model <your_gemini_model> --api-key <your_api_key>
    ```
    Replace `<your_gemini_model>` with a valid Gemini model (obtainable using the `list-models --api gemini --api-key <your_api_key>` command)  and `<your_api_key>` with your actual API key. The `-v $(pwd):/app` mounts your current directory into the container so the README is written locally.

### Local Installation

1.  Create a virtual environment (recommended):

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.  Run the tool:

    ```bash
    python readmeai.py generate <path_to_repository> --api gemini --ai-model <your_gemini_model> --api-key <your_api_key>
    ```
    Replace `<path_to_repository>` with the path to the code repository you want to analyze, `<your_gemini_model>` with the desired model, and `<your_api_key>` with your API key.


## Usage


### Generating a README

```bash
python readmeai.py generate <path_to_repository> --api <api> --ai-model <ai_model> --api-key <api_key> [options]
```

*   `<path_to_repository>`: The path to the directory you want to analyze.  Use `.` for the current directory.
*   `--api`:  The AI API to use (e.g., `gemini`).
*   `--ai-model`:  The specific AI model to use (e.g., `models/gemini-pro`).
*   `--api-key`: Your API key for the selected service.
*   `--dirs-to-ignore` (optional): Comma-separated list of directories to ignore (e.g., `.git,.venv,node_modules`).
*   `--files-to-ignore` (optional): Comma-separated list of files to ignore (e.g., `package-lock.json,.DS_Store`).
*   `--additional-context` (optional): Additional text to provide context to the AI.
*   `--readme-filename` (optional): The name of the README file (default: `README.md`).



### Configuration

```bash
python readmeai.py configure --api-key <your_api_key> --default-api <api> --default-model <ai_model> 
```

This command allows you to set your API key, default API provider, and default model. These settings are stored in a configuration file (`~/.readmeai/config.json`) and will be used unless overridden by command-line arguments.

### Listing Available Models

```bash
python readmeai.py list-models --api <api> [--api-key <your_api_key>]
```
Lists the available models for the specified `api`.  You must provide an `api-key` unless it has been configured.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT License