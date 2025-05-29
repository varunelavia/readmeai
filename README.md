# README.md for README.ai - AI-Powered README Generator

## Project Title

**README.ai - AI-Powered README Generator**

## Description

The repository consists of a command-line tool "README.ai", which uses various AI services (OpenAI, Anthropic, Google Gemini) to auto-generate comprehensive README.md files for your projects. The script analyzes your directory's files, building a prompt from the contents, which is then sent to the chosen AI for content generation.

The README.ai is capable of analyzing different codebases and making intelligent decisions to generate high-quality READMEs. Additionally, this script allows the use of multiple AI providers and comes equipped with features such as smart file filtering, configurable settings and API keys, and an integrated retry mechanism for better API reliability.

## Features

- Generate README files from existing project files
- Support for multiple AI providers like OpenAI, Anthropic, Google Gemini
- User-configurable settings and API keys
- Gathers context by smart file filtering
- Retry mechanism for handling API unreliability

## Tech Stack/Requirements

The project is predominantly created using Python. The libraries used primarily include OpenAI, Anthropic, and google.generativeai (as genai). A Dockerfile is present to containerize the application, suggesting deployment through a Docker runtime environment. The API key for AI services needs to be provided either as an environment variable or a command-line argument.

## Installation

Please follow the below instructions to set up README.ai on your local system:

1. Clone the repository into your local system using git clone command.
```bash
git clone https://github.com/varunelavia/readmeai.git
```
2. Navigate to the cloned repository.
```bash
cd readmeai
```
3. Create a virtual environment (Optional but Recommended).
```bash
python3 -m venv myenv
```
4. Activate the virtual environment. For Unix or MacOS system,
```bash
source myenv/bin/activate
```
5. Install the required dependencies.
``` bash
pip install openai anthropic google-cloud-aiplatform
```
6. Set the required environment variables:
```bash
export API_KEY='your_api_key'
```
7. You're set to use README.ai. Run it with the `--help` argument to see its usage:
```bash
python readmeai.py --help
```

For docker installation, use the Dockerfile provided in the repository.

## Usage

You can use the `readmeai.py` script to generate README files from your existing project files. 

Here is an example of how one might invoke it:

```bash
python readmeai.py generate path_to_your_directory
```

You can provide additional flags as per your requirements. Type `python readmeai.py --help` to see the list of accepted flags.

For instance, you can specify a different AI service provider using the `--api` flag like so:

```bash
python readmeai.py generate path_to_directory --api anthropic
```

Please replace `path_to_directory` with the path to your project directory.

## Configuration

You can configure the `readmeai.py` script using the `configure` command:

```bash
python readmeai.py configure --api-key YOUR_API_KEY --default-api openai --default-model text-davinci-002
```

Please replace `YOUR_API_KEY` with your API Key. The API key can