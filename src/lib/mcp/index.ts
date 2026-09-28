import { auth, defineMcp } from '@lovable.dev/mcp-js';
import listWorkspaces from './tools/list-workspaces';
import searchSampleEvidence from './tools/search-sample-evidence';

// Canonical Lovable Cloud auth issuer (from OpenID discovery). Not a secret.
const OAUTH_ISSUER = 'https://lvivocjfuqhmnsplkwyq.supabase.co/auth/v1';

export default defineMcp({
  name: 'medarcy-clinical-intelligence',
  title: 'Medarcy: Clinical Intelligence',
  version: '0.1.0',
  instructions: 'Read-only tools for exploring the Medarcy visual prototype. Callers must sign in. All evidence records are fictional samples, not verified medical sources. Never present results as clinical advice, actual citations, or a substitute for clinician judgment. Do not submit patient data.',
  auth: auth.oauth.issuer({
    issuer: OAUTH_ISSUER,
    acceptedAudiences: 'authenticated',
    jwksUri: `${OAUTH_ISSUER}/.well-known/jwks.json`,
  }),
  tools: [listWorkspaces, searchSampleEvidence],
});
