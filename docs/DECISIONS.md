# Beelzebub — Architecture Decision Log

**Project:** Beelzebub  
**Document:** Architecture Decision Log  
**Version:** 1.0  
**Status:** Initial Decisions  
**Purpose:** Record important technical and architectural decisions.

---

# 1. Introduction

This document records the significant architectural and technical decisions made during the development of Beelzebub.

Each decision includes:

- Context: Why the decision was necessary.
- Decision: What we selected.
- Alternatives: Other options considered.
- Consequences: Benefits and trade-offs.

Decisions may be revisited when new requirements or technical evidence justify a change.

---

# 2. ADR-001: Modular Monolithic Architecture

**Status:** Accepted

### Context

Beelzebub requires several interconnected business modules, including inventory, suppliers, purchasing, invoices, and AI orchestration.

A distributed microservice architecture would introduce unnecessary infrastructure and operational complexity during initial development.

### Decision

Use a modular monolithic architecture.

The application will have one primary FastAPI backend, one PostgreSQL database, and a React frontend.

Internal modules will have clearly defined responsibilities.

### Alternatives Considered

- Microservices.
- Serverless architecture.
- Traditional monolithic architecture without module boundaries.

### Consequences

Positive:
- Simpler development and deployment.
- Easier transaction management.
- Lower infrastructure costs.
- Clear internal separation.

Trade-off:
- Individual modules cannot be independently deployed initially.

---

# 3. ADR-002: FastAPI for Backend Development

**Status:** Accepted

### Context

The application requires typed APIs, asynchronous request handling where useful, input validation, and integration with Python-based AI tools.

### Decision

Use FastAPI with Pydantic.

### Alternatives Considered

- Django REST Framework.
- Flask.
- Litestar.

### Consequences

Positive:
- Python-native development.
- Automatic API documentation.
- Pydantic validation.
- Suitable for integrating AI workflows.

Trade-off:
- Authentication, authorization, and other application infrastructure must be explicitly implemented.

---

# 4. ADR-003: React, Vite, and TypeScript for Frontend

**Status:** Accepted

### Context

Beelzebub requires a responsive business dashboard and an interactive AI assistant.

### Decision

Use React, Vite, TypeScript, and Tailwind CSS.

### Alternatives Considered

- Next.js.
- Vue.js.
- Angular.

### Consequences

Positive:
- Flexible component architecture.
- Fast development server.
- Type safety.
- Large ecosystem.

Trade-off:
- API communication and frontend application state must be explicitly organized.

---

# 5. ADR-004: PostgreSQL as Primary Database

**Status:** Accepted

### Context

The application stores structured business information involving products, suppliers, invoices, purchase orders, and approvals.

Data integrity and transactional consistency are important.

### Decision

Use PostgreSQL as the primary relational database.

### Alternatives Considered

- MySQL.
- SQLite.
- MongoDB.

### Consequences

Positive:
- ACID transactions.
- Relational constraints.
- Strong indexing capabilities.
- JSONB support.
- Suitable for multi-business data isolation.

Trade-off:
- Requires database infrastructure and connection management.

---

# 6. ADR-005: SQLAlchemy as ORM

**Status:** Accepted

### Context

The backend requires maintainable database access and integration with PostgreSQL.

### Decision

Use SQLAlchemy 2.x with typed ORM models.

### Alternatives Considered

- SQLModel.
- Django ORM.
- Direct SQL using psycopg.

### Consequences

Positive:
- Explicit database relationships.
- Transaction management.
- Typed model definitions.
- Flexible query construction.

Trade-off:
- Requires understanding session lifecycle and ORM behavior.

---

# 7. ADR-006: Alembic for Database Migrations

**Status:** Accepted

### Context

The database schema will evolve throughout development.

Manually recreating database tables is not a reliable approach.

### Decision

Use Alembic for version-controlled database migrations.

### Alternatives Considered

- Manual SQL scripts.
- ORM metadata table creation without migrations.

### Consequences

Positive:
- Reproducible schema changes.
- Version-controlled database evolution.
- Controlled deployment migrations.

Trade-off:
- Migrations require review and testing.

---

# 8. ADR-007: LangGraph for Agent Orchestration

**Status:** Accepted for planned agent implementation

### Context

Beelzebub requires stateful workflows involving multiple tool calls, approval interruptions, recovery, and controlled execution.

A simple LLM request-response loop would not provide sufficient workflow control.

### Decision

Use LangGraph for central agent orchestration.

Initially, use one orchestrator with specialized validated tools.

### Alternatives Considered

- Direct LLM function calling.
- LangChain agents without a dedicated stateful workflow.
- CrewAI.
- AutoGen.
- Custom orchestration using ordinary Python functions.

### Consequences

Positive:
- Explicit workflow graphs.
- Stateful execution.
- Human-in-the-loop interruptions.
- Checkpointing and recovery support.

Trade-off:
- Additional orchestration complexity.
- Checkpoint persistence and recovery must be implemented and tested correctly.

