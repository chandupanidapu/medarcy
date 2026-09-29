# Reduced-motion support

## Goal

When a clinician's operating system is set to "reduce motion", Medarcy should show every page, card, tab, and section instantly — no sliding, fading, lifting, or shimmering — while keeping all the feedback that matters: hover color changes, pressed-button states, focus outlines, and the dark/light theme switch.

## What exists today

`src/styles.css` already has a small reduced-motion block, but it only shortens animations to 1 millisecond. That still leaves gaps:

- Page-entry and staggered card animations still technically run (a flash of motion).
- The loading shimmer would flicker rapidly instead of resting.
- The arrow that slides on quick-action cards still moves (it animates via a parent hover, which the current rule doesn't cover).
- The theme-switch color fade still animates.

## Changes

All in `src/styles.css`, inside the existing `@media (prefers-reduced-motion: reduce)` block:

1. **Stop animations outright** — set `animation: none` (not just 1ms duration) for page entry, staggered children, tab panels, expandable sections, and the shimmer. Content simply appears in its final state.
2. **Stop hover movement** — extend the existing no-transform rule to also cover the sliding arrow on quick-action cards and any other child elements that move on hover.
3. **Instant theme switch** — disable the `.theme-transition` color fade when reduced motion is requested; colors change immediately.
4. **Keep essential feedback** — color/opacity changes on hover and press, focus rings, and state changes (open/closed, active tab) remain instant but fully visible. Nothing becomes hidden or unusable.

No component files need changes; this is purely a strengthening of the existing CSS rule.

## Testing

- Add a test in `src/test/navigation.test.tsx` that emulates `prefers-reduced-motion: reduce` and confirms pages render fully visible (no element stuck at opacity 0) and navigation still works.
- Re-run the existing 6 navigation tests.
- Browser check with reduced motion emulated at mobile and desktop widths: open pages, switch tabs, toggle theme — everything appears instantly with no motion, and hover/press feedback still reads clearly.
