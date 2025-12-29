# Training Academy Management System

Lightweight Odoo module bundle for managing courses, categories, enrollments, partners and related products/sales.

## Overview

- Odoo 18 compatible module collection under `addons/academy`.
- Provides models and views for courses, categories, enrollments, partner data, product templates and sales integration.

## Features

- Course and category management
- Enrollment workflows
- Product templates for courses and related sales
- Basic security and access control
- Wizard for product creation

## Prerequisites

- Odoo 18 (this repository includes an Odoo tree in `odoo_18.0.20251224` for reference)
- Docker & Docker Compose (optional but recommended for quick development)

## Quick start (Docker Compose)

From the project root run:

```bash
docker compose up -d
```

Then open Odoo in your browser (usually at http://localhost:8069). Use the web UI to create a database.

## Installing the `academy` module

1. In Odoo go to `Apps` → click `Update Apps List` (or enable developer mode and Update).
2. Search for `academy` (or `Training Academy`) and click `Install`.

Note: If Odoo does not find the module, ensure the `addons_path` in your Odoo configuration includes this repository's `addons` folder.

## Development notes

- VS Code: a workspace-specific settings file exists at `.vscode/settings.json` that sets `python.analysis.extraPaths` using `${workspaceFolder}` so the language server can resolve Odoo imports. Example value:

```
${workspaceFolder}/../odoo_18.0.20251224/odoo-18.0.post20251224/odoo/addons
```

- Odoo config file included: `config/odoo.conf` — adapt paths there as needed.

- Common developer workflow:

```bash
# rebuild/start containers
docker compose up -d --build

# follow logs
docker compose logs -f
```

## Project structure (key paths)

- `addons/academy/` — the main module code (models, views, security, wizards)
- `config/odoo.conf` — example Odoo configuration
- `docker-compose.yml` — service orchestration for local development

## Contributing

Feel free to open issues or pull requests. For code contributions, keep changes focused, add tests when appropriate, and follow the existing module structure.

## License

See repository root files for license information. If none provided, ask the project owner for licensing details before reuse.
