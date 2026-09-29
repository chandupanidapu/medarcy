# Import profile from a downloaded JSON backup

Add an "Import profile" option to Settings that reads a previously downloaded `medarcy-profile.json`, validates it, and saves it — the counterpart to the existing Download profile button.

## What you'll see

- A new **Import profile** button in Settings → Profile, next to Download profile.
- Clicking it opens a file picker limited to `.json` files.
- A valid backup fills in and saves the display name, clinical role, and specialty immediately, with a success message; the sidebar and profile menu update at once.
- An invalid file (wrong file type, broken JSON, not a Medarcy profile backup, or fields that fail the same rules as the form — e.g. empty name or over 80 characters) is **not** saved. A clear inline message explains what was wrong, and your current profile stays untouched.
- Works on phone and desktop; respects reduced motion like the rest of the page.

## Technical details

- `src/lib/profile.ts`: add `parseProfileImport(json: string)` — parses the JSON, checks the export envelope (`type: 'profile-backup'` with a `profile` object), and validates the profile fields with the existing `profileSchema`. Returns either the validated `Profile` or a readable error message. Also accept a bare profile object (no envelope) for flexibility.
- `src/routes/settings.tsx`: hidden `<input type="file" accept="application/json,.json">` triggered by an outline "Import profile" button (Upload icon). On file selection, read the text, run `parseProfileImport`, and on success call `saveProfile` + update the draft; on failure set the existing inline error state. Reset the input value after each pick so the same file can be chosen again.
- Validation errors reuse the existing `role="alert"` error area; success reuses the `role="status"` message ("Profile imported and saved in this browser.").
- `src/test/navigation.test.tsx`: add tests — importing a valid backup updates the profile and persists across remount; importing invalid JSON and a schema-failing file shows an error and leaves the saved profile unchanged.
- No backend involved: import stays browser-local, matching the existing demo-profile storage. The "no patient information" disclaimer remains.
