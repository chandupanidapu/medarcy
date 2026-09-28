import { defineTool } from '@lovable.dev/mcp-js';
import { nav } from '../../medarcy-data';

export default defineTool({
  name: 'list_workspaces',
  title: 'List Medarcy workspaces',
  description: 'List the publicly visible workspaces in the Medarcy visual prototype.',
  annotations: { readOnlyHint: true, idempotentHint: true, openWorldHint: false },
  handler: () => ({
    content: [{ type: 'text', text: 'Medarcy is a visual prototype; these workspace links do not provide live clinical services.' }],
    structuredContent: {
      notice: 'Visual prototype only. No clinical analysis, real patient data, or connected medical sources.',
      workspaces: nav.map(({ label, to }) => ({ title: label, path: to })),
    },
  }),
});