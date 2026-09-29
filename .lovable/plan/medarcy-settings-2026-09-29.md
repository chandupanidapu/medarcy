# Medarcy Settings

## Experience
- Replace the profile menu’s **Profile settings** entry with **Settings**, opening a dedicated Settings page. Keep the profile avatar as the entry point.
- Place the demo profile information in a **Profile** section on Settings, clearly labeled as sample workspace information rather than an editable or authenticated account.
- Move the light/dark appearance control from the top bar into an **Appearance** section on Settings. Preserve its current saved preference and instant theme behavior.
- Move the top-bar **?** clinical-services message into an **About** section on Settings. State plainly that this interface demo has no connected clinical services or live clinical analysis; remove the redundant top-bar help icon.
- Make Settings easy to reach from the sidebar as well as the profile menu, including the mobile drawer and collapsed navigation.

## Technical details
- Add a dedicated `/settings` TanStack page with unique page metadata and semantic, keyboard-accessible controls matching Medarcy’s existing design tokens.
- Reuse the shell’s existing appearance state and local preference; avoid a second source of truth or changing authentication/data behavior.
- Update navigation and interaction tests for Settings access, theme persistence, About copy, and the absence of the old top-bar controls. Verify desktop and mobile layouts and reduced-motion behavior.