LangGraph will not replace application-level authorization, approval validation, or database transactions.

---

# 9. ADR-008: Deterministic Business Logic

**Status:** Accepted

### Context

Inventory quantities, supplier prices, reorder calculations, and invoice balances must be accurate.

LLMs can produce incorrect arithmetic or invent business facts.

### Decision

All authoritative business calculations will use validated deterministic Python functions.

The LLM will interpret requests, coordinate tools, and explain results.

### Alternatives Considered

- Allowing the LLM to calculate business values directly.
- Generating SQL through the LLM.
- Combining model-generated calculations with database updates.

### Consequences

Positive:
- Reproducible calculations.
- Easier testing.
- Reduced hallucination risk.
- Clear separation of responsibilities.

Trade-off:
- Business rules must be explicitly implemented and maintained.

---

# 10. ADR-009: Human-Controlled Approval

**Status:** Accepted

### Context

Purchase orders and external business actions can have financial consequences.

The AI agent must not independently authorize consequential actions.

### Decision

All purchase order approvals must be performed by authorized human users through backend-controlled approval services.

Approvals must reference the exact version of the proposed action.

### Alternatives Considered

- Fully autonomous purchasing.
- Approval based solely on LLM decisions.
- Unrestricted execution of agent-generated actions.

### Consequences

Positive:
- Human oversight.
- Traceable decisions.
- Reduced risk of unauthorized purchasing.
- Stronger operational accountability.

Trade-off:
- Some workflows require additional human interaction.

---

# 11. ADR-010: pytest for Automated Testing

**Status:** Accepted

### Context

Business calculations, API behavior, database operations, and agent workflows require repeatable verification.

### Decision

Use pytest as the primary backend testing framework.

Add API integration tests and agent workflow evaluation as the application develops.

### Alternatives Considered

- unittest.
- Manual testing only.

### Consequences

Positive:
- Automated regression testing.
- Reproducible results.
- Convenient fixtures and parametrization.

Trade-off:
- Test infrastructure must be maintained alongside application code.

---

# 12. ADR-011: Python 3.12 for Initial Development

**Status:** Accepted, subject to dependency compatibility verification

### Context

The development machine has Python 3.14, 3.12, and 3.10 installed.

We need a predictable environment for the backend and AI ecosystem.

### Decision

Use Python 3.12 in a dedicated virtual environment initially.

Do not modify or uninstall other Python installations.

### Alternatives Considered

- Python 3.14.
- Python 3.10.

### Consequences

Positive:
- Isolated dependencies.
- Mature package compatibility.
- Reproducible local development.

Trade-off:
- Requires maintaining a separate Python environment.

The final supported dependency versions will be verified during installation.

---

# 13. ADR-012: Business-Level Multi-Tenancy

**Status:** Accepted

### Context

Beelzebub may eventually support multiple businesses.

Business records must remain isolated.

### Decision

Include business ownership in all relevant business records and enforce authorization in the backend.

Use appropriate database constraints to prevent cross-business relationships.

Evaluate PostgreSQL Row-Level Security as an additional security layer.

### Alternatives Considered

- One database per business.
- One schema per business.
- Shared database without explicit business ownership.

### Consequences

Positive:
- Easier multi-business expansion.
- Centralized database management.
- Consistent business-level authorization.

Trade-off:
- Every relevant query must enforce business ownership correctly.

---

# 14. General Decision-Making Rules

Future architectural decisions must follow these principles:

1. Prefer simple solutions that satisfy actual requirements.
2. Avoid introducing infrastructure without a demonstrated need.
3. Prioritize data integrity and security.
4. Keep business logic independent of the LLM.
5. Prefer established libraries with appropriate documentation and support.
6. Test important assumptions before adopting new technologies.
7. Document significant changes.
8. Revisit decisions when implementation evidence justifies doing so.

---

# 15. Decision Review Process

A decision may be:

- Proposed.
- Accepted.
- Rejected.
- Deprecated.
- Superseded.

When a decision changes, its original record should be preserved.

A new decision should explain:

- Why the previous approach is insufficient.
- What new approach is selected.
- What migration or implementation changes are required.

---

# 16. Current Technical Decisions Summary

| Area | Selected Technology |
|---|---|
| Frontend | React |
| Build tool | Vite |
| Frontend language | TypeScript |
| Styling | Tailwind CSS |
| Backend | FastAPI |
| Backend language | Python 3.12 |
| Validation | Pydantic |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Migrations | Alembic |
| Agent orchestration | LangGraph |
| Testing | pytest |
| Containerization | Docker |
| Version control | Git + GitHub |

---

# 17. Final Principle

Beelzebub must be intelligent without becoming unpredictable.

The system should combine AI-based coordination with deterministic business operations, controlled permissions, persistent state, and human oversight.

**Architecture decisions must serve reliability, security, maintainability, and measurable business value.**

---

**Document owner:** Beelzebub Development Project  
**Version:** 1.0  
**Status:** Initial decision log.