# Medarcy dark mode

## Experience
- Add an accessible light/dark appearance control in the shared header, usable on desktop and mobile. Keep the current light appearance as the initial default, and remember the user's choice on this device.
- Apply the existing restrained navy, slate, teal, and gold dark palette consistently across all workspaces, menus, dialogs, search, and notifications. Preserve clinical readability and the current compact visual style.

## Implementation details
- Use the existing semantic color tokens and `.dark` palette in the global stylesheet; adjust tokens only where a screen fails contrast or hierarchy checks. Do not duplicate color values in individual pages.
- Initialize the saved appearance before the app paints to avoid a light-theme flash, while keeping server and client markup consistent. Use one small client-side theme control in the shared shell, with an accessible label and state. Store only the appearance choice locally; clinical content remains an unsaved prototype.
- Extend the navigation/control regression tests to cover switching appearances and remembering a choice after reload. Check the shared header and representative clinical pages at desktop and mobile widths, including dialog and menu contrast and no text overlap or horizontal overflow.

No authentication, clinical behavior, or backend changes.
