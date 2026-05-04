# Gemini Prompt

Scan `/Users/ywchen/Dev/lingo/lingo-frontend-web` for product-visible UI completeness gaps after
`FRONTEND_V2_INTAKE_COMPLETION`.

Focus on:

- Routes and navigation targets that do not match `app_router.dart`.
- Product-visible placeholder copy such as `coming soon`, `placeholder`, `Beta`, `Legacy Mockup`, or `Fail-Soft`.
- Whether Learning Library product routes use artifact data by default.
- Whether modular runtime pilot screens are reachable from normal product navigation.

Do not propose content data format changes. Do not inspect or modify `content-ko` or
`content-pipeline`. Output file/line references, severity, and a minimal fix plan.

