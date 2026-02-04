# Configuration Files

This directory contains YAML configuration files used by the Magic Umbrella time allocation system.

## Files

- **customers.yaml** - List of customers and their aliases/domains
- **projects.yaml** - List of projects and their associations
- **categories.yaml** - Meeting type definitions and keywords

## Setup

1. Copy the example files:
   ```bash
   cp customers.example.yaml customers.yaml
   cp projects.example.yaml projects.yaml
   cp categories.example.yaml categories.yaml
   ```

2. Edit each file to add your organization's customers and projects

3. The `.yaml` files are gitignored to protect sensitive information

## Adding a New Customer

```yaml
- name: "Full Customer Name"
  aliases: ["Short Name", "Alternative Name"]
  domains: ["customerdomain.com"]
  color: "#HEXCOLOR"
```

## Adding a New Project

```yaml
- name: "Project Name"
  aliases: ["Alias"]
  customer: "Customer Name" # or null for internal
  type: "customer" # or "internal"
  active: true # or false if completed
```

## Validation

Run validation to check YAML syntax:
```bash
uv run python -m magic_umbrella.config.validator
```
