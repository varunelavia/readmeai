#!/usr/bin/env python3
"""
Generates a README.md file for a code repository using Google's Gemini AI.

This script reads the contents of specified files in a directory,
constructs a prompt for a Gemini model, and then generates a README.md
file based on the model's response.
"""

import argparse
import anthropic
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Union

# It's more common to import the google.generativeai package like this:
import google.generativeai as genai

# --- Constants ---
DEFAULT_README_FILENAME: str = "README.md"

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


def get_api_key(args: argparse.Namespace) -> Optional[str]:
    """
    Get the API key from various sources in order of priority:
    1. Command line argument (--api-key)
    2. Environment variable (API_KEY)
    """
    if args.api_key:
        print("Using API key from command line argument.")
        return args.api_key

    api_key: Optional[str] = os.getenv('API_KEY')
    if api_key:
        print("Using API key from API_KEY environment variable.")
        return api_key

    return None


def read_files_from_folder(
    folder_path: Path,
    dirs_to_ignore: Optional[List[str]] = None,
    files_to_ignore: Optional[List[str]] = None
) -> str:
    """
    Reads content from files in a specified folder, skipping ignored ones.

    Args:
        folder_path: The Path object of the folder to read.
        dirs_to_ignore: A list of directory names to ignore.
        files_to_ignore: A list of file names to ignore.

    Returns:
        A string combining all read file contents, prefixed with their paths.

    Raises:
        FileNotFoundError: If the folder_path does not exist.
    """
    if not folder_path.exists() or not folder_path.is_dir():
        raise FileNotFoundError(f"Error: Folder path '{folder_path}' does not exist or is not a directory.")

    file_contents: Dict[str, str] = {}
    # Ensure default empty lists if None
    _dirs_to_ignore: List[str] = dirs_to_ignore or []
    _files_to_ignore: List[str] = files_to_ignore or []

    print(f"Scanning folder: {folder_path}")
    print(f"Ignoring directories: {_dirs_to_ignore}")
    print(f"Ignoring files: {_files_to_ignore}")

    for item in folder_path.rglob('*'): # rglob for recursive globbing
        if item.is_dir():
            # Skip hidden directories and ignored directories
            if item.name.startswith('.') or item.name in _dirs_to_ignore:
                # To prevent rglob from going into these dirs, ideally os.walk behavior is better
                # For pathlib, one would typically filter after getting all paths or build a complex generator.
                # For simplicity with rglob, we just skip if the parent is ignored.
                # This is a limitation of rglob vs os.walk for complex skipping logic.
                # A more robust way with rglob is to get all files and then filter paths.
                # os.walk is actually better for conditional pruning of directories. Let's stick to that.
                pass # Handled by os.walk's dir pruning below

        # Let's revert to os.walk for its directory pruning capability which is more efficient
        # for ignoring directories.
    for root, dirs, files in os.walk(folder_path, topdown=True):
        # Prune ignored and hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in _dirs_to_ignore]

        for filename in files:
            # Skip ignored files, .md files (usually READMEs themselves), and hidden files
            if (filename in _files_to_ignore or
                filename.endswith('.md') or
                filename.startswith('.')):
                continue

            file_path = Path(root) / filename
            try:
                # Store relative path for context in the prompt
                rel_path = file_path.relative_to(folder_path)
                content = file_path.read_text(encoding='utf-8')
                file_contents[str(rel_path)] = content
                print(f"Read file: {rel_path}")
            except UnicodeDecodeError:
                print(f"Warning: Could not decode file {file_path} as UTF-8. Skipping.")
            except Exception as e:
                print(f"Warning: Error reading file {file_path}: {e}. Skipping.")

    if not file_contents:
        print("Warning: No files were read from the specified directory (or all were ignored/unreadable).")
        return "No readable file content found in the repository."

    combined_content: str = ""
    for rel_path_str, content in file_contents.items():
        combined_content += f"\n=== {rel_path_str} ===\n{content}\n"

    return combined_content


