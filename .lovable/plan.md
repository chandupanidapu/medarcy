# Editable profile in Settings

## Experience
- Replace the static sample profile in Settings with an editable form for display name, clinical role, and specialty. Keep the clinical fields optional so the profile never implies verified credentials.
- Add a clear Save button, inline validation, and feedback for successful or failed saves. Show the saved name, role, and specialty in Settings and update the existing sidebar/profile menu identity to match.
- Keep the page’s existing Appearance and About sections unchanged. Label the profile as a local demo preference, not a verified clinician account.

## Technical details
- Store the profile only in this browser using a dedicated, versioned local-storage key; do not create a database, authentication flow, or clinical-record integration. Show that it does not sync across devices or accounts.
- Keep one shared client-side profile state in the app shell, with safe initialization after hydration, validated reads, and guarded writes when storage is unavailable. Avoid storing patient information.
- Add interaction tests covering editing, validation, save/readback after reload, and sidebar/menu updates; inspect mobile and desktop layouts and confirm no new React or preview errors.
