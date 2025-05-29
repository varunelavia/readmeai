# Project Title: README.ai Generator

## Description
This project is a Python script that generates comprehensive README.md files for a given code repository using AI services. The script can be configured to use multiple AI services such as `Gemini`, `Anthropic`, and `OpenAI`, each of them able to provide a unique style of content generation.

## Features

* Analyze a repository and generate a README.md file using AI services.
* Can be configured to use any of the following AI services: `Gemini`, `Anthropic`, `OpenAI`
* Retry logic in case of a failure during content generation
* Fetch and list models available with each provider (`Gemini`, `Anthropic`, `OpenAI`)
* Ability to specify ignored directories and files during the repository scan
* Docker support 

## Tech Stack

* Python 3.10
* Docker
* AI APIs: `Gemini`, `Anthropic`, `OpenAI`
* External Libraries: `google-generativeai`, `anthropic`, `openai`

## Installation

Prerequisite: 
- Python 3.10
- Docker

Step by Step install guide:
1. Clone or download the repository.
2. For Python script, install the requirements using pip:
    ```sh
    pip install -r requirements.txt
    ```
3. For Docker, build the image from the provided `Dockerfile`:
    ```sh
    docker build -t readmeai .
    ```

## Usage

### Python Script

Use the following command:

```sh
python readmeai.py generate --api=openai --ai-model=gpt-3.5 PATH_TO_YOUR_DIR
```

To see all available options:

```sh
python readmeai.py --help
```

### Docker Image

To run the Docker image:

```sh
docker run --rm -it -v PATH_TO_REPO:/app/data readmeai:latest generate --api=openai --ai-model=gpt-3.5 ./data
```

## Running Tests

Currently, the script does not contain any tests. This could be an area of contribution!

## Deployment

The Python script is easy to deploy and can be run directly in the terminal. In addition, a Dockerfile is included for containerization of the application. The script can also be easily integrated into Continuous Deployment (CD) pipelines to generate updated README files automatically.

## Contributing

The project currently doesn't have any contribution guidelines. Adding contribution guidelines can benefit the repository.

## License

The information regarding the type of license used has not been provided. Considering adding a license to specify the terms of use of the repository.

## Acknowledgements

The repository uses the following AI services:

* Google's `Gemini` Generative AI Model for content generation.
* `Anthropic` AI for text generation.
* `OpenAI` for completion tasks and draft content creation.

## Contact

No contact information has been provided. Considering adding means of contact for support or queries.