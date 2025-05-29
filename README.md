# README.md

## READMEai - AI-Powered README Generator

### Table of Contents
1. [Description](#description)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [API Keys](#api-keys)
8. [AI Model Selection and Validation](#ai-model-selection-and-validation)
9. [Running with Docker](#running-with-docker)
10. [Contributions](#contributions)
11. [License](#license)
12. [Contact](#contact)

### Description

READMEai is a command-line tool developed in Python, that uses various AI services (OpenAI, Anthropic, Google Gemini) to generate comprehensive README.md files for your projects from the given codebase. 

This tool takes in a directory, reads through the files, and uses AI to generate a detailed README that includes project title, description, how to install and use the project, features, technologies used and so on, based on the analysed codebase.

### Features
- Generate detailed READMEs automatically from your codebase
- Support for multiple AI providers (Google Gemini, Anthropic, OpenAI)
- Configurable settings and API keys
- Smart file filtering and context gathering
- Retry mechanism for API reliability
- Docker support for easy setup and execution

### Requirements
The main requirements are the following:
- Python 3.8+
- OpenAI 1.82.1
- Google GenerativeAI 0.8.5
- Anthropic 0.52.1

For the full list of dependencies, please see the requirements.txt file.

### Installation

Clone the repository and install all necessary packages:

```bash
git clone https://github.com/yourusername/readmeai.git
cd readmeai
pip install -r requirements.txt
```

### Usage

To generate a README file for a supplied directory, you can run the following command:

```bash
python readmeai.py generate /path/to/your/project
```

Numerous optional arguments are available to control functionality. You can view them by using the help command:

```bash
python readmeai.py --help
```

### Configuration

Configure the tool using the configure command:

```bash
python readmeai.py configure
```

### API Keys

In order to use any of the supported APIs (Gemini, Anthropic, OpenAI), you'll need to provide an API key. API keys can be provided via the command line (`--api-key YOUR_API_KEY`), as an environment variable (`export API_KEY='YOUR_API_KEY'`), or through the tool’s configuration command.

### AI Model Selection and Validation

You can also specify which AI model you want to use by passing the `--default-model` and `--default-api` arguments during the configuration step. The tool ensures the chosen model exists within the specified API before starting the generations process.

### Running with Docker

For Docker users, a Dockerfile has been provided:

Build the Docker image:

```bash
docker build -t readmeai .
```

Run the tool:

```bash
docker run -v ${PWD}:/app readmeai generate /app/your-directory-to-analyze
```

### Contributions

This project welcomes contributions from the open source community. To contribute, just fork this repository, make your changes and create a pull request.

### License

This section is yet to be generated. The developer can fill it as per the chosen license.

### Contact

For any further queries, issues or suggestions, feel free to create an issue at https://github.com/yourusername/readmeai/issues.