# Beelzebub — Product Requirements Document (PRD)

**Product:** Beelzebub AI  
**Product category:** AI Business Operations Agent  
**Version:** 1.0  
**Status:** Initial Specification  
**Project:** Beelzebub  
**Target market:** Small retail and distribution businesses  
**Competition:** Dubai Chamber of Digital Economy — Create AI Agents Championship 2026–2027  
**Target category:** Best Business AI Agent

---

# 1. Product Overview

## 1.1 Vision

Beelzebub is an AI-powered business operations agent designed to help small retail and distribution businesses understand their operations, identify problems, and execute routine business workflows through controlled, intelligent automation.

Traditional business management software requires business owners to navigate multiple modules, manually inspect records, and coordinate repetitive operational tasks.

Beelzebub aims to simplify this experience by introducing an AI agent that understands business goals, retrieves relevant business information, coordinates tools, and prepares or executes actions with appropriate human authorization.

The objective is not to build another chatbot or a complete ERP replacement.

The objective is to create an intelligent operational assistant that can reliably get business work done.

## 1.2 Product Philosophy

Beelzebub follows five principles:

1. **Action over conversation:** The agent should complete useful operational workflows rather than merely answer questions.
2. **Data over assumptions:** Business facts must come from authoritative database records.
3. **Deterministic business logic:** Calculations and business rules must be implemented in validated application code.
4. **Human control:** Consequential actions require appropriate authorization and approval.
5. **Transparency:** Users should understand what the agent knows, recommends, proposes, and executes.

## 1.3 Problem Statement

Small retail and distribution businesses frequently struggle with:

- Identifying products that require replenishment.
- Monitoring inventory levels.
- Comparing supplier prices and purchasing conditions.
- Preparing purchase orders.
- Tracking outstanding and overdue invoices.
- Following up with customers.
- Understanding daily operational performance.
- Coordinating repetitive administrative work.

These activities are often performed manually using spreadsheets, accounting software, messaging applications, and disconnected business tools.

This creates operational overhead, delayed decisions, and avoidable mistakes.

Beelzebub addresses these problems through a unified AI-assisted operations interface.

---

# 2. Target Customers

## 2.1 Initial Target Market

Small retail and distribution businesses that maintain product inventory, work with multiple suppliers, and manage customer invoices.

## 2.2 Demonstration Business

For initial development, Beelzebub will operate using one synthetic demonstration business.

Proposed characteristics:

- Business type: Electronics accessories distributor.
- Products: Approximately 500–2,000.
- Suppliers: Multiple suppliers with different pricing and purchasing conditions.
- Customers: Retailers and business customers.
- Inventory: Product quantities maintained at a business location.
- Purchasing: Purchase orders prepared for supplier replenishment.
- Invoices: Customer invoices with payment deadlines and outstanding balances.

These figures describe our proposed test environment, not real customer data.

## 2.3 Primary User Personas

### Business Owner

Needs:
- Understand business performance.
- Identify operational problems.
- Approve purchases.
- Monitor overdue invoices.
- Reduce repetitive administrative work.

### Operations Manager

Needs:
- Monitor inventory.
- Compare suppliers.
- Prepare purchase orders.
- Coordinate operational workflows.
- Review task history.

### Staff Member

Needs:
- Access permitted business information.
- Prepare operational drafts.
- Monitor assigned tasks.
- Request approval for restricted actions.

---

# 3. Product Scope

## 3.1 Core Modules

| Module | Description | Priority |
|---|---|---|
| Dashboard | Business metrics and operational overview | P0 |
| Inventory | Stock monitoring and low-stock detection | P0 |
| Suppliers | Supplier information and comparison | P0 |
| Purchasing | Reorder calculations and purchase order drafts | P0 |
| Approvals | Human review and approval management | P0 |
| AI Assistant | Natural-language operational interaction | P1 |
| Invoices | Outstanding and overdue invoice monitoring | P1 |
| Customer Management | Customer information and reminder drafts | P1 |
| Daily Briefing | Summarized operational report | P1 |
| Activity History | Workflow and audit history | P0 |

