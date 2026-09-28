import { defineMcp } from '@lovable.dev/mcp-js';
import listWorkspaces from './tools/list-workspaces';
import searchSampleEvidence from './tools/search-sample-evidence';

export default defineMcp({
  name: 'medarcy-clinical-intelligence',
  title: 'Medarcy: Clinical Intelligence',
  version: '0.1.0',
  instructions: 'Read-only tools for exploring the public Medarcy visual prototype. All evidence records are fictional samples, not verified medical sources. Never present results as clinical advice, actual citations, or a substitute for clinician judgment. Do not submit patient data.',
  tools: [listWorkspaces, searchSampleEvidence],
});