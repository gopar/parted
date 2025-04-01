# Code Conventions

- Follow Domain Driven Development
- Add tests to verify work

## Code Style and Formatting

### Python
- Use type hints for all function/method arguments and return types
- Follow the HackSoft Django style guide patterns:
  - Use explicit service and selector layers
  - Prefer DTO (Data Transfer Objects) over class attributes when passing data around
  - Use atomic transactions for data modifications
  - Only use CBV that inherit from `View`, `TemplateView` or `RedirectView`
  - Keep thin Models/Views/Templates but fat services

### HTML/CSS/JS
- Use 2 spaces for indentation
- Use Tailwind + DaisyUI for the styling
- HTMX best practices

Related docs:
- https://v3.tailwindcss.com/docs/
- https://daisyui.com/docs/intro/

## Project Structure

### Backend (Django)
- Organize code using Django's app structure
- Follow HackSoft's layered architecture:
  - `models.py` for database models
  - `views.py` for API endpoints
  - `serializers.py` for data serialization
  - `services/` directory for business logic with atomic transactions
  - `selectors/` directory for database queries
  - `migrations/` for database schema changes
  - `helpers.py` for utility functions

## Template Design

- Use HTMX best practices along side django template best practices
- Validate input data
- Use atomic transactions for database operations
- Follow the HackSoftware Django Styleguide equivalent for templates

## Authentication

- Use session based authentication
- Will be using django-allauth as the authentication library

## Error Handling

- Use try/catch blocks for async operations
- Display user-friendly error messages
- Log errors to console for debugging
- Validate form inputs and show field-specific errors

## Testing

- Write unit tests for backend code
- Use pytest for Python testing
- Include test fixtures for common test data
- Mock external services in tests

## Documentation

- Include docstrings for Python classes and functions
- Document API endpoints with clear input/output specifications
- Add comments for complex logic
- Keep README.md updated with setup and development instructions
- Type hint all function parameters and return values

## Security Practices

- Store sensitive configuration in environment variables
- Use HTTPS for all API requests
- Implement proper authentication and authorization
- Sanitize user inputs to prevent injection attacks
