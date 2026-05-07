# SOAR Automation Engineering Portfolio

This repository showcases selected security automation engineering work based on real-world experience with Palo Alto Cortex XSOAR and XSIAM.

The goal of this portfolio is to demonstrate practical capability in building, extending, troubleshooting, and documenting SOAR-based workflows for security operations environments.

The examples in this repository are sanitized and recreated for portfolio purposes. They do not contain proprietary client data, production credentials, private indicators, internal playbooks, or confidential implementation details.

---

## Focus Areas

This portfolio focuses on the following areas:

- XSOAR and XSIAM automation design
- Custom Python integration development
- API-driven security workflow automation
- Incident enrichment and investigation support
- Dynamic HTML sections for analyst-facing layouts
- XQL-based investigation and reporting logic
- SOC process optimization
- Secure handling of sensitive data
- Troubleshooting and production-readiness patterns

---

## Why This Repository Exists

Security operations teams often rely on repetitive manual investigation steps across alerts, tickets, threat intelligence sources, endpoint telemetry, firewall logs, and case management systems.

My work focuses on reducing that manual effort by designing automations that help analysts:

- enrich incidents faster
- standardize investigation steps
- reduce repetitive API lookups
- improve case visibility
- generate cleaner reports
- preserve auditability
- reduce alert-handling fatigue

This repository documents selected patterns and recreated examples from that experience.

---

## Technologies and Platforms

Core technologies represented in this portfolio:

- Palo Alto Cortex XSOAR
- Palo Alto Cortex XSIAM
- Python
- REST APIs
- XQL
- HTML dynamic sections
- JSON data normalization
- Threat intelligence enrichment
- Service management API integrations
- SOC workflow automation

Supporting engineering practices:

- modular Python design
- safe error handling
- API client abstraction
- reusable rendering functions
- sample payload testing
- defensive parsing
- sanitized documentation
- production-style troubleshooting notes

---

## Portfolio Sections

### 1. Custom Integrations

The `integrations/` directory contains recreated examples of custom or extended integrations.

Example areas include:

- ServiceDesk Plus API extension patterns
- request conversation retrieval
- notification rendering
- note creation troubleshooting
- Hatching Triage result parsing
- threat intelligence enrichment workflows

Each integration section includes:

- purpose
- command behavior
- sample input and output
- implementation notes
- known API issues
- troubleshooting observations

---

### 2. XSOAR / XSIAM Playbook Designs

The `playbooks/` directory contains documentation for security automation workflows.

Examples include:

- DNS malware investigation
- DNS tunneling or DGA-style investigation support
- XDR collector monitoring
- phishing investigation support
- threat intelligence enrichment workflows

Each playbook section explains:

- operational purpose
- analyst pain point
- automation workflow
- decision logic
- expected inputs
- expected outputs
- limitations
- future improvements

---

### 3. XQL Investigation Examples

The `xql/` directory contains sanitized XQL examples used for investigation and reporting logic.

Example use cases:

- DNS domain activity review
- PAN NGFW traffic pivoting
- XDR collector status monitoring
- event count aggregation
- source and destination IP context
- time-window based investigation

Queries are written as portfolio-safe examples and may require adjustment depending on tenant schema, dataset availability, and Cortex version.

---

### 4. Dynamic Section Rendering

The `dynamic-sections/` directory contains examples of HTML rendering patterns for XSOAR layouts.

These examples demonstrate how analyst-facing information can be presented as clean, readable cards inside incident layouts.

Covered patterns include:

- notification cards
- conversation thread rendering
- compact HTML for layout constraints
- fallback rendering when HTML size becomes too large
- safe formatting for inconsistent API responses

---

## Example Use Cases

This repository includes examples inspired by the following types of work:

### DNS Malware Investigation Support

A workflow that helps analysts investigate suspicious DNS-related alerts by organizing enrichment data, related traffic, domain intelligence, and contextual indicators into a structured investigation view.

### ServiceDesk Plus Integration Extension

A custom integration enhancement pattern for retrieving request conversations, notifications, and notes from a service management platform and rendering them inside XSOAR.

### XDR Collector Monitoring

A recurring monitoring pattern that identifies stopped collectors, suppresses duplicate reporting, and produces consolidated status output for operational review.

### Hatching Triage Result Interpretation

A parser and documentation pattern for interpreting sandbox result summaries, including score, status, target, tags, and analysis kind.

---

## Security and Data Handling

This repository does not include:

- production credentials
- real API tokens
- client names
- internal tenant URLs
- proprietary playbook exports
- private indicators of compromise
- real incident data
- confidential screenshots
- employer-owned code

All examples are sanitized, generalized, or recreated for demonstration purposes.

See `SECURITY.md` and `DISCLAIMER.md` for additional details.

---

## Engineering Principles Demonstrated

This portfolio is built around the following principles:

### 1. Analyst-Centered Automation

Automation should reduce cognitive load for analysts, not create another layer of complexity.

### 2. Defensive API Integration

External APIs can return inconsistent, incomplete, or unexpected payloads. Integration code should handle this safely.

### 3. Clear Investigation Context

Security automation should preserve enough context for analysts to understand what happened, why it matters, and what to do next.

### 4. Audit-Friendly Design

Automation outputs should be explainable, reproducible, and suitable for review.

### 5. Safe Portfolio Publishing

Security automation examples must be sanitized before public release.

---

## Target Roles

This portfolio is relevant to roles such as:

- Security Automation Engineer
- SOAR Engineer
- Cybersecurity Automation Engineer
- Security Integration Engineer
- Detection and Response Engineer
- SOC Automation Engineer
- XSOAR Engineer
- XSIAM Engineer
- Security Platform Engineer
- AI / ML Security Automation Engineer

---

## About Me

I am a cybersecurity automation engineer with experience building and maintaining automation workflows for security operations environments.

My work includes XSOAR and XSIAM playbook development, Python-based integration engineering, API troubleshooting, incident enrichment, layout rendering, and automation design for SOC use cases.

I am especially interested in the intersection of:

- cybersecurity automation
- AI-assisted SOC workflows
- security architecture
- cloud security
- threat investigation
- analyst productivity tooling

---

## Repository Status

This repository is continuously updated as a professional portfolio.

The examples are intended to demonstrate engineering thinking, implementation style, documentation quality, and practical security automation experience.