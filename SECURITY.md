# Security Policy

This repository is a public portfolio repository. It does not contain production secrets, confidential data, customer data, real incident data, or employer-owned proprietary code.

## Data Sanitization Rules

Before publishing any example, the following must be removed or replaced:

- API tokens
- authentication headers
- tenant URLs
- customer names
- internal usernames
- private IP ranges tied to real environments
- real domains or indicators
- incident IDs
- ticket IDs
- screenshots containing sensitive metadata
- proprietary playbook exports
- employer-specific implementation details

## Safe Example Data

All examples should use mock values such as:

- `example.com`
- `192.0.2.10`
- `203.0.113.25`
- `tenant.example.local`
- `INC-000000`
- `REQ-000000`
- `api.example.com`

## Disclosure

This repository is for demonstration and educational purposes only. It does not represent any employer, client, or production environment.