def write_readme(content: str, output_folder: Path, readme_filename: str) -> None:
    """
    Writes the generated README content to a file.

    Args:
        content: The string content to write to the README.
        output_folder: The Path object of the folder where the README will be saved.
        readme_filename: The name of the README file.
    """
    readme_path = output_folder / readme_filename
    try:
        readme_path.write_text(content, encoding='utf-8')
        print(f"✅ README successfully written to: {readme_path.resolve()}")
    except IOError as e:
        print(f"❌ Error: Could not write README file to '{readme_path}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ An unexpected error occurred while writing the README: {e}", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    """Main function to parse arguments and generate README."""
    parser = argparse.ArgumentParser(
        description="Generate a README.md from directory contents.\n\n"
                   "For more details, visit: https://hub.docker.com/r/readmeai/readmeai",
        formatter_class=argparse.RawTextHelpFormatter # For better help text formatting
    )
    parser.add_argument(
        "path",
        type=str,
        help="Path to the directory to analyze."
    )
    parser.add_argument(
        "--dirs-to-ignore",
        type=str,
        help="Comma-separated list of directory names to skip (e.g., '.git,node_modules,venv')."
    )
    parser.add_argument(
        "--files-to-ignore",
        type=str,
        help="Comma-separated list of file names to skip (e.g., 'package-lock.json,.DS_Store')."
    )
    parser.add_argument(
        "--additional-context",
        type=str,
        help="Additional textual context about the project to provide to the AI."
    )
    parser.add_argument(
        "--readme-filename",
        default=DEFAULT_README_FILENAME,
        type=str,
        help=f"Name of the README file to generate (default: {DEFAULT_README_FILENAME})."
    )
    parser.add_argument(
        "--api",
        type=str,
        choices=["gemini", "openai", "anthropic"],
        help="AI API to use for generating the README."
    )
    parser.add_argument(
        "--ai-model",
        type=str,
        help=f"AI model to use."
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key for the selected AI service. Overrides API_KEY environment variable."
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 1.0.0" # Simple versioning
    )

    args = parser.parse_args()

    api_key = get_api_key(args)
    if not api_key:
        print(
            "❌ Error: No API key found. Please provide an API key using one of these methods:\n"
            "1. Command line argument: --api-key YOUR_API_KEY\n"
            "2. Environment variable: export API_KEY='YOUR_API_KEY'\n\n"
            "To get an API key, visit the respective service's website.\n\n"
            "For more information, visit: https://hub.docker.com/r/readmeai/readmeai",
            file=sys.stderr
        )
        sys.exit(1)

    if args.api == "gemini":
        try:
            genai.configure(api_key=api_key)
        except Exception as e:
            print(f"❌ Error: Failed to configure Gemini API: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.api == "anthropic":
        try:
            anthropic_client = anthropic.Anthropic(api_key=api_key)
        except Exception as e:
            print(f"❌ Error: Failed to configure Anthropic API: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.api in ["openai", "anthropic"]:
        print(f"❌ Error: {args.api} API support is not implemented yet.", file=sys.stderr)
        sys.exit(1)

    target_path = Path(args.path)

    # Process ignore lists from comma-separated strings to lists
    dirs_to_ignore_list: Optional[List[str]] = args.dirs_to_ignore.split(',') if args.dirs_to_ignore else None
    files_to_ignore_list: Optional[List[str]] = args.files_to_ignore.split(',') if args.files_to_ignore else None

    try:
        repository_content: str = read_files_from_folder(
            target_path,
            dirs_to_ignore_list,
            files_to_ignore_list
        )
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e: # Catch other potential errors from read_files_from_folder
        print(f"❌ An unexpected error occurred while reading files: {e}", file=sys.stderr)
        sys.exit(1)

    prompt = GENERATION_PROMPT_TEMPLATE.format(repository_content=repository_content)

    if args.additional_context:
        prompt += f"\n\nAdditional Context Provided by User:\n{args.additional_context}"

    print(f"\n🤖 Attempting to generate README using {args.api} model: {args.ai_model}...")
    try:
        if args.api == "gemini":
            model = genai.GenerativeModel(args.ai_model)
            response = model.generate_content(prompt)
            generated_text = response.text
        elif args.api == "anthropic":
            response = anthropic_client.messages.create(
                model=args.ai_model,
                messages=[{"role": "user", "content": prompt}]
            )
            generated_text = response.content[0].text
        else:
            print(f"❌ Error: {args.api} API support is not implemented yet.", file=sys.stderr)
            sys.exit(1)
    except AttributeError: # Handle cases where response.text might not be directly available
        try:
            # For some complex responses, text might be within parts
            generated_text = "".join(part.text for part in response.parts)
        except Exception: # If still failing, log the response structure
            print(f"❌ Error: Could not extract text from {args.api} response. Response object: {response}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {args.api} content generation failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not generated_text.strip():
        print("❌ Error: The AI returned an empty response. Cannot generate README.", file=sys.stderr)
        sys.exit(1)

    write_readme(generated_text, target_path, args.readme_filename)
    print("\n🎉 README generation process complete!")

if __name__ == "__main__":
    # For making it open source, consider adding these files to your repository:
    # - requirements.txt (listing dependencies like google-generativeai)
    # - LICENSE (e.g., MIT, Apache 2.0)
    # - .gitignore (to ignore venv, __pycache__, etc.)
    # - A README.md for this script itself, explaining how to install and use it.
    # - CONTRIBUTING.md (if you want contributions)
    # - Optionally, set up pre-commit hooks for formatting (e.g., black, ruff) and linting.
    main()