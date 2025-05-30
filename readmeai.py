#!/usr/bin/env python3
"""
README.ai - AI-Powered README Generator

A command-line tool that generates comprehensive README.md files for your projects
using various AI services (OpenAI, Anthropic, Google Gemini).

Features:
- Generate detailed READMEs from your codebase
- Support for multiple AI providers
- Configurable settings and API keys
- Smart file filtering and context gathering
- Retry mechanism for API reliability

For more information, visit: https://github.com/varunelavia/readmeai
"""

import argparse
import anthropic
from openai import OpenAI
import os
import sys
import json
from pathlib import Path
from typing import List, Optional, Dict, Union, Any
import time
import logging
from datetime import datetime

# It's more common to import the google.generativeai package like this:
import google.generativeai as genai

# --- Constants ---
DEFAULT_README_FILENAME: str = "README.md"
CONFIG_FILE: str = os.path.expanduser("~/.readmeai/config.json")
MAX_RETRIES: int = 3
RETRY_DELAY: int = 2  # seconds
DEFAULT_MAX_TOKENS: int = 2048  # Reasonable default for README generation
SUPPORTED_APIS: List[str] = ["gemini", "anthropic", "openai"]

# Core directories to ignore - minimal set for essential functionality
DEFAULT_IGNORE_DIRS: List[str] = [".git", "node_modules", "venv", "__pycache__", ".pytest_cache", "dist", "build"]

