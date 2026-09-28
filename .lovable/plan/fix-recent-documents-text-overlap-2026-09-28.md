# Fix Recent documents text overlap

## Change
- Adjust only the document rows on the Knowledge Base page so each row grows to fit its title and collection/date text instead of forcing the shared button's fixed height.
- Keep the existing document selection, tags, styling, and sample content; allow long text to wrap or truncate safely at narrow widths without colliding with adjacent rows.

## Verify
- Check the Recent documents list at the reported 962px width and at mobile and desktop widths, including long labels and document selection.
- Confirm rows no longer overlap or cause horizontal scrolling.

## Technical detail
- The document rows use the shared Button component's default `h-9` and `whitespace-nowrap` styles, while each row contains a two-line text block taller than 36px. Override those dimensions on the Knowledge Base row instances rather than changing Button globally.
