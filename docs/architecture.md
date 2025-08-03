# WanderWise Architecture

WanderWise is built using **Clean Architecture** principles, ensuring separation of concerns, testability, and scalability. The project is structured into distinct layers:

## Layers

- **Domain Layer**: Core business logic, entities, and use case contracts. Independent of frameworks or external systems.
- **Application Layer**: Implements use cases, orchestrates domain logic, and coordinates between domain and adapters.
- **Adapters Layer**: Bridges between application/domain and external services (e.g., OpenAI API, web frameworks).
- **Infrastructure Layer**: System-level concerns like logging, environment config, and external integrations.
- **Presentation Layer**: FastAPI endpoints, Jinja2 templates, static assets, and HTMX for dynamic UI.

## Technology Stack

- **Backend**: Python 3.11, FastAPI
- **Frontend**: Jinja2 (server-side templates), HTMX (dynamic UI), Tailwind CSS (utility-first styling)
- **AI Integration**: OpenAI GPT models (via adapters)
- **Containerization**: Docker (production & dev)
- **Other**: Pydantic, python-dotenv, robust logging

## Dependency Flow
- **Dependencies always point inward**: Outer layers (presentation, infrastructure) depend on inner layers (domain, application), never the reverse.
- **Adapters**: Implement interfaces defined in the domain/application layers, allowing easy swapping of implementations (e.g., mock LLM for tests).

## Rationale
- **Testability**: Business logic is decoupled from frameworks and infrastructure.
- **Maintainability**: Each layer has a single responsibility and clear boundaries.
- **Extensibility**: New features or integrations can be added with minimal impact on core logic.
