# Settings: download saved profile as JSON

## What to build

Add a "Download profile" control in the Settings page's Profile section so the saved local profile (display name, clinical role, specialty) can be exported as a JSON file for backup or transfer.

## Behavior

- A secondary button labelled "Download profile" (with a Download icon) appears next to "Save profile" in the Profile section.
- Clicking it downloads a file named `medarcy-profile.json` containing:
  - `app: "Medarcy"` and `type: "profile-backup"` markers
  - `exportedAt`: current ISO timestamp
  - `profile`: the saved (not draft) profile fields — displayName, clinicalRole, specialty
- Uses the same Blob-download pattern as the existing Export Report action; no backend, nothing is uploaded anywhere.
- Shows a toast clarifying it is a local export of sample/demo workspace details (no patient information involved).
- Button stays enabled even when the profile is unchanged, since it exports the saved state, not the draft.

## Files

- `src/lib/profile.ts` — add a small `buildProfileExport(profile)` helper returning the export object (keeps the shape testable and reusable for a future "import" flow).
- `src/routes/settings.tsx` — add the Download profile button wired to the helper + Blob download + toast.
- `src/test/navigation.test.tsx` — add one test: clicking Download profile produces a JSON blob with the saved profile fields and the export markers.

## Verification

- Run the interaction test suite; confirm the new export test and all existing tests pass.
- Playwright check on the Settings page (desktop and mobile widths): button renders inline with Save profile, download is triggered, no layout overflow.
