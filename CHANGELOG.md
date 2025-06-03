# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.0] - 2025-05-30

### Added
- Initial release of readmeai
- Support for multiple AI providers (OpenAI, Anthropic, Google Gemini)
- Command-line interface with various options
- File filtering capabilities
- Configuration management
- Docker support
- Comprehensive documentation
- Examples and usage guides

### Features
- Multi-AI support with OpenAI, Anthropic, and Google Gemini
- Smart file analysis with intelligent filtering
- Highly configurable settings
- Built-in retry mechanism for API reliability
- Docker containerization
- Configuration management for API keys and defaults
- Model discovery functionality
- Security-first approach with API key validation

### Technical Details
- Python 3.10+ compatibility
- Dependencies:
  - google-generativeai==0.8.5
  - anthropic==0.52.1
  - openai==1.82.1
- Comprehensive input validation
- Detailed error handling
- Extensive logging 