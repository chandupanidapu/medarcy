import { createFileRoute } from '@tanstack/react-router';
import { Download, Moon, Sun } from 'lucide-react';
import { toast } from 'sonner';
import { useEffect, useState, type FormEvent } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { PageHeading } from '@/components/medarcy/primitives';
import { useAppearance } from '@/components/medarcy/appearance';
import { useProfile } from '@/components/medarcy/profile';
import { buildProfileExport, profileInitials, profileSchema, type Profile } from '@/lib/profile';
import { meta } from '@/lib/medarcy-data';

export const Route = createFileRoute('/settings')({
  head: () => meta('Settings', 'Edit your local demo profile and manage appearance in Medarcy Settings.', '/settings'),
  component: Settings,
});

export function Settings() {
  const { dark, setAppearance } = useAppearance();
  const { profile, saveProfile } = useProfile();
  const [draft, setDraft] = useState<Profile>(profile);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  useEffect(() => { setDraft(profile); }, [profile]);
  const update = (key: keyof Profile, value: string) => {
    setDraft((current) => ({ ...current, [key]: value }));
    setError('');
    setMessage('');
  };
  const submit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const parsed = profileSchema.safeParse(draft);
    if (!parsed.success) { setError(parsed.error.issues[0]?.message ?? 'Check your profile details.'); return; }
    if (!saveProfile(parsed.data)) { setError('Could not save in this browser. Check your storage settings and try again.'); return; }
    setError('');
    setMessage('Profile saved in this browser.');
  };
  const downloadProfile = () => {
    const json = JSON.stringify(buildProfileExport(profile), null, 2);
    const url = URL.createObjectURL(new Blob([json], { type: 'application/json' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'medarcy-profile.json';
    link.click();
    URL.revokeObjectURL(url);
    toast.success('Profile downloaded.', {
      description: 'Local export of this browser demo workspace details. No patient information included.',
    });
  };
  return <div className="space-y-8">
    <PageHeading eyebrow="Workspace / Preferences" title="Settings" description="Your workspace preferences and information." />
    <div className="max-w-3xl divide-y divide-border">
      <section aria-labelledby="profile-heading" className="grid gap-4 py-7 first:pt-0 sm:grid-cols-[180px_1fr]">
        <div><h2 id="profile-heading" className="text-base font-semibold">Profile</h2><p className="mt-1 text-xs text-muted-foreground">Local demo profile</p></div>
        <div className="min-w-0 space-y-5">
          <div className="flex items-center gap-3"><span className="grid size-10 shrink-0 place-items-center rounded-full bg-secondary text-xs font-semibold">{profileInitials(profile.displayName)}</span><div className="min-w-0"><p className="truncate text-sm font-medium">{profile.displayName}</p><p className="text-xs text-muted-foreground">{[profile.clinicalRole, profile.specialty].filter(Boolean).join(' · ') || 'Interface demo'}</p></div></div>
          <form onSubmit={submit} noValidate className="space-y-4">
            <div className="space-y-1.5"><Label htmlFor="display-name">Display name</Label><Input id="display-name" value={draft.displayName} maxLength={80} aria-invalid={!!error && !draft.displayName.trim()} onChange={(event) => update('displayName', event.target.value)} autoComplete="off" /></div>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-1.5"><Label htmlFor="clinical-role">Clinical role</Label><Input id="clinical-role" value={draft.clinicalRole} maxLength={80} placeholder="e.g. Physician" onChange={(event) => update('clinicalRole', event.target.value)} autoComplete="off" /></div>
              <div className="space-y-1.5"><Label htmlFor="specialty">Specialty</Label><Input id="specialty" value={draft.specialty} maxLength={80} placeholder="e.g. Internal medicine" onChange={(event) => update('specialty', event.target.value)} autoComplete="off" /></div>
            </div>
            <p className="text-xs leading-5 text-muted-foreground">Saved only in this browser. Not verified, synced to an account, or shared across devices. Do not enter patient information.</p>
            {error && <p role="alert" className="text-sm text-destructive">{error}</p>}
            {message && <p role="status" className="text-sm text-primary">{message}</p>}
            <div className="flex flex-wrap gap-2">
              <Button type="button" variant="outline" onClick={downloadProfile}><Download className="size-4" />Download profile</Button>
              <Button type="submit" disabled={JSON.stringify(draft) === JSON.stringify(profile)}>Save profile</Button>
            </div>
          </form>
        </div>
      </section>
      <section aria-labelledby="appearance-heading" className="grid gap-4 py-7 sm:grid-cols-[180px_1fr]">
        <div><h2 id="appearance-heading" className="text-base font-semibold">Appearance</h2><p className="mt-1 text-xs text-muted-foreground">Display preference</p></div>
        <div className="flex flex-wrap gap-2" role="group" aria-label="Appearance">
          <Button variant={!dark ? 'default' : 'outline'} aria-pressed={!dark} onClick={() => setAppearance('light')}><Sun className="size-4" />Light</Button>
          <Button variant={dark ? 'default' : 'outline'} aria-pressed={dark} onClick={() => setAppearance('dark')}><Moon className="size-4" />Dark</Button>
        </div>
      </section>
      <section aria-labelledby="about-heading" className="grid gap-4 py-7 sm:grid-cols-[180px_1fr]">
        <div><h2 id="about-heading" className="text-base font-semibold">About</h2><p className="mt-1 text-xs text-muted-foreground">Medarcy</p></div>
        <div className="space-y-3 text-sm"><p className="font-medium">Clinical Intelligence Platform</p><p className="text-muted-foreground">Connected clinical services: none. This is an interface demo with no live clinical analysis.</p><p className="text-xs leading-5 text-muted-foreground">Clinical decision support only. Verify findings and recommendations before applying them to patient care.</p></div>
      </section>
    </div>
  </div>;
}