# Core files to ignore - essential files that shouldn't be included in README generation
DEFAULT_IGNORE_FILES: List[str] = [
    # System and IDE files
    ".DS_Store", "Thumbs.db", ".env*", ".vscode/*", ".idea/*", "*.swp", "*.swo",
    
    # Package manager files
    "package-lock.json", "yarn.lock", "composer.lock", "poetry.lock", "Cargo.lock",
    
    # Compiled and binary files
    "*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll", "*.dylib", "*.class",
    "*.o", "*.obj", "*.exe", "*.bin", "*.dat", "*.db", "*.sqlite",
    
    # Build and cache files
    "*.egg-info", "*.egg", "*.whl", "*.tar.gz", "*.zip", "*.rar", "*.7z",
    "*.log", "*.tmp", "*.temp", "*.cache", "*.pid", "*.pid.lock",
    
    # Media and binary assets
    "*.jpg", "*.jpeg", "*.png", "*.gif", "*.ico", "*.svg", "*.webp",
    "*.mp3", "*.mp4", "*.mov", "*.avi", "*.wav", "*.pdf", "*.doc", "*.docx",
    
    # Font files
    "*.ttf", "*.otf", "*.woff", "*.woff2", "*.eot",
    
    # Test and coverage files
    "coverage.xml", "*.lcov", "*.coverage", "htmlcov/*", ".coverage.*",
    
    # Documentation files (except README.md)
    "*.md", "*.rst", "LICENSE*", "CHANGELOG*", "AUTHORS*",
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# The prompt is quite large. Keeping it as a constant here.
# For very complex prompts or internationalization, consider loading from a template file.
GENERATION_PROMPT_TEMPLATE: str = """
You are an expert AI programmer tasked with generating a comprehensive and suitable README.md file for a given code repository.

The input will be a single string variable containing the contents of all relevant files in the repository. Each file's content is preceded by its filename and a newline character, and files are separated by a newline character.

Your task is to:

1.  **Analyze the provided file contents** to understand the **purpose and functionality** of the repository. Determine the primary programming language(s) used and any significant frameworks or libraries.
2.  **Identify the type of project** (e.g., web application, mobile app, data science project, library, command-line tool, terraform module, terraform provider, terraform code etc.).
3.  **Generate a complete README.md file in Markdown format.** The primary goal is to create a README that is genuinely useful and informative for this specific repository.

    **Below is a list of common sections found in README files. Consider these as suggestions and examples. Not all sections are mandatory for every project, and you are not limited to only these sections. Feel free to include, exclude, or adapt sections based on what is most relevant and beneficial for understanding and using this particular repository:**

    * **Project Title:** A concise and descriptive title.
    * **Description:** A brief overview of what the project does, its key features, and the problem it solves.
    * **Table of Contents (Consider if helpful):**
    * **Features:** A bulleted list of the main functionalities.
    * **Tech Stack/Requirements:** List the primary technologies, languages, frameworks, and any prerequisites needed to run or build the project.
    * **Installation:** Step-by-step instructions on how to get the project set up and running locally. Include any necessary commands.
    * **Usage:** How to use the project or examples of its functionality. If it's a library, show how to import and use its functions. If it's an application, explain how to interact with it.
    * **Configuration (if applicable):** Explain any necessary configuration steps or environment variables.
    * **API Reference (if applicable):** For libraries or APIs, provide details on endpoints, request/response formats, etc.
    * **File Structure (Consider if helpful for complex projects):** A brief overview of the important directories and files.
    * **Running Tests (if applicable):** How to execute any included tests.
    * **Deployment (if applicable):** Instructions or notes on how to deploy the project.
    * **Contributing:** Guidelines for contributing to the project.
    * **License:** The license under which the project is shared. (Suggest adding this if not found)
    * **Acknowledgements:** Credit any resources or inspirations.
    * **Contact:** How to get in touch for support or questions.

    **Be flexible and prioritize creating a README that best serves the repository's needs.**

**Important Considerations:**

* The README should be well-structured, clear, and easy to understand.
* Use appropriate Markdown formatting (headings, lists, code blocks, etc.).
* Infer as much as possible from the provided code. If certain information isn't present in the code (e.g., license, specific deployment steps not evident from a Dockerfile or similar), you can make reasonable suggestions or indicate where the user should fill in details.
* Be concise but thorough. The length and detail should be appropriate for the project's complexity.
* The README should be in markdown format.

Here is the content of the repository:

{repository_content}
"""

def validate_api_key(api: str, api_key: str) -> bool:
    """Validate API key format and test connection."""
    if not api_key or len(api_key.strip()) < 10:  # Basic length check
        return False
        
    try:
        if api == "gemini":
            genai.configure(api_key=api_key)
            # Test connection by listing models
            genai.list_models()
        elif api == "anthropic":
            client = anthropic.Anthropic(api_key=api_key)
            # Test connection by listing models
            client.models.list()
        elif api == "openai":
            client = OpenAI(api_key=api_key)
            # Test connection by listing models
            client.models.list()
        return True
    except Exception as e:
        logger.error(f"API key validation failed for {api}: {e}")
        return False

def get_api_key(args: argparse.Namespace) -> Optional[str]:
    """
    Get the API key from various sources in order of priority:
    1. Command line argument (--api-key)
    2. Environment variable (API_KEY)
    3. Configuration file
    """
    if args.api_key:
        if validate_api_key(args.api, args.api_key):
            logger.info("Using API key from command line argument.")
            return args.api_key
        else:
            logger.error("Invalid API key provided via command line.")
            return None

    api_key: Optional[str] = os.getenv('API_KEY')
    if api_key and validate_api_key(args.api, api_key):
        logger.info("Using API key from API_KEY environment variable.")
        return api_key

    config = load_config()
    api_key = config.get('api_key')
    if api_key and validate_api_key(args.api, api_key):
        logger.info("Using API key from configuration file.")
        return api_key

    return None

def read_files_from_folder(
    folder_path: Path,
    dirs_to_ignore: Optional[List[str]] = None,
    files_to_ignore: Optional[List[str]] = None,
    extensions_to_ignore: Optional[List[str]] = None,
    extensions_to_allow: Optional[List[str]] = None
) -> str:
    """
    Reads content from files in a specified folder, skipping ignored ones.

    Args:
        folder_path: The Path object of the folder to read.
        dirs_to_ignore: A list of directory names to skip.
        files_to_ignore: A list of file names to skip.
        extensions_to_ignore: A list of file extensions to skip (e.g., ['py', 'js']).
        extensions_to_allow: A list of file extensions to explicitly allow (e.g., ['py', 'js']).
                           If provided, only files with these extensions will be processed.

    Returns:
        A string combining all read file contents, prefixed with their paths.

    Raises:
        FileNotFoundError: If the folder_path does not exist.
        ValueError: If no readable files are found.
    """
    if not folder_path.exists() or not folder_path.is_dir():
        raise FileNotFoundError(f"Error: Folder path '{folder_path}' does not exist or is not a directory.")

    # Merge default ignore lists with user-provided ones
    _dirs_to_ignore: List[str] = list(set(DEFAULT_IGNORE_DIRS + (dirs_to_ignore or [])))
    _files_to_ignore: List[str] = list(set(DEFAULT_IGNORE_FILES + (files_to_ignore or [])))
    _extensions_to_ignore: List[str] = [ext.lower().lstrip('.') for ext in (extensions_to_ignore or [])]
    _extensions_to_allow: List[str] = [ext.lower().lstrip('.') for ext in (extensions_to_allow or [])]

    logger.info(f"Scanning folder: {folder_path}")
    logger.debug(f"Ignoring directories: {_dirs_to_ignore}")
    logger.debug(f"Ignoring files: {_files_to_ignore}")
    if _extensions_to_ignore:
        logger.debug(f"Ignoring extensions: {_extensions_to_ignore}")
    if _extensions_to_allow:
        logger.debug(f"Only allowing extensions: {_extensions_to_allow}")

    file_contents: Dict[str, str] = {}
    total_files = 0
    skipped_files = 0
    max_file_size = 1024 * 1024  # 1MB limit per file

    for root, dirs, files in os.walk(folder_path, topdown=True):
        # Prune ignored and hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in _dirs_to_ignore]

        for filename in files:
            total_files += 1
            file_path = Path(root) / filename
            file_ext = file_path.suffix.lower().lstrip('.')
            
            # Skip ignored files, .md files, and hidden files
            if (any(filename.endswith(ext.lstrip('*')) for ext in _files_to_ignore) or
                filename.endswith('.md') or
                filename.startswith('.')):
                skipped_files += 1
                continue

            # Handle extension filtering
            if _extensions_to_allow:
                # If allow list is provided, only process files with allowed extensions
                if file_ext not in _extensions_to_allow:
                    logger.debug(f"Skipping file with non-allowed extension: {file_path}")
                    skipped_files += 1
                    continue
            elif _extensions_to_ignore and file_ext in _extensions_to_ignore:
                # If ignore list is provided and allow list is not, skip ignored extensions
                logger.debug(f"Skipping file with ignored extension: {file_path}")
                skipped_files += 1
                continue

            try:
                # Check file size
                if file_path.stat().st_size > max_file_size:
                    logger.warning(f"Skipping large file: {file_path} (size > 1MB)")
                    skipped_files += 1
                    continue

                # Store relative path for context in the prompt
                rel_path = file_path.relative_to(folder_path)
                content = file_path.read_text(encoding='utf-8')
                file_contents[str(rel_path)] = content
                logger.debug(f"Read file: {rel_path}")
            except UnicodeDecodeError:
                logger.warning(f"Could not decode file {file_path} as UTF-8. Skipping.")
                skipped_files += 1
            except Exception as e:
                logger.warning(f"Error reading file {file_path}: {e}. Skipping.")
                skipped_files += 1

    if not file_contents:
        raise ValueError(
            f"No readable files found in the repository. "
            f"Total files scanned: {total_files}, "
            f"Files skipped: {skipped_files}"
        )

    logger.info(f"Successfully read {len(file_contents)} files (skipped {skipped_files} files)")

    combined_content: str = ""
    for rel_path_str, content in file_contents.items():
        combined_content += f"\n=== {rel_path_str} ===\n{content}\n"

    return combined_content

def write_readme(content: str, output_folder: Path, readme_filename: str, skip_backup: bool = False) -> None:
    """
    Writes the generated README content to a file.

    Args:
        content: The string content to write to the README.
        output_folder: The Path object of the folder where the README will be saved.
        readme_filename: The name of the README file.
        skip_backup: Whether to skip backing up an existing README file.

    Raises:
        IOError: If the file cannot be written.
        Exception: For unexpected errors.
    """
    readme_path = output_folder / readme_filename
    
    # Check if README already exists
    if readme_path.exists() and not skip_backup:
        backup_path = readme_path.with_suffix(f'.{datetime.now().strftime("%Y%m%d_%H%M%S")}.md')
        try:
            readme_path.rename(backup_path)
            logger.info(f"Backed up existing README to: {backup_path}")
        except Exception as e:
            logger.warning(f"Could not backup existing README: {e}")

    try:
        readme_path.write_text(content, encoding='utf-8')
        logger.info(f"✅ README successfully written to: {readme_path.resolve()}")
    except IOError as e:
        logger.error(f"❌ Error: Could not write README file to '{readme_path}': {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ An unexpected error occurred while writing the README: {e}")
        sys.exit(1)

def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file."""
    config_dir = os.path.dirname(CONFIG_FILE)
    os.makedirs(config_dir, exist_ok=True)
    
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f"✅ Configuration saved to {CONFIG_FILE}")
    except Exception as e:
        logger.error(f"❌ Error saving configuration: {e}")
        sys.exit(1)

def load_config() -> Dict[str, Any]:
    """Load configuration from file."""
    if not os.path.exists(CONFIG_FILE):
        return {}
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"❌ Error loading configuration: {e}")
        return {}

def fetch_gemini_models(api_key: str) -> List[str]:
    """Fetch available models from Gemini API."""
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        return [model.name for model in models]
    except Exception as e:
        logger.error(f"❌ Error fetching Gemini models: {e}")
        return []

def fetch_anthropic_models(api_key: str) -> List[str]:
    """Fetch available models from Anthropic API."""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        models = client.models.list()
        return [model.id for model in models.data]
    except Exception as e:
        logger.error(f"❌ Error fetching Anthropic models: {e}")
        return []

def fetch_openai_models(api_key: str) -> List[str]:
    """Fetch available models from OpenAI API."""
    try:
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        # Filter for chat completion models only
        return [model.id for model in models.data if model.id.startswith(('gpt-3.5', 'gpt-4'))]
    except Exception as e:
        logger.error(f"❌ Error fetching OpenAI models: {e}")
        return []

def list_models(args: argparse.Namespace) -> None:
    """List available models for each API."""
    print("\nAvailable AI Models:")
    print("===================")
    
    # Get API key from args, config, or environment
    api_key = args.api_key or load_config().get('api_key') or os.getenv('API_KEY')
    
    # Get API from args or config
    api = args.api or load_config().get('default_api')
    
    if not api:
        print("Please specify an API to fetch models from using --api flag.")
        print(f"Available APIs: {', '.join(SUPPORTED_APIS)}")
        return
        
    if not api_key:
        print(f"❌ Error: No API key found for {api}. Please provide an API key using --api-key or configure it.")
        return
            
    if api == "gemini":
        models = fetch_gemini_models(api_key)
        print(f"\nGEMINI:")
        for model in models:
            print(f"  - {model}")
    elif api == "anthropic":
        models = fetch_anthropic_models(api_key)
        print(f"\nANTHROPIC:")
        for model in models:
            print(f"  - {model}")
    elif api == "openai":
        models = fetch_openai_models(api_key)
        print(f"\nOPENAI:")
        for model in models:
            print(f"  - {model}")

def configure(args: argparse.Namespace) -> None:
    """Configure API keys and default settings."""
    config = load_config()
    
    if args.api_key:
        if not validate_api_key(args.default_api or config.get('default_api', 'openai'), args.api_key):
            print("❌ Error: Invalid API key provided.")
            sys.exit(1)
        config['api_key'] = args.api_key
        print("✅ API key saved")
    
    if args.default_api:
        if args.default_api not in SUPPORTED_APIS:
            print(f"❌ Error: Invalid API '{args.default_api}'. Choose from: {', '.join(SUPPORTED_APIS)}")
            sys.exit(1)
        config['default_api'] = args.default_api
        print(f"✅ Default API set to {args.default_api}")
    
    if args.default_model:
        # Validate model exists for the API
        api_key = args.api_key or config.get('api_key') or os.getenv('API_KEY')
        if not api_key:
            print("❌ Error: No API key found. Please provide an API key to validate the model.")
            sys.exit(1)
            
        api = args.default_api or config.get('default_api')
        if not api:
            print("❌ Error: No API specified. Please specify the API for the model.")
            sys.exit(1)
            
        if api == "gemini":
            models = fetch_gemini_models(api_key)
        elif api == "anthropic":
            models = fetch_anthropic_models(api_key)
        elif api == "openai":
            models = fetch_openai_models(api_key)
            
        if args.default_model not in models:
            print(f"❌ Error: Invalid model '{args.default_model}' for API '{api}'")
            print("Available models:")
            for model in models:
                print(f"  - {model}")
            sys.exit(1)
            
        config['default_model'] = args.default_model
        print(f"✅ Default model set to {args.default_model}")
    
    if config:
        save_config(config)
    else:
        print("ℹ️ No configuration changes specified")

def generate_with_retry(api: str, client: Union[genai.GenerativeModel, anthropic.Anthropic, OpenAI], 
                       model: str, prompt: str, max_retries: int = MAX_RETRIES, 
                       max_tokens: int = DEFAULT_MAX_TOKENS) -> str:
    """Generate content with retry logic."""
    for attempt in range(max_retries):
        try:
            if api == "gemini":
                response = client.generate_content(prompt)
                return response.text
            elif api == "anthropic":
                response = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            elif api == "openai":
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=1,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"⚠️ Attempt {attempt + 1} failed: {e}. Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                raise e
    return ""

def show_config() -> None:
    """Display current configuration without exposing the API key."""
    config = load_config()
    if not config:
        print("No configuration found.")
        return

    print("\nCurrent Configuration:")
    print("=====================")
    
    # Show default API if set
    if 'default_api' in config:
        print(f"Default API: {config['default_api']}")
    
    # Show default model if set
    if 'default_model' in config:
        print(f"Default Model: {config['default_model']}")
    
    # Show API key status without exposing the key
    if 'api_key' in config:
        masked_key = config['api_key'][:4] + '*' * (len(config['api_key']) - 8) + config['api_key'][-4:]
        print(f"API Key: {masked_key}")
    
    print(f"\nConfiguration file: {CONFIG_FILE}")

def reset_config() -> None:
    """Delete the configuration file."""
    if os.path.exists(CONFIG_FILE):
        try:
            os.remove(CONFIG_FILE)
            print("✅ Configuration has been reset.")
        except Exception as e:
            print(f"❌ Error resetting configuration: {e}")
            sys.exit(1)
    else:
        print("No configuration file found.")

def validate_path(path: str) -> Path:
    """Validate and convert path string to Path object."""
    try:
        path_obj = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")
        if not path_obj.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {path}")
        return path_obj
    except Exception as e:
        raise ValueError(f"Invalid path: {e}")

def validate_comma_list(value: str, name: str) -> List[str]:
    """Validate comma-separated list input."""
    if not value:
        return []
    try:
        items = [item.strip() for item in value.split(',') if item.strip()]
        if not items:
            raise ValueError(f"Empty {name} list")
        return items
    except Exception as e:
        raise ValueError(f"Invalid {name} list: {e}")

def validate_api_model(api: str, model: str, api_key: str) -> None:
    """Validate API and model combination."""
    if api not in SUPPORTED_APIS:
        raise ValueError(f"Unsupported API: {api}. Choose from: {', '.join(SUPPORTED_APIS)}")
    
    if not model:
        raise ValueError("Model name is required")
    
    # Validate model exists for the API
    if api == "gemini":
        models = fetch_gemini_models(api_key)
    elif api == "anthropic":
        models = fetch_anthropic_models(api_key)
    elif api == "openai":
        models = fetch_openai_models(api_key)
        
    if model not in models:
        raise ValueError(f"Invalid model '{model}' for API '{api}'. Available models:\n" + 
                        "\n".join(f"  - {m}" for m in models))

def validate_numeric(value: int, name: str, min_val: int, max_val: int) -> int:
    """Validate numeric input within range."""
    try:
        num = int(value)
        if num < min_val or num > max_val:
            raise ValueError(f"{name} must be between {min_val} and {max_val}")
        return num
    except ValueError as e:
        raise ValueError(f"Invalid {name}: {e}")

def main() -> None:
    """Main function to parse arguments and handle commands."""
    parser = argparse.ArgumentParser(
        description="Generate README.md files using AI.\n\n"
                   "For more details, visit: https://github.com/varunelavia/readmeai",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a README.md file')
    generate_parser.add_argument(
        "path",
        type=str,
        help="Path to the directory to analyze."
    )
    generate_parser.add_argument(
        "--dirs-to-ignore",
        type=str,
        help="Comma-separated list of directory names to skip (e.g., '.git,node_modules,venv')."
    )
    generate_parser.add_argument(
        "--files-to-ignore",
        type=str,
        help="Comma-separated list of file names to skip (e.g., 'package-lock.json,.DS_Store')."
    )
    generate_parser.add_argument(
        "--extensions-to-ignore",
        type=str,
        help="Comma-separated list of file extensions to skip (e.g., 'py,js,css'). Do not include the dot."
    )
    generate_parser.add_argument(
        "--extensions-to-allow",
        type=str,
        help="Comma-separated list of file extensions to explicitly allow (e.g., 'py,js,css'). "
             "If provided, only files with these extensions will be processed. Do not include the dot."
    )
    generate_parser.add_argument(
        "--additional-context",
        type=str,
        help="Additional textual context about the project to provide to the AI."
    )
    generate_parser.add_argument(
        "--readme-filename",
        type=str,
        default=DEFAULT_README_FILENAME,
        help=f"Name of the README file to generate (default: {DEFAULT_README_FILENAME})."
    )
    generate_parser.add_argument(
        "--skip-readme-backup",
        action="store_true",
        help="Skip backing up existing README file if it exists."
    )
    generate_parser.add_argument(
        "--api",
        type=str,
        choices=SUPPORTED_APIS,
        help="AI API to use for generating the README."
    )
    generate_parser.add_argument(
        "--ai-model",
        type=str,
        help="AI model to use."
    )
    generate_parser.add_argument(
        "--api-key",
        type=str,
        help="API key for the selected AI service. Overrides API_KEY environment variable."
    )
    generate_parser.add_argument(
        "--max-retries",
        type=int,
        default=MAX_RETRIES,
        help=f"Maximum number of retries for API calls (default: {MAX_RETRIES})."
    )
    generate_parser.add_argument(
        "--retry-delay",
        type=int,
        default=RETRY_DELAY,
        help=f"Delay between retries in seconds (default: {RETRY_DELAY})."
    )
    generate_parser.add_argument(
        "--max-tokens",
        type=int,
        default=DEFAULT_MAX_TOKENS,
        help=f"Maximum number of tokens to generate (default: {DEFAULT_MAX_TOKENS})."
    )
    generate_parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging."
    )
    
    # Configure command
    config_parser = subparsers.add_parser('configure', help='Configure API keys and default settings')
    config_parser.add_argument(
        "--api-key",
        type=str,
        help="Set the API key for the selected service"
    )
    config_parser.add_argument(
        "--default-api",
        type=str,
        choices=SUPPORTED_APIS,
        help="Set the default API to use"
    )
    config_parser.add_argument(
        "--default-model",
        type=str,
        help="Set the default model to use"
    )
    
    # Show configuration command
    subparsers.add_parser('configure-show', help='Display current configuration')
    
    # Reset configuration command
    subparsers.add_parser('configure-reset', help='Reset configuration by deleting the config file')
    
    # List models command
    list_models_parser = subparsers.add_parser('list-models', help='List available models for each API')
    list_models_parser.add_argument(
        "--api",
        type=str,
        choices=SUPPORTED_APIS,
        help="Fetch models from specific API (requires API key)"
    )
    list_models_parser.add_argument(
        "--api-key",
        type=str,
        help="API key for fetching models (optional if configured)"
    )
    
    # Version argument
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    args = parser.parse_args()

    # Set debug logging if requested
    if hasattr(args, 'debug') and args.debug:
        logger.setLevel(logging.DEBUG)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'list-models':
            list_models(args)
            return

        if args.command == 'configure':
            configure(args)
            return
            
        if args.command == 'configure-show':
            show_config()
            return
            
        if args.command == 'configure-reset':
            reset_config()
            return

        if args.command == 'generate':
            # Validate path
            target_path = validate_path(args.path)
            
            # Validate numeric inputs
            max_retries = validate_numeric(args.max_retries, "max-retries", 1, 10)
            retry_delay = validate_numeric(args.retry_delay, "retry-delay", 1, 30)
            max_tokens = validate_numeric(args.max_tokens, "max-tokens", 100, 4096)
            
            # Validate comma-separated lists
            dirs_to_ignore_list = validate_comma_list(args.dirs_to_ignore, "directories to ignore") if args.dirs_to_ignore else None
            files_to_ignore_list = validate_comma_list(args.files_to_ignore, "files to ignore") if args.files_to_ignore else None
            extensions_to_ignore_list = validate_comma_list(args.extensions_to_ignore, "extensions to ignore") if args.extensions_to_ignore else None
            extensions_to_allow_list = validate_comma_list(args.extensions_to_allow, "extensions to allow") if args.extensions_to_allow else None
            
            # Load configuration
            config = load_config()
            
            # Use command line args or fall back to config
            api = args.api or config.get('default_api')
            ai_model = args.ai_model or config.get('default_model')
            api_key = get_api_key(args)

            if not api:
                raise ValueError("No API specified. Use --api or configure a default API.")
            
            if not ai_model:
                raise ValueError("No AI model specified. Use --ai-model or configure a default model.")

            if not api_key:
                raise ValueError(
                    "No valid API key found. Please provide an API key using one of these methods:\n"
                    "1. Command line argument: --api-key YOUR_API_KEY\n"
                    "2. Environment variable: export API_KEY='YOUR_API_KEY'\n"
                    "3. Configuration: readmeai.py configure --api-key YOUR_API_KEY\n\n"
                    "To get an API key, visit the respective service's website.\n\n"
                    "For more information, visit: https://github.com/varunelavia/readmeai"
                )

            # Validate API and model combination
            validate_api_model(api, ai_model, api_key)

            # Initialize API clients
            if api == "gemini":
                try:
                    genai.configure(api_key=api_key)
                    client = genai.GenerativeModel(ai_model)
                except Exception as e:
                    raise RuntimeError(f"Failed to configure Gemini API: {e}")
            elif api == "anthropic":
                try:
                    client = anthropic.Anthropic(api_key=api_key)
                except Exception as e:
                    raise RuntimeError(f"Failed to configure Anthropic API: {e}")
            elif api == "openai":
                try:
                    client = OpenAI(api_key=api_key)
                except Exception as e:
                    raise RuntimeError(f"Failed to configure OpenAI API: {e}")

            try:
                repository_content: str = read_files_from_folder(
                    target_path,
                    dirs_to_ignore_list,
                    files_to_ignore_list,
                    extensions_to_ignore_list,
                    extensions_to_allow_list
                )
            except FileNotFoundError as e:
                raise ValueError(f"Directory not found: {e}")
            except ValueError as e:
                raise ValueError(f"Error reading files: {e}")
            except Exception as e:
                raise RuntimeError(f"Unexpected error while reading files: {e}")

            prompt = GENERATION_PROMPT_TEMPLATE.format(repository_content=repository_content)

            if args.additional_context:
                prompt += f"\n\nAdditional Context Provided by User:\n{args.additional_context}"

            logger.info(f"🤖 Attempting to generate README using {api} model: {ai_model}...")
            try:
                generated_text = generate_with_retry(
                    api, 
                    client, 
                    ai_model, 
                    prompt, 
                    max_retries,
                    max_tokens
                )
            except Exception as e:
                raise RuntimeError(f"{api} content generation failed after {max_retries} retries: {e}")

            if not generated_text.strip():
                raise ValueError("The AI returned an empty response. Cannot generate README.")

            write_readme(generated_text, target_path, args.readme_filename, args.skip_readme_backup)
            logger.info("🎉 README generation process complete!")

    except ValueError as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()