# Medarcy logo integration

## What will change
- Replace the placeholder sidebar “M” and typed wordmark with the supplied Medarcy artwork: blue logo in light mode, white logo in dark mode.
- Keep the “Clinical Intelligence Platform” descriptor and the existing navigation behavior. Give the light-mode brand area a light surface so the blue artwork remains legible against the otherwise dark sidebar; retain a dark brand area for the white artwork.
- Fit the artwork cleanly in expanded and mobile navigation, with a mark-only presentation when the desktop sidebar is collapsed. Preserve accessible naming for the home link.
- Derive a compact square favicon from the uploaded blue mark, and point the browser icon at it.

## Verification
- Check the logo on desktop expanded/collapsed navigation and the mobile drawer, in both appearances and after reloading a saved appearance.
- Confirm the favicon loads, no horizontal overflow appears, and existing navigation/theme tests continue passing.

## Technical details
- Store the supplied raster images as Lovable Assets pointers and switch between them with the existing appearance state or theme selector.
- Create small, proportionally cropped mark derivatives only where compact navigation and favicon require them; keep the favicon as a real square file in `public/`.
- Keep this entirely within the visual prototype; no changes to clinical content or services.
