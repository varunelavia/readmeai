# Contributing to readmeai

Thank you for your interest in contributing to readmeai! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### 1. Fork and Clone

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/readmeai.git
   cd readmeai
   ```

### 2. Set Up Development Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

### 3. Make Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
3. Run tests:
   ```bash
   pytest
   ```

4. Ensure code style:
   ```bash
   black .
   flake8
   ```

### 4. Commit Changes

1. Stage your changes:
   ```bash
   git add .
   ```

2. Commit with a descriptive message:
   ```bash
   git commit -m "Description of changes"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

### 5. Create Pull Request

1. Go to the original repository
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR template
5. Submit the PR

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions
- Keep functions focused and small
- Write meaningful commit messages

### Testing

- Write tests for new features
- Ensure all tests pass
- Maintain or improve test coverage
- Test edge cases

### Documentation

- Update README.md if needed
- Add docstrings for new functions
- Update EXAMPLES.md for new features
- Keep documentation clear and concise

## Pull Request Process

1. Update documentation
2. Add tests if needed
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Questions?

Feel free to open an issue for any questions or concerns. 