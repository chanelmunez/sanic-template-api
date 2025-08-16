# Contributing Guide

Thank you for your interest in contributing to the Sanic + Next.js Template! This guide will help you get started.

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- Git

### Setup Development Environment

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/sanic-template-api.git
   cd sanic-template-api
   ```
3. **Run setup script**
   ```bash
   ./dev-setup.sh
   ```

## 🔧 Development Workflow

### Frontend Development

```bash
# Start Next.js development server
npm run dev

# Run linting
npm run lint

# Build for production
npm run build
```

### Backend Development

```bash
# Start Sanic development server
npm run python-dev

# Or manually:
cd api
source venv/bin/activate
python -m uvicorn main:app --reload --port 8000
```

### Testing

```bash
# Frontend tests
npm test

# Backend tests (add tests in api/tests/)
cd api
python -m pytest
```

## 📝 Code Standards

### TypeScript/JavaScript

- Use TypeScript for all new code
- Follow ESLint configuration
- Use Prettier for formatting
- Prefer functional components with hooks
- Use proper TypeScript types

```typescript
// ✅ Good
interface User {
  id: number;
  name: string;
  email: string;
}

const UserCard = ({ user }: { user: User }) => {
  return <div>{user.name}</div>;
};

// ❌ Avoid
const UserCard = ({ user }: any) => {
  return <div>{user.name}</div>;
};
```

### Python

- Follow PEP 8 style guide
- Use type hints
- Use Pydantic models for validation
- Write docstrings for functions and classes

```python
# ✅ Good
from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str

async def get_users() -> List[User]:
    """Get all users from the database."""
    return db.find_all('users')

# ❌ Avoid
def get_users():
    return db.find_all('users')
```

## 🎯 Contributing Areas

### High Priority
- [ ] Database integration (PostgreSQL, MongoDB)
- [ ] Authentication system
- [ ] API rate limiting
- [ ] Unit and integration tests
- [ ] Performance optimizations

### Medium Priority
- [ ] Admin dashboard
- [ ] File upload handling
- [ ] Email notifications
- [ ] Caching layer
- [ ] API documentation improvements

### Low Priority
- [ ] Dark mode theme
- [ ] Additional UI components
- [ ] Internationalization
- [ ] Advanced filtering

## 📋 Pull Request Process

### Before Submitting

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow code standards
   - Add tests if applicable
   - Update documentation

3. **Test your changes**
   ```bash
   # Frontend
   npm run lint
   npm run build

   # Backend
   cd api
   python -m pytest
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add user authentication"
   ```

### Commit Message Format

Use conventional commits:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Examples:
```bash
feat: add user authentication system
fix: resolve CORS issue in production
docs: update API documentation
style: format code with prettier
refactor: extract user service to separate module
test: add unit tests for user endpoints
chore: update dependencies
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🐛 Bug Reports

### Before Reporting
- Check existing issues
- Reproduce the bug
- Test on latest version

### Bug Report Template
```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to...
2. Click on...
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., macOS 12.0]
- Browser: [e.g., Chrome 95]
- Node.js: [e.g., 18.0.0]
- Python: [e.g., 3.9.0]

**Additional Context**
Screenshots, logs, etc.
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
Clear description of what you want

**Describe alternatives you've considered**
Alternative solutions or features

**Additional context**
Screenshots, mockups, etc.
```

## 📚 Documentation

### Areas Needing Documentation
- API endpoints
- Component usage
- Deployment guides
- Architecture decisions

### Documentation Standards
- Use clear, concise language
- Include code examples
- Add screenshots when helpful
- Keep examples up to date

## 🎨 Design Guidelines

### UI/UX Principles
- Mobile-first responsive design
- Accessibility (WCAG 2.1 AA)
- Consistent spacing and typography
- Clear visual hierarchy

### Component Guidelines
- Reusable and composable
- Well-documented props
- Consistent naming conventions
- TypeScript types included

## 🔒 Security

### Security Guidelines
- Never commit secrets or credentials
- Validate all user inputs
- Use HTTPS in production
- Implement proper error handling
- Follow OWASP guidelines

### Reporting Security Issues
Email security issues to: [security-email]
Do not create public issues for security vulnerabilities.

## 📞 Getting Help

### Communication Channels
- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and ideas
- Discord: Real-time chat (if available)

### Code Review Process
1. Maintainer review required
2. Automated checks must pass
3. At least one approval needed
4. Squash and merge preferred

## 🎉 Recognition

Contributors will be:
- Added to the contributors list
- Mentioned in release notes
- Invited to maintainer team (for significant contributions)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🚀
