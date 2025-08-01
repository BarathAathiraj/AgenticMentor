# 🤝 Contributing to Agentic Mentor

Thank you for your interest in contributing to Agentic Mentor! This guide will help you get started with the development process.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- API keys for your preferred LLM provider

### Development Setup

1. **Fork the repository**
   ```bash
   # Go to GitHub and fork the repository
   # Then clone your fork
   git clone https://github.com/yourusername/agentic-mentor.git
   cd agentic-mentor
   ```

2. **Set up your environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure your environment**
   ```bash
   # Copy environment template
   cp env.example .env
   
   # Edit .env with your API keys
   # At minimum, set one LLM provider:
   # GEMINI_API_KEY=your_key
   # or
   # OPENAI_API_KEY=your_key
   ```

4. **Test your setup**
   ```bash
   # Start the server
   python run_server.py
   
   # Open http://localhost:3000 in your browser
   ```

## 🔄 Development Workflow

### 1. Create a Feature Branch
```bash
# Make sure you're on main and up to date
git checkout main
git pull origin main

# Create a new feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Write your code
- Add tests if applicable
- Update documentation
- Follow the coding standards below

### 3. Test Your Changes
```bash
# Run the server
python run_server.py

# Test your changes
# Make sure the application works as expected
```

### 4. Commit Your Changes
```bash
# Add your changes
git add .

# Commit with a descriptive message
git commit -m "Add: brief description of your changes

- Detailed description of what you added
- Any important notes for reviewers
- Related issue numbers if applicable"
```

### 5. Push and Create Pull Request
```bash
# Push your branch
git push origin feature/your-feature-name

# Go to GitHub and create a Pull Request
```

## 📝 Coding Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small

### Example Code Structure
```python
from typing import Dict, Any, Optional
from loguru import logger

class YourClass:
    """Brief description of what this class does."""
    
    def __init__(self, param: str):
        """Initialize the class.
        
        Args:
            param: Description of the parameter
        """
        self.param = param
        self.logger = logger.bind(component="your_component")
    
    async def your_method(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Brief description of what this method does.
        
        Args:
            input_data: Description of input data
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: When input is invalid
        """
        try:
            # Your implementation here
            result = await self._process_data(input_data)
            self.logger.info("Successfully processed data")
            return result
        except Exception as e:
            self.logger.error(f"Error processing data: {e}")
            raise
```

### Commit Message Format
Use conventional commit format:
```
type(scope): description

- type: feat, fix, docs, style, refactor, test, chore
- scope: optional, the part of the codebase affected
- description: brief description in present tense

Examples:
- feat(agents): add new reflection agent
- fix(search): resolve JSON parsing issues
- docs(readme): update installation instructions
- style(qa_agent): improve code formatting
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/

# Run specific test file
python -m pytest tests/test_agents.py

# Run with verbose output
python -m pytest -v tests/
```

### Writing Tests
- Create test files in the `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test names
- Test both success and failure cases

Example test:
```python
import pytest
from src.agents.qa_agent import QAAgent

class TestQAAgent:
    """Test cases for Q&A Agent."""
    
    @pytest.fixture
    def qa_agent(self):
        """Create a Q&A agent for testing."""
        # Setup your test agent
        return QAAgent(vector_store, search_engine)
    
    async def test_process_query_success(self, qa_agent):
        """Test successful query processing."""
        input_data = {"query_text": "What is Agentic Mentor?"}
        result = await qa_agent.process(input_data)
        
        assert result is not None
        assert "response" in result
        assert result["response"].response_text is not None
    
    async def test_process_query_empty_input(self, qa_agent):
        """Test query processing with empty input."""
        with pytest.raises(ValueError):
            await qa_agent.process({})
```

## 📚 Documentation

### Code Documentation
- Write clear docstrings for all functions and classes
- Include type hints
- Document complex algorithms
- Add comments for non-obvious code

### README Updates
- Update README.md when adding new features
- Include usage examples
- Update installation instructions if needed

### API Documentation
- Document new API endpoints
- Include request/response examples
- Update API documentation in README

## 🔍 Code Review Process

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation is updated
- [ ] No sensitive data is committed
- [ ] Branch is up to date with main

### Pull Request Guidelines
- Provide a clear description of changes
- Include screenshots for UI changes
- Link related issues
- Request reviews from teammates
- Respond to review comments promptly

### Review Checklist
- [ ] Code is readable and well-structured
- [ ] Tests are comprehensive
- [ ] Documentation is clear
- [ ] No security issues
- [ ] Performance considerations addressed

## 🐛 Bug Reports

### Reporting Bugs
1. Check existing issues first
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots if applicable

### Bug Fix Process
1. Create a branch for the fix
2. Write a test that reproduces the bug
3. Fix the bug
4. Ensure all tests pass
5. Submit pull request

## ✨ Feature Requests

### Suggesting Features
1. Check existing issues and discussions
2. Create a feature request issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Implementation suggestions if possible
   - Priority level

### Implementing Features
1. Discuss the feature with the team
2. Create a design document if needed
3. Implement the feature
4. Add tests and documentation
5. Submit pull request

## 🚀 Deployment

### Testing Before Deployment
```bash
# Run all tests
python -m pytest tests/

# Test the application locally
python run_server.py

# Check for any linting issues
# (Add linting tools as needed)
```

### Deployment Checklist
- [ ] All tests pass
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Database migrations if needed
- [ ] Performance tested

## 🤝 Team Collaboration

### Communication
- Use GitHub Issues for discussions
- Tag teammates for reviews
- Use descriptive branch names
- Keep commits atomic and focused

### Code Ownership
- Take ownership of your code
- Respond to review comments
- Help review others' code
- Share knowledge with the team

### Best Practices
- Write self-documenting code
- Add comments for complex logic
- Use meaningful variable names
- Keep functions small and focused
- Test your changes thoroughly

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and discussions
- **Team Chat**: For quick questions and coordination
- **Documentation**: Check README and code comments

## 🙏 Thank You

Thank you for contributing to Agentic Mentor! Your contributions help make this project better for everyone.

---

**Happy Coding! 🚀** 