P0 represents essential MVP capabilities. P1 represents capabilities to implement after the foundational workflow.

## 3.2 Business Intelligence Dashboard

The dashboard should provide an overview of business operations.

Initial information:

- Total products.
- Total inventory units.
- Number of low-stock products.
- Number of pending purchase order approvals.
- Outstanding invoice amount.
- Number of overdue invoices.
- Recent operational activities.

Requirements:

- Metrics must be calculated from actual database records.
- Displayed information must be consistent with the underlying business data.
- Users should be able to navigate to the relevant records.
- Loading, empty, and error states must be supported.

## 3.3 Inventory Management

The inventory module will monitor stock quantities and identify products that need replenishment.

Required product information:

- Product ID.
- SKU.
- Product name.
- Description.
- Category.
- Unit of measurement.
- Selling price.
- Cost price.
- Current stock quantity.
- Reorder point.
- Target stock quantity.
- Preferred supplier, if configured.
- Active/inactive status.

### Low-stock detection

A product is considered low-stock when:

`available_stock <= reorder_point`

The comparison must be performed by deterministic backend business logic.

### Reorder quantity calculation

Initial calculation:

`reorder_quantity = max(0, target_stock_quantity - available_stock)`

Additional constraints:

- Reorder quantities must respect minimum order quantities.
- Quantities must respect supplier pack sizes where applicable.
- Inactive products must not be recommended for purchasing.
- Products with invalid or missing purchasing configuration must be flagged rather than silently processed.
- The calculation must use current authoritative inventory data.

The initial MVP will not attempt advanced demand forecasting.

---

# 4. Supplier Management and Comparison

Beelzebub must retrieve and compare suppliers associated with the products requiring replenishment.

Required supplier information:

- Supplier ID.
- Supplier name.
- Contact information.
- Supplied products.
- Unit prices.
- Minimum order quantities.
- Pack sizes.
- Lead times.
- Delivery conditions.
- Active/inactive status.

### Supplier comparison

The system should compare eligible suppliers using:

1. Product availability.
2. Unit purchase price.
3. Minimum order quantity.
4. Pack-size constraints.
5. Delivery lead time.
6. Other configured purchasing conditions.

The system should explain the comparison and identify the recommended supplier.

The cheapest supplier must not automatically be considered the best supplier when other purchasing conditions make an alternative more appropriate.

Supplier recommendations must be based on actual stored supplier records.

---

# 5. Purchase Order Management

Purchase order preparation is the primary business workflow of the MVP.

## 5.1 Purchase Order Draft

The system must support creating a purchase order draft containing:

- Purchase order ID.
- Supplier.
- Product line items.
- Quantities.
- Unit prices.
- Subtotals.
- Taxes, where configured.
- Total amount.
- Creation timestamp.
- Order status.
- Workflow reference.

All monetary calculations must be performed using appropriate decimal arithmetic rather than floating-point approximations.

## 5.2 Purchase Order Lifecycle

Initial lifecycle:

`DRAFT → PENDING_APPROVAL → APPROVED → RECORDED`

Additional states:

- REJECTED
- CANCELLED
- EXPIRED
- REQUIRES_REVIEW

A recorded purchase order is an internal business record. It does not mean an order has been transmitted to or accepted by an external supplier.

External purchasing integrations are outside the initial MVP.

## 5.3 Duplicate Prevention

The system must prevent duplicate purchase orders when:

- A workflow is retried.
- A network request is repeated.
- A user submits the same approval action multiple times.
- An agent resumes from a previous workflow checkpoint.

Use appropriate idempotency controls and database constraints.

---

# 6. Human Approval Management

Consequential actions must be reviewed by authorized users.

### Approval requirements

Users must be able to:

- View pending purchase orders.
- Inspect suppliers and line items.
- Review prices and total amounts.
- Understand why the order was recommended.
- Approve the proposal.
- Reject the proposal.
- Request modifications where supported.

### Approval integrity

An approval must apply to the exact purchase order version reviewed by the user.

