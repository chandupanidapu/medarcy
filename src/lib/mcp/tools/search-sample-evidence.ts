import { defineTool } from '@lovable.dev/mcp-js';
import { z } from 'zod';
import { studies } from '../../medarcy-data';

export default defineTool({
  name: 'search_sample_evidence',
  title: 'Search fictional evidence examples',
  description: 'Search Medarcy’s five fictional demonstration study records; these are not real publications.',
  inputSchema: {
    query: z.string().trim().max(100).optional().describe('Optional text to match against sample titles, types, and summaries.'),
  },
  annotations: { readOnlyHint: true, idempotentHint: true, openWorldHint: false },
  handler: ({ query }) => {
    const term = query?.toLocaleLowerCase() ?? '';
    const matches = studies.filter((study) =>
      [study.title, study.type, study.summary].some((value) => value.toLocaleLowerCase().includes(term)),
    );
    return {
      content: [{ type: 'text', text: `${matches.length} fictional sample record(s) found. These are not real publications and must not be cited or used for patient care.` }],
      structuredContent: {
        notice: 'Fictional demonstration content only. No verified medical sources or live search are connected. Do not cite or use for patient care.',
        results: matches.map(({ id, title, year, type, summary, relevance }) => ({ id, title, year, type, summary, relevance })),
      },
    };
  },
});