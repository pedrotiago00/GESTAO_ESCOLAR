# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Django + Python, using the project’s existing app structure under `apps/` and Django templates with SQLite for the default local development database.

## Users

Primary users are school administrators, coordinators, and staff who manage academic and operational records for an institution. The project also supports teacher workflows and school-scoped user roles, with data organized around a single `Escola` context.

## Product Purpose

This product is a school management system designed to centralize academic administration and daily school operations. It supports the creation and maintenance of teachers, classes, students, schedules, attendance, exams, grades, and institutional communication.

## Positioning

The product is a domain-specific management system for educational institutions, built around school-scoped records and academic workflows rather than a generic admin dashboard or ERP.

## Operating Context

Users work in a secured Django application with authenticated access. The main flows are dashboard review, student and class registration, timetable management, attendance tracking, assessment records, exam scheduling, and communications such as notices and meetings. The system is organized by school and user role rather than by a broad multi-tenant SaaS model.

## Capabilities and Constraints

- School-scoped records keyed by `Escola` across the data model.
- Role-based access via `PerfilUsuario` and `Funcao`.
- Core entities include `Professores`, `Disciplinas`, `Turmas`, `Estudantes`, `Responsaveis`, `Horarios`, `Frequencia`, `Exames`, and `Notas`.
- Academic and administrative data are stored in relational models with integrity constraints such as unique codes and school-specific uniqueness rules.
- The project is currently structured as a Django app with template-based views and login-protected routes.
- The default development database is SQLite-based, and the app is organized in modular application folders: `academico`, `cadastros`, `comunicacao`, `dashboard`, and `usuarios`.
- No evidence yet of external integrations, billing, public portal flows, or a broad multi-school deployment model.

## Brand Commitments

No formal brand, logo system, voice, or visual identity is defined in the codebase. The project does not yet show a bound brand name or customer-facing positioning beyond the operational school-management purpose.

## Evidence on Hand

- `apps/usuarios/models.py` defines `Escola`, `Funcao`, and `PerfilUsuario`.
- `apps/cadastros/models.py` defines the core school registry entities.
- `apps/academico/models.py` defines schedules, attendance, exams, and grades.
- `apps/dashboard/views.py` and `apps/dashboard/templates/dashboard/` show the central monitoring flow.
- `apps/usuarios/views.py` and `apps/usuarios/forms.py` define authentication and account access.
- `workspace/settings.py` confirms the Django project configuration.
- `db.sqlite3` is the current local data store.
- No product marketing copy, brand assets, testimonials, or legal claims are present in the repository.

## Product Principles

1. Operational clarity for school administration and academic management.
2. Data integrity and school-specific isolation across records.
3. Role-aware access and structured workflows for teachers and staff.
4. Maintenance of reliable academic history for classes, students, and assessments.
5. Practical administration over generalized consumer-facing features.

## Accessibility & Inclusion

No product-specific accessibility or inclusion requirements are established in the codebase yet. As the interface is built, the default Django form and HTML patterns should be reviewed for clear labeling, keyboard support, and readable contrast.
