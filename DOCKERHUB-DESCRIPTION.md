# README.ai - AI-Powered README Generator (Multi-Provider)

**Automatically generate comprehensive `README.md` files for your projects using your choice of AI: Google Gemini, OpenAI, or Anthropic!**

This Docker image (`readmeai/readmeai`) provides a versatile Python command-line tool that analyzes your codebase and intelligently crafts detailed, well-structured `README.md` files.

**Project & Source:** [https://github.com/varunelavia/readmeai](https://github.com/varunelavia/readmeai)

### Key Features

* **Multi-AI Provider Support:** Generate READMEs using:
    * Google Gemini
    * OpenAI (GPT models)
    * Anthropic (Claude models)
* **Smart Code Analysis:** Reads your project files to understand purpose, language, frameworks, and key functionalities.
* **Configuration System:**
    * Save API keys and default preferences (`~/.readmeai/config.json` within the container).
    * Manage settings using the `configure` command.
* **Advanced File Filtering:**
    * Comprehensive default ignore lists for common project files/directories.
    * Customize ignored/allowed directories, files, and extensions.
* **CLI Subcommands:**
    * `generate`: Main command to create READMEs.
    * `configure`: Set up API keys and default API/model.
    * `list-models`: Discover available models for your configured API.
* **Retry Mechanism:** Built-in retries for more reliable API interactions.
* **README Backup:** Automatically backs up existing README files before overwriting.
* **Easy to Use:** Packaged in a Docker container for a consistent environment.

---

### Quick Start with Docker

1. **Pull the Image:**
    ```bash
    docker pull readmeai/readmeai:latest 
    # Or specify a version, e.g., readmeai/readmeai:1.0.0
    ```

2. **Basic Generation (using Environment Variable for API Key):**
    This example uses Gemini. Replace `--api gemini` and the `API_KEY` with your chosen provider and key.

    ```bash
    docker run --rm \
      --user "$(id -u):$(id -g)" \
      -v "/path/to/your/project:/app/project" \
      -e API_KEY="YOUR_CHOSEN_PROVIDER_API_KEY" \
      readmeai/readmeai \
      generate \
      --api gemini \
      --ai-model "gemini-1.5-flash" \
      "/app/project"
    ```

    **Explanation of common Docker flags:**
    * `--rm`: Automatically removes the container when it exits.
    * `--user "$(id -u):$(id -g)"`: Runs the container process with your host user's ID and group ID. Crucial to avoid permission errors when writing the README to your mounted volume.
    * `-v "/path/to/your/project:/app/project"`: Mounts your local project directory to `/app/project` inside the container. The generated README is saved here.
    * `-e API_KEY="YOUR_..."`: Sets the generic `API_KEY` environment variable. The tool uses this key for the provider specified by the `--api` flag.

---

### CLI Usage via Docker

The tool uses subcommands: `generate`, `configure`, `list-models`.

#### 1. `generate` - Create a README

```bash
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "/path/to/your/project:/app/project" \
  -e API_KEY="YOUR_PROVIDER_API_KEY" \
  readmeai/readmeai \
  generate \
  --api <gemini|openai|anthropic> \
  --ai-model "<model_name>" \
  "/app/project" \
  [generate_options...]
```

**Generate Options:**
* `path`: (Required) Path to the directory to analyze (e.g., "/app/project" inside container).
* `--api <gemini|openai|anthropic>`: (Required if not configured) Specify the AI provider.
* `--ai-model <model_name>`: (Required if not configured) Specify the model from the chosen provider. Use list-models to see available models.
* `--api-key <key_string>`: Provide API key directly (overrides API_KEY env var and config).
* `--readme-filename <name.md>`: Output filename (default: README.md).
* `--additional-context <text>`: Provide extra context to the AI.
* `--dirs-to-ignore <dir1,dir2>`: Comma-separated directories to ignore.
* `--files-to-ignore <file1,file2>`: Comma-separated files to ignore.
* `--extensions-to-ignore <ext1,ext2>`: Comma-separated file extensions to ignore (no dots).
* `--extensions-to-allow <ext1,ext2>`: Comma-separated file extensions to explicitly process.
* `--max-retries <N>`: (Default: 3) Max API call retries.
* `--retry-delay <N>`: (Default: 2) Seconds between retries.
* `--max-tokens <N>`: (Default: 2048) Max tokens for generation.
* `--debug`: Enable debug logging.

#### 2. `configure` - Set API Keys & Defaults

This command saves settings to `~/.readmeai/config.json` inside the container. For persistence across Docker runs, you'd need to mount a volume for this config directory (see Advanced Configuration).

```bash
# Example: Configure default API and API key
docker run --rm -it \
  --user "$(id -u):$(id -g)" \
  # For persistent config, add: -v "$HOME/.your_local_config_for_readmeai:/root/.readmeai" 
  # (Note: path inside container might be /root/.readmeai or /home/user/.readmeai depending on base image and --user flag behavior)
  readmeai/readmeai \
  configure --default-api openai --api-key "sk-YOUR_OPENAI_KEY" --default-model "gpt-3.5-turbo"
```

**Configure Options:**
* `--api-key <key_string>`: API key to save for the default (or specified) API.
* `--default-api <gemini|openai|anthropic>`: Set the default AI provider.
* `--default-model <model_name>`: Set the default model for the default API.

#### 3. `list-models` - Discover Available Models

```bash
docker run --rm \
  -e API_KEY="YOUR_PROVIDER_API_KEY" \
  readmeai/readmeai \
  list-models --api <gemini|openai|anthropic>
  # --api-key "YOUR_PROVIDER_API_KEY" # Alternative way to pass key
```

**List-models Options:**
* `--api <gemini|openai|anthropic>`: (Required) Provider to list models for.
* `--api-key <key_string>`: API key if not set via environment or config.

### API Key Management

API keys are sourced in the following order of priority:

1. Command-line argument: `--api-key` flag for generate or list-models.
2. Environment Variable: `API_KEY` set when running the Docker container (`-e API_KEY="YOUR_KEY"`). The `--api` flag tells the tool which provider this key is for.
3. Configuration File: (`~/.readmeai/config.json` inside the container, managed by the configure command).

For Docker usage, setting the `API_KEY` environment variable along with the `--api` flag during generate or list-models is often the most straightforward approach.

### Persistent Configuration (Advanced Docker Usage)

The `readmeai configure` command saves to `~/.readmeai/config.json` inside the container. By default, this configuration is lost when the container stops. To make it persistent:

1. Create a directory on your host to store the configuration:
    ```bash
    mkdir -p "$HOME/.config/readmeai_docker_config"
    ```

2. Mount this directory when running readmeai configure or any command that needs to read the config:
    ```bash
    docker run --rm -it \
      --user "$(id -u):$(id -g)" \
      -v "$HOME/.config/readmeai_docker_config:/home/readmeai_user/.readmeai" \
      readmeai/readmeai \
      configure --default-api gemini --api-key "YOUR_GEMINI_KEY"
    ```

> **Note:** Correctly mapping `~` for dynamic UIDs in Docker can be tricky. Test the target path (`/root/.readmeai` or a path corresponding to the dynamic user's potential home) for your specific base image.

### Important: AI Provider Usage, Quotas & Billing

This tool uses third-party AI APIs. Your usage is subject to the respective provider's policies, quotas, and pricing.

* **API Keys:** Obtain API keys directly from Google AI Studio (for Gemini), OpenAI Platform or Anthropic Console.
* **Billing:** For sustained or heavy use, ensure you have a valid billing method associated with your AI provider accounts. Free tiers often have strict rate limits.
* **Error Handling:** If you encounter errors related to quotas or API limits, please check your account status and usage dashboards on the respective AI provider's platform.

### Useful Links & References

* **Project Repository:** [https://github.com/varunelavia/readmeai](https://github.com/varunelavia/readmeai)
* **Google Gemini:**
    * [Pricing](https://ai.google.dev/pricing)
    * [Quotas](https://ai.google.dev/gemini-api/docs/rate-limits)
* **OpenAI:**
    * [Pricing](https://openai.com/pricing)
    * [Rate Limits](https://platform.openai.com/docs/guides/rate-limits)
* **Anthropic Claude:**
    * [Pricing](https://www.anthropic.com/pricing)
    * [Rate Limits](https://docs.anthropic.com/claude/reference/rate-limits)

### Feedback & Contact

We value your feedback and are here to help! If you:

* Have suggestions for improvements
* Found a bug or issue
* Need help with configuration
* Want to contribute to the project
* Have questions about usage

Please reach out to us at [readmeai@proton.me](mailto:readmeai@proton.me) or open an issue on our [GitHub repository](https://github.com/varunelavia/readmeai/issues).

Your feedback helps us make README.ai better for everyone! 