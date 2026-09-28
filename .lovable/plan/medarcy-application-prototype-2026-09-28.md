# Medarcy application prototype

## Product experience

- Replace the blank first screen with a signed-in **Medarcy workspace**: a restrained greeting, clinical task composer, six task shortcuts, recent fictional sessions, and a conceptual clinical workflow strip.
- Create a consistent app shell with a collapsible desktop sidebar, mobile drawer, page title, search, status, notifications, help, and profile controls. Treat the signed-in appearance as a **visual prototype**, not real authentication.
- Build distinct workspaces for Clinical Review, Medical Research, Evidence Engine, Drug Intelligence, Diagnostics, Knowledge Base, and History. Each gets a purposeful layout rather than a generic chat or repeated dashboard template.
- Use the supplied navy, dark, white, slate, restrained gold, and teal palette with semantic design tokens, subtle borders, compact radii, accessible type, and responsive layouts.

## Clinical content and safety

- Use clearly marked fictional sample cases, studies, documents, and references. Avoid real patient information, fabricated real-world citations, invented drug doses, or claims of live retrieval or analysis.
- Make Clinical Review a structured two-column workstation with editable case fields, scannable report sections, evidence/context rail, source-versus-interpretation labeling, uncertainty, limitations, and the requested decision-support notice.
- Make Research and Evidence Engine source-oriented, with sample study summaries, strategy/filter controls, comparison, and traceable sample reference details. Make Drug Intelligence safety-first and Diagnostics explicitly uncertain and clinician-reviewed.
- Show the six-step cognitive workflow as a **conceptual** process, not a representation of implemented internal operations.

## Prototype behavior

- Connect navigation, task shortcuts, local search/filtering, report expansion, tabs, dialogs, and empty/loading/error presentation where relevant.
- Provide local-only action feedback. Save, export, regenerate, upload, microphone, notifications, and approval controls must never imply a real clinical service or persistent storage; approval requires explicit confirmation and remains a demo state.
- Check the primary journeys and desktop, tablet, and mobile presentation, including no horizontal overflow and readable clinical content.

## Technical implementation

- Use the existing TanStack Start/React/TypeScript/Tailwind project and its UI primitives and Lucide icons. Create separate content routes with unique page metadata and reusable shell, control, and clinical-content components.
- Keep data and interactions in client-side mock modules/state only. Do not add a backend, database, authentication, external medical integration, or actual clinical decision engine. Organize sample data and interface boundaries so a future FastAPI connection can replace them cleanly.