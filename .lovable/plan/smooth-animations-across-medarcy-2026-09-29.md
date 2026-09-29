# Smooth animations across Medarcy

Add calm, restrained motion everywhere, in keeping with the clinical, enterprise style: no bouncing, glowing, or flashy effects.

## What you'll see
- **Page changes:** each workspace fades in and slides up slightly when you open it.
- **Cards and lists:** quick-action cards, recent sessions, evidence results, studies, documents and report sections appear one after another in a short sequence.
- **Hover and press:** cards lift gently with a soft border highlight. Buttons respond with a slight press effect.
- **Sidebar and drawer:** collapsing the sidebar and opening the mobile menu move smoothly. Labels fade instead of popping.
- **Report sections and tabs:** expanding sections opens smoothly, and switching tabs cross-fades the content.
- **Dialogs, menus, toasts:** these fade and scale in slightly (for example, the approval confirmation and the profile menu).
- **Theme switch:** colours shift gently between light and dark instead of changing all at once.
- **Workflow strip:** the Clinical Context → Structured Result steps light up in order once.
- **Loading states:** skeleton placeholders shimmer softly.

## Accessibility
All motion turns off automatically for people who set their device to reduce motion.

## Technical details
- Add reusable motion tokens to `src/styles.css`: durations of 150/250/400ms, an ease-out curve, and keyframes for fade-up, stagger and shimmer. Add utilities such as `animate-enter` and `stagger-children` (using an nth-child delay via a CSS variable).
- In `shell.tsx`, key the page container to the route path so the entry animation runs on each navigation. Add width and opacity transitions to the sidebar.
- Apply the utilities in the route pages. Use existing shadcn accordion, tabs, dialog and dropdown animations, and make their timing consistent.
- Theme transition: temporarily add a `theme-transition` class during the toggle so colour changes are smooth without affecting other interactions.
- Use a global `@media (prefers-reduced-motion: reduce)` override.
- Use CSS only, with no new dependencies. Re-run the 6 tests and check at 360px and 1280px for overflow.