If consequential order details change after review, the previous approval must no longer authorize the modified order.

The system must request renewed approval.

### Authorization

- Only authorized users may approve purchase orders.
- Staff permissions must be enforced by the backend.
- The LLM must never grant itself permissions.
- Approval decisions must be persisted.
- Every consequential approval decision must produce an audit event.

---

# 7. Invoice Monitoring

Beelzebub must identify customer invoices that have outstanding balances and are past their due dates.

Required invoice information:

- Invoice ID.
- Invoice number.
- Customer.
- Invoice date.
- Due date.
- Total amount.
- Paid amount.
- Outstanding amount.
- Status.

### Overdue detection

An invoice is overdue when:

- Its outstanding balance is greater than zero.
- Its due date is earlier than the current business date.
- It is not cancelled or otherwise excluded by the business rules.

The business timezone must be considered when determining the current business date.

### Customer reminders

The system should:

- Retrieve overdue invoices.
- Calculate overdue duration.
- Retrieve relevant customer information.
- Draft a professional payment reminder.
- Present the reminder for review.

The MVP must not send external customer emails automatically.

---

# 8. Daily Operational Briefing

Beelzebub should generate a concise daily briefing containing:

- Low-stock products.
- Suggested replenishment actions.
- Pending purchase order approvals.
- Overdue customer invoices.
- Important operational changes.
- Relevant outstanding tasks.

The briefing must be grounded in current business records.

The LLM may summarize and explain the results, but it must not invent business facts or financial figures.

---

# 9. AI Agent Requirements

## 9.1 Agent Architecture

Beelzebub will initially use one central AI orchestrator with a collection of specialized tools.

LangGraph will be used for stateful workflow orchestration when the underlying business workflows are implemented and tested.

## 9.2 Initial Agent Tools

| Tool | Responsibility |
|---|---|
| get_inventory_summary | Retrieve inventory information |
| detect_low_stock | Identify products requiring replenishment |
| calculate_reorder_quantity | Calculate reorder quantities |
| get_supplier_options | Retrieve eligible suppliers |
| compare_suppliers | Compare supplier conditions |
| create_purchase_order_draft | Prepare a purchase order |
| get_overdue_invoices | Retrieve overdue invoices |
| draft_customer_reminder | Prepare payment reminder text |
| generate_daily_briefing | Produce an operational summary |

## 9.3 Tool Requirements

Every tool must have:

- A defined input schema.
- A validated output contract.
- Clearly defined permissions.
- Appropriate error handling.
- Bounded execution time.
- Structured logging where appropriate.

The agent must not:

- Generate and execute arbitrary SQL.
- Directly modify database records outside validated application services.
- Invent inventory quantities, prices, or invoice balances.
- Bypass approval requirements.
- Execute unlimited tool loops.
- Treat untrusted external documents as system instructions.

## 9.4 Workflow Reliability

The agent should support:

- Workflow state persistence.
- Controlled retries.
- Timeout handling.
- Error recovery.
- Human approval interruptions.
- Duplicate-action prevention.
- Clear workflow status reporting.

---

# 10. Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-001 | Retrieve authorized business inventory | P0 |
| FR-002 | Detect low-stock products | P0 |
| FR-003 | Calculate reorder quantities | P0 |
| FR-004 | Retrieve supplier options | P0 |
| FR-005 | Compare supplier conditions | P0 |
| FR-006 | Generate purchase order drafts | P0 |
| FR-007 | Display purchase order recommendations | P0 |
| FR-008 | Obtain explicit purchase order approval | P0 |
| FR-009 | Persist approval decisions | P0 |
| FR-010 | Maintain audit history | P0 |
| FR-011 | Provide a business dashboard | P0 |
| FR-012 | Retrieve overdue invoices | P1 |
| FR-013 | Draft customer reminders | P1 |
| FR-014 | Generate daily operational briefings | P1 |
| FR-015 | Interpret natural-language operational requests | P1 |
| FR-016 | Support persistent AI workflows | P1 |

---

# 11. Non-Functional Requirements

## 11.1 Security

- Authentication must be implemented before exposing private business data.
- Business-level authorization must be enforced.
- Users must only access records belonging to authorized businesses.
- Secrets must be stored securely.
- API inputs must be validated.
- Database access must use controlled application services.
- Consequential actions must be audited.
- Uploaded documents and external content must be treated as untrusted input.

## 11.2 Reliability

- Important business operations must be covered by automated tests.
- Database transactions must preserve data integrity.
- Repeated requests must not create unintended duplicate actions.
- Workflow failures must be recoverable where possible.
- Approval decisions must remain traceable.

## 11.3 Maintainability

- Use modular architecture.
- Maintain typed interfaces.
- Keep business logic separate from AI orchestration.
- Use database migrations.
- Maintain reproducible development configuration.
- Document important architectural decisions.

## 11.4 Performance

Initial development targets:

- Normal backend operations should generally respond within one second under the synthetic demonstration workload.
- Dashboard data should load without unnecessary repeated database queries.
- Long-running agent workflows should expose their progress.
- LLM response latency should be measured separately from deterministic backend operations.

These are development targets, not measured performance claims.

---

# 12. User Interface Requirements

The application should have a clean, professional, responsive interface.

Initial navigation:

1. Overview
2. Inventory
3. Suppliers
4. Purchase Orders
5. Invoices
6. Customers
7. AI Assistant
8. Activity History
9. Settings

### Dashboard

Display business metrics, operational warnings, pending approvals, and recent activities.

### AI Assistant

Provide a natural-language interface through which users can request operational workflows.

### Approval Interface

Display proposed actions with supporting information and clear approval controls.

### Activity History

Display workflow execution history, status changes, approval decisions, and relevant audit events.

### Visual Identity

The project name Beelzebub is inspired by Baby Beel from the Beelzebub anime and manga.

The intended visual direction combines:

- A distinctive green Baby Beel-inspired mascot.
- Dark charcoal and green branding.
- Clean, professional SaaS interface design.
- Readable typography.
- Minimal visual complexity.

The product should retain a professional business identity while having a recognizable personality.

---

# 13. Technology Stack

## Frontend

- React
- Vite
- TypeScript
- Tailwind CSS

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

## Database

- PostgreSQL

## AI

- LangGraph
- Configurable hosted LLM API
- Structured tool calling

## Testing

- pytest
- API integration tests
- Agent workflow evaluation
- Frontend tests where appropriate

## Deployment

- Docker
- Hosted frontend
- Hosted backend
- Managed PostgreSQL

Technology changes must be justified and recorded in the project decision log.

---

# 14. MVP Boundaries

The first version must demonstrate a complete, reliable inventory-to-purchase-order workflow.

### Included

- One synthetic demonstration business.
- Product and inventory records.
- Supplier records and pricing.
- Low-stock detection.
- Reorder calculations.
- Supplier comparison.
- Purchase order draft generation.
- Human approval.
- Purchase order state persistence.
- Audit history.
- Basic operational dashboard.

### Additional MVP capabilities

- Overdue invoice monitoring.
- Customer reminder drafting.
- Daily operational briefing.

### Excluded

- Complete ERP functionality.
- Automatic bank payments.
- Unrestricted external email sending.
- Automatic external purchasing.
- Complex warehouse management.
- Advanced demand forecasting.
- Multiple autonomous agents.
- Unnecessary microservices.
- Real supplier integrations in the initial version.

---

# 15. Testing and Evaluation

Testing must accompany implementation rather than being postponed until the end.

Required testing areas:

1. Inventory calculations.
2. Reorder quantity calculations.
3. Supplier comparison.
4. Purchase order totals.
5. API input validation.
6. Database integrity.
7. Approval enforcement.
8. Duplicate-action prevention.
9. Workflow recovery.
10. Business-level data isolation.
11. Unauthorized access prevention.
12. Prompt-injection resistance.

A reproducible synthetic evaluation dataset must be maintained with known expected outcomes.

