# Training Academy Management System

Lightweight Odoo addon that links Products to Courses and automatically creates draft Academy enrollments from confirmed Sale Orders while preserving Academy business rules (capacity, uniqueness, workflows).

## Overview

- Product ↔ Course mapping: product.template.course_id (readonly in form; editable via admin wizard).
- Sales integration: when a sale order is confirmed, for each order line whose product is linked to a course the module creates a draft `academy.enrollment` (student = order.partner_id, course = product.course_id).
- Academy models (course, category, enrollment, partner) include stored/computed fields, constraints and statusbar workflows; sales integration only creates draft enrollments — Academy workflows enforce capacity and uniqueness.

## Module tree (key files)

- **init**.py, **manifest**.py
- models/
  - academy_partner.py — partner flags, counters, smart buttons
  - account_move.py — optional accounting hooks
  - category.py — course categories
  - course.py — course model, computed/stored fields, validations, actions, product helper
  - enrollment.py — enrollment model, computed fields, SQL uniqueness constraint, confirmation checks
  - product_template.py — adds readonly Many2one `course_id` to product.template
  - sale_order.py — extends sale.order to create draft enrollments on confirm
- views/
  - product_template_views.xml — product form integration
  - course_views.xml, category_views.xml, enrollment_views.xml, partner_views.xml, menus.xml
- wizard/
  - product.py — transient model to create/link products for courses
  - product_wizard_view.xml — wizard form/action
- security/
  - academy_security.xml, ir.model.access.csv
- tests/ (optional) — unit/integration tests

## Functional flow

1. Admin links a product to a course (Product form or Product Link wizard).
2. Customer places and confirms a Sale Order containing that product.
3. On confirm, the module creates a draft `academy.enrollment` for the sale partner and course.
4. Use Academy UI to confirm enrollment — server-side constraints prevent confirming when the course is full or when duplicate (student, course) exists.

## Quick test checklist

- Link a product to a course (via wizard or product form).
- Create and confirm a Sale Order containing that product → verify a draft `academy.enrollment` exists for the order partner + course.
- Confirm enrollment in Academy UI — ensure capacity rules block over-enrollment.
- Try duplicate enrollment for same student+course → SQL constraint should fail.

## UI & Actions

- Product form displays readonly Course field (product_template_views.xml).
- Course form includes action to open product creation wizard (course.action_create_product).
- Partner form includes Academy tab and smart buttons to view enrollments/courses (partner_views.xml).
- Menus available under "Academy" (menus.xml).

## Security & Data Integrity

- Module integrates with Academy security (groups, record rules, ir.model.access.csv).
- Enrollment SQL constraint prevents duplicate (student_id, course_id).
- Enrollment confirmation is guarded server-side (ValidationError raised if course is full).
- Course model contains validations for dates, positive capacity and product linkage checks.

## Developer notes & best practices

- Keep product.course mapping readonly in production UI; use the wizard for controlled creation/association.
- Perform all critical checks on server-side (constraints, @api.constrains) — client-side checks are helpful but not sufficient.
- Use stored computed fields for counts (enrolled_count, available_seats) to optimize report queries.
- Prefer creating draft enrollments from external channels (sales, website) then confirm them using Academy workflows so existing business rules run.
- Add/maintain unit tests for:
  - sale → enrollment creation
  - enrollment uniqueness constraint
  - capacity / confirmation blocking
  - course date and capacity validations
- If you require strict one-product-per-course mapping enable the commented SQL constraint in product_template.py.
