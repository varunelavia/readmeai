# ReadMeAI

A Python script for generating comprehensive README.md files using AI.

## Description

ReadMeAI is a command-line tool that leverages AI to automatically generate high-quality README files for your code repositories. It analyzes the contents of your repository, identifies the project type and technologies used, and generates a well-structured README in Markdown format.

## Features

- Automatically generates a complete README.md file
- Supports various AI services: Google Generative AI (Gemini), Anthropic, and OpenAI
- Allows customization of ignored directories and files
- Provides commands for configuration and listing available AI models
- Containerized using Docker for easy deployment and usage

## Requirements

- Python 3.10+
- google-generativeai==0.8.5

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/readmeai.git
   ```

2. Change to the project directory:
   ```
   cd readmeai
   ```

3. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate
   ```

4. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

```
python readmeai.py [command] [options]
```

Available commands:
- `generate`: Generate a README.md file
- `configure`: Configure API keys and default settings
- `list-models`: List available models for each API

For detailed usage instructions and options, run:
```
python readmeai.py --help
```

## Configuration

Before using ReadMeAI, you need to configure the API key for your desired AI service. You can do this using the `configure` command:

```
python readmeai.py configure --api-key YOUR_API_KEY --default-api [gemini|anthropic|openai] --default-model MODEL_NAME
```

Replace `YOUR_API_KEY` with your actual API key, choose the default API service, and specify the default model to use.

## Docker Usage

ReadMeAI can also be run using Docker. To build the Docker image, run:

```
docker build -t readmeai .
```

Then, you can run the container with the desired command and options. For example:

```
docker run --rm readmeai generate /path/to/your/repository
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

ReadMeAI was inspired by the need for automated README generation and the capabilities of modern AI services.

## Contact

For any questions or inquiries, please contact [your-email@example.com](mailto:your-email@example.com).