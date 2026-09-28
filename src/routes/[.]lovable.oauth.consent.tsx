import { createFileRoute } from '@tanstack/react-router';
import { useEffect, useState } from 'react';
import { supabase } from '@/integrations/supabase/client';
import { Button } from '@/components/ui/button';

type Details = { client?: { name?: string; client_name?: string; redirect_uri?: string } | null; scope?: string; redirect_url?: string; redirect_to?: string };
type OAuthApi = {
  getAuthorizationDetails(id: string): Promise<{ data: Details | null; error: { message: string } | null }>;
  approveAuthorization(id: string): Promise<{ data: { redirect_url?: string; redirect_to?: string } | null; error: { message: string } | null }>;
  denyAuthorization(id: string): Promise<{ data: { redirect_url?: string; redirect_to?: string } | null; error: { message: string } | null }>;
};
const oauth = () => (supabase.auth as unknown as { oauth: OAuthApi }).oauth;

export const Route = createFileRoute('/.lovable/oauth/consent')({
  head: () => ({
    meta: [
      { title: 'Authorize agent · Medarcy' },
      { name: 'description', content: 'Approve or deny an agent connection to Medarcy.' },
      { property: 'og:title', content: 'Authorize agent · Medarcy' },
      { property: 'og:description', content: 'Approve or deny an agent connection to Medarcy.' },
      { property: 'og:type', content: 'website' },
      { name: 'twitter:card', content: 'summary' },
    ],
  }),
  errorComponent: () => <p className="py-10 text-sm text-destructive">Something went wrong loading this authorization. Please retry from your agent.</p>,
  component: Consent,
});

function Consent() {
  const [state, setState] = useState<'loading' | 'ready' | 'error' | 'busy'>('loading');
  const [details, setDetails] = useState<Details | null>(null);
  const [email, setEmail] = useState<string>('');
  const [error, setError] = useState('');
  const [id, setId] = useState('');

  useEffect(() => {
    const authId = new URLSearchParams(window.location.search).get('authorization_id');
    if (!authId) { setError('This authorization link is invalid or expired.'); setState('error'); return; }
    setId(authId);
    (async () => {
      const { data } = await supabase.auth.getSession();
      if (!data.session) {
        const next = window.location.pathname + window.location.search;
        window.location.href = `/auth?next=${encodeURIComponent(next)}`;
        return;
      }
      setEmail(data.session.user.email ?? '');
      const res = await oauth().getAuthorizationDetails(authId);
      if (res.error) { setError('This authorization link is invalid or expired.'); setState('error'); return; }
      const redirect = res.data?.redirect_url ?? res.data?.redirect_to;
      if (redirect && !res.data?.client) { window.location.href = redirect; return; }
      setDetails(res.data); setState('ready');
    })();
  }, []);

  async function decide(approve: boolean) {
    setState('busy');
    const res = approve ? await oauth().approveAuthorization(id) : await oauth().denyAuthorization(id);
    const redirect = res.data?.redirect_url ?? res.data?.redirect_to;
    if (res.error || !redirect) { setError(approve ? 'Approval failed. Please retry.' : 'Could not cancel. Please retry.'); setState('error'); return; }
    window.location.href = redirect;
  }

  if (state === 'loading') return <p className="py-10 text-sm text-muted-foreground">Loading authorization…</p>;
  if (state === 'error') return <p className="py-10 text-sm text-destructive">{error}</p>;

  const name = details?.client?.client_name ?? details?.client?.name ?? 'An agent';
  const scopes = (details?.scope ?? '').split(' ').filter(Boolean);
  const label = (s: string) => s === 'openid' ? 'Confirm your identity' : s === 'email' ? 'Share your email address' : s === 'profile' ? 'Share your basic profile' : `Additional permission requested: ${s}`;

  return (
    <div className="mx-auto w-full max-w-md py-10">
      <h1 className="text-xl font-semibold text-foreground">Connect {name} to Medarcy</h1>
      <p className="mt-2 text-sm text-muted-foreground">Signed in as {email}. {name} will be able to call Medarcy's read-only sample tools as you.</p>
      {details?.client?.redirect_uri && <p className="mt-2 break-all text-xs text-muted-foreground">Redirects to {details.client.redirect_uri}</p>}
      {scopes.length > 0 && <ul className="mt-4 list-disc space-y-1 pl-5 text-sm text-foreground">{scopes.map((s) => <li key={s}>{label(s)}</li>)}</ul>}
      <p className="mt-4 text-xs text-muted-foreground">This does not bypass Medarcy's permissions. Tools return fictional sample content only.</p>
      <div className="mt-6 flex gap-3">
        <Button onClick={() => decide(true)} disabled={state === 'busy'}>Approve</Button>
        <Button variant="outline" onClick={() => decide(false)} disabled={state === 'busy'}>Cancel connection</Button>
      </div>
    </div>
  );
}