Evaluation metrics should include:

- Correct low-stock detection rate.
- Reorder calculation correctness.
- Supplier recommendation correctness.
- Workflow completion rate.
- Unauthorized action prevention.
- Duplicate-action prevention.
- Average workflow execution time.
- Failure recovery rate.

Business value must be measured through real user experiments rather than fabricated productivity or financial claims.

---

# 16. MVP Acceptance Criteria

The MVP will be considered functionally complete only when the following conditions are demonstrated.

### Inventory-to-Purchase-Order Workflow

- [ ] User can retrieve inventory information.
- [ ] Low-stock products are correctly identified.
- [ ] Reorder quantities match expected calculations.
- [ ] Eligible suppliers are retrieved correctly.
- [ ] Supplier comparisons use actual stored data.
- [ ] Purchase order drafts contain correct line items and totals.
- [ ] Recommendations include supporting evidence.
- [ ] Unauthorized users cannot approve purchase orders.
- [ ] Authorized users can approve or reject purchase orders.
- [ ] Modified orders require renewed approval.
- [ ] Retried workflows do not create duplicate purchase orders.
- [ ] All consequential actions produce appropriate audit records.

### Additional Operational Workflows

- [ ] Overdue invoices are correctly identified.
- [ ] Outstanding balances are correctly calculated.
- [ ] Customer reminders are drafted accurately.
- [ ] Daily briefings reflect current business records.

### Engineering and Security

- [ ] Backend business logic has automated tests.
- [ ] API integration tests pass.
- [ ] Database migrations work.
- [ ] Business-level data isolation is tested.
- [ ] Workflow recovery is tested.
- [ ] Secrets are excluded from version control.
- [ ] Application can run using the documented development setup.

A generated codebase or successful demonstration alone does not satisfy these criteria.

---

# 17. Success Metrics

We will evaluate Beelzebub using measurable criteria.

| Area | Measurement |
|---|---|
| Business correctness | Correctness of recommendations |
| Workflow reliability | Successful end-to-end execution rate |
| Security | Unauthorized action prevention |
| Reliability | Recovery from controlled failures |
| Efficiency | Time required to complete operational tasks |
| Usability | Feedback from actual business users |
| Agent performance | Tool selection and execution correctness |

Targets will be established after the first working baseline and initial user testing.

No performance or customer adoption figures will be claimed without evidence.

---

# 18. Future Expansion

Only after the MVP is reliable should we consider:

- Multiple business accounts.
- External ERP and accounting integrations.
- Supplier communication integrations.
- Advanced demand forecasting.
- Automated recurring workflows.
- Additional business intelligence.
- Multi-location inventory.
- More sophisticated operational agents.

Each expansion must be evaluated against customer value, engineering effort, security, and competition priorities.

---

# 19. Product Development Strategy

Development will proceed through these milestones:

| Milestone | Deliverable |
|---|---|
| M0 | Project foundation and product specification |
| M1 | Database schema and synthetic business data |
| M2 | FastAPI backend and database integration |
| M3 | Inventory and supplier business logic |
| M4 | Purchase orders and approval management |
| M5 | Invoice monitoring and customer reminders |
| M6 | LangGraph orchestration |
| M7 | React dashboard and AI assistant |
| M8 | Security, integration testing, and evaluation |
| M9 | Deployment |
| M10 | User validation and competition preparation |

A milestone must be tested before being marked complete.

---

# 20. Final Product Definition

Beelzebub is an AI-powered business operations agent that helps small retail and distribution businesses monitor operations, identify problems, coordinate business workflows, and prepare actions through controlled AI-assisted automation.

Its differentiator is the combination of:

- Actual business data.
- Deterministic business calculations.
- Intelligent workflow orchestration.
- Validated tool execution.
- Human approval.
- Persistent workflow state.
- Traceable audit history.

**The central promise:**

Help business owners spend less time coordinating routine operations and more time running their businesses.

---

**Document ownership:** Beelzebub Development Project  
**Document version:** 1.0  
**Status:** Initial specification pending review and approval.