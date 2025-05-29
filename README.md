# readmeai

A command-line tool that **generates high-quality `README.md` files for code repositories using advanced AI models** (Gemini, Anthropic, OpenAI). It scans your project files, summarizes their purpose and structure, and produces a comprehensive, professional README in Markdown format—saving you hours of manual documentation work.

---

## Table of Contents

- [Features](#features)
- [Tech Stack / Requirements](#tech-stack--requirements)
- [Installation](#installation)
  - [Using Docker](#using-docker)
  - [Manual Installation](#manual-installation)
- [Usage](#usage)
  - [Basic README Generation](#basic-readme-generation)
  - [Configuration](#configuration)
  - [Listing Available AI Models](#listing-available-ai-models)
- [Configuration](#configuration)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

---

## Features

- **AI-powered README Generation:** Produces detailed `README.md` files by analyzing your repository code.
- **Supports Multiple AI Providers:** Use Google Gemini, Anthropic Claude, or OpenAI GPT models.
- **Easy Setup:** Configure API keys and defaults interactively or via command-line flags.
- **Customizable Ignore Lists:** Skip files or directories from analysis (e.g., `.git`, `venv`, `node_modules`).
- **Docker Support:** Run the tool with zero local Python setup using Docker.
- **Model Listing:** Quickly view supported models for your chosen AI provider.
- **Simple CLI Interface:** Intuitive commands for generating, configuring, and exploring models.

---

## Tech Stack / Requirements

- **Programming Language:** Python 3.10+
- **Core Libraries:**
    - [`google-generativeai`](https://pypi.org/project/google-generativeai/) (Gemini)
    - [`anthropic`](https://pypi.org/project/anthropic/) (Claude)
    - [`openai`](https://pypi.org/project/openai/) (GPT)
- **Other:** Docker (optional, for containerized usage)

### Python Dependencies

See `requirements.txt`:
```
google-generativeai==0.8.5
anthropic==0.52.1
openai==1.82.1
```

---

## Installation

### Using Docker

The recommended way to use `readmeai` is via Docker (no need for local Python or dependencies):

```sh
# Build the Docker image
docker build -t readmeai .

# Run the tool (replace /path/to/your/project with the absolute path to your code)
docker run --rm -it \
  -e API_KEY=YOUR_MODEL_API_KEY \
  -v /path/to/your/project:/app \
  readmeai generate . --api openai --ai-model gpt-4o
```

*Replace `YOUR_MODEL_API_KEY` and choose the appropriate `--api` and `--ai-model`. See [Configuration](#configuration) below.*

---

### Manual Installation

1. **Clone the repository** (or copy `readmeai.py` to your project):

    ```sh
    git clone https://github.com/yourusername/readmeai.git
    cd readmeai
    ```

2. **Install Python dependencies:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

3. **(Optional) Make the script executable:**

    ```sh
    chmod +x readmeai.py
    ```

---

## Usage

### Basic README Generation

1. **Set your API key** (for OpenAI/Gemini/Anthropic):

    ```sh
    export API_KEY=YOUR_MODEL_API_KEY
    ```

2. **Generate a README:**

    ```sh
    python readmeai.py generate . --api openai --ai-model gpt-4o
    ```

    - The tool will scan your project directory and produce (or overwrite) `README.md` in place.

#### Additional Options

- **Ignore folders/files:**
    ```sh
    python readmeai.py generate . --dirs-to-ignore .git,venv,node_modules --files-to-ignore package-lock.json,.DS_Store
    ```
- **Specify output filename:**
    ```sh
    python readmeai.py generate . --readme-filename MYDOC.md
    ```
- **Add extra project context for the AI:**
    ```sh
    python readmeai.py generate . --additional-context "This project is for a hackathon. It uses FastAPI."
    ```

---

### Configuration

Set up your default API provider and model once:

```sh
python readmeai.py configure --api-key YOUR_API_KEY --default-api openai --default-model gpt-4o
```

- Your configuration is saved in `~/.readmeai/config.json`.
- You can override the API provider or model with command-line flags anytime.

---

### Listing Available AI Models

See which models are available for your chosen provider:

```sh
python readmeai.py list-models --api openai
python readmeai.py list-models --api gemini
python readmeai.py list-models --api anthropic
```

---

## File Structure

```
├── readmeai.py          # Main CLI script
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build instructions
```

- The tool creates a configuration file at: `~/.readmeai/config.json`

---

## Contributing

Contributions, issue reports, and suggestions are welcome!

- Please open issues or pull requests via GitHub.
- For major changes, discuss them via issue first.
- See `CONTRIBUTING.md` (if present) for details.

---

## License

*No license file detected.*  
**We recommend adding a `LICENSE` file (e.g., MIT, Apache 2.0) to clarify usage rights.**

---

## Acknowledgements

- Inspired by the need for better documentation automation.
- Built with the power of OpenAI, Anthropic, and Google Generative AI APIs.

---

## Contact

For support or questions, open an issue or contact the maintainer via GitHub.

---

**Happy documenting! 🚀**