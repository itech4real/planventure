# Contributing to PlanVenture

Thank you for your interest in contributing to PlanVenture! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please read and follow our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) in all interactions.

## Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/yourusername/planventure.git
cd planventure
```

### 2. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/add-trip-sharing` for new features
- `fix/auth-token-bug` for bug fixes
- `docs/update-readme` for documentation
- `test/add-endpoint-tests` for tests

### 3. Set Up Development Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
cd planventure-api
pip install -r requirements.txt
```

### 4. Create Local .env
```bash
cp .env.example .env
```

Configure for development (defaults are fine for local testing).

## Development Workflow

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_endpoints.py -v

# Run with coverage
pytest --cov=. --cov-report=html

# Run tests in watch mode
pytest-watch tests/
```

### Code Quality

#### Linting
```bash
pip install flake8 pylint
flake8 planventure-api/
pylint planventure-api/
```

#### Code Formatting
```bash
pip install black autopep8
black planventure-api/
autopep8 --in-place --aggressive planventure-api/**/*.py
```

#### Type Checking
```bash
pip install mypy
mypy planventure-api/
```

### Running the Server
```bash
cd planventure-api
python app.py
```

Server runs at: http://localhost:5000

### Testing Endpoints
Use Bruno API Client (included in repo) or curl:
```bash
curl -X GET http://localhost:5000/health
```

## Commit Guidelines

### Commit Message Format
```
[TYPE] Brief description

Detailed explanation if needed. Keep lines under 72 characters.

Fixes #issue_number
```

### Types
- `feat` - New feature
- `fix` - Bug fix
- `test` - Adding/updating tests
- `docs` - Documentation changes
- `refactor` - Code refactoring without functionality change
- `style` - Code style changes (formatting, missing semicolons, etc)
- `chore` - Build process, dependencies, tooling

### Examples
```
feat: Add trip sharing functionality

Allow users to share trip plans with other users.
Implements new endpoint POST /trips/{id}/share
Adds sharing permission model and validation

test: Increase endpoint test coverage to 90%

Added tests for all authentication endpoints
Coverage increased from 78% to 90%

fix: Correct JWT token expiration bug

JWT refresh tokens now properly expire after 30 days
Previously had no expiration limit
Fixes #234
```

## Pull Request Guidelines

### Before Submitting PR
- [ ] Tests pass: `pytest tests/ -v`
- [ ] Coverage maintained: `pytest --cov=.`
- [ ] Code formatted: `black` and `autopep8`
- [ ] Linting passes: `flake8`
- [ ] Commit messages follow guidelines
- [ ] Branch is up-to-date with main

### PR Title Format
```
[CATEGORY] Short description

Examples:
[Feature] Add trip sharing functionality
[Fix] Correct JWT token expiration
[Test] Increase endpoint coverage
[Docs] Update API documentation
```

### PR Description Template
```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Fixes #(issue number)

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
```

## Coding Standards

### Python Style Guide
Follow PEP 8:
```python
# Good
def create_trip(user_id: int, title: str) -> Trip:
    """Create a new trip for a user.
    
    Args:
        user_id: ID of the user
        title: Title of the trip
    
    Returns:
        The created Trip object
    """
    trip = Trip(user_id=user_id, title=title)
    db.session.add(trip)
    db.session.commit()
    return trip

# Bad
def createTrip(userId,title):
    trip=Trip(user_id=userId,title=title)
    db.session.add(trip)
    db.session.commit()
    return trip
```

### Naming Conventions
- **Functions/Methods**: `lowercase_with_underscores`
- **Classes**: `PascalCase`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Private**: `_leading_underscore`

### Documentation
- Add docstrings to all functions/classes
- Use Google-style docstrings
- Update README.md if adding new features

### Error Handling
```python
# Good
try:
    result = operation()
except ValueError as e:
    logger.error(f"Invalid value: {str(e)}")
    return jsonify({"error": "Invalid input"}), 400

# Bad
try:
    result = operation()
except:
    pass
```

## Adding New Features

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature
```

### 2. Implement Feature
- Add model if needed
- Add endpoint(s) if needed
- Add validation
- Add error handling

### 3. Add Tests
```python
# tests/test_your_feature.py
def test_your_feature():
    """Test description."""
    # Arrange
    
    # Act
    
    # Assert
```

### 4. Update Documentation
- Add to README.md API section
- Update DEPLOYMENT.md if applicable
- Add comments in code

### 5. Test Thoroughly
```bash
pytest tests/ -v --cov=.
```

## Adding Bug Fixes

### 1. Create Issue
Report the bug with:
- Description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment info

### 2. Create Fix Branch
```bash
git checkout -b fix/bug-description
```

### 3. Fix & Test
- Write test that reproduces bug
- Fix the bug
- Verify test passes

### 4. Submit PR
Reference the issue in your PR

## Database Changes

### Adding Migrations
If you modify models:
```bash
# Generate migration (manual for now, Flask-Migrate coming soon)
# Document changes in scripts/migrations/

# Test migration
python scripts/create_db.py reset
python scripts/seed_db.py
```

## Documentation

### README.md
Update with:
- New features
- New dependencies
- Configuration changes
- Breaking changes

### Code Comments
```python
# Bad
x = x + 1  # increment x

# Good  
user_count = user_count + 1  # increment active user count for batch processing
```

## Review Process

### What Reviewers Look For
- ✓ Code quality and style
- ✓ Test coverage
- ✓ Documentation
- ✓ Performance impact
- ✓ Security concerns
- ✓ Backward compatibility

### Addressing Feedback
- Respond to all comments
- Make requested changes
- Re-request review
- Don't dismiss feedback

## Release Process

### Version Numbering
Use Semantic Versioning: `MAJOR.MINOR.PATCH`
- `1.0.0` - Major release (breaking changes)
- `1.1.0` - Minor release (new features)
- `1.0.1` - Patch release (bug fixes)

## Community

### Getting Help
- GitHub Issues - Report bugs or request features
- Discussions - Ask questions and discuss ideas
- Discord - Real-time chat (link in README)

### Code Review Etiquette
- Be respectful and constructive
- Ask questions, don't make accusations
- Acknowledge good work
- Admit mistakes gracefully

## Resources

- [Python PEP 8 Style Guide](https://pep8.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Git Commit Best Practices](https://chris.beams.io/posts/git-commit/)

## Questions?

Feel free to:
- Open an issue with tag `[question]`
- Check SUPPORT.md for more help
- Contact maintainers

Thank you for contributing to PlanVenture! 🎉
