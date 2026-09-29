import { createFileRoute } from '@tanstack/react-router';
import { Moon, Sun } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { PageHeading } from '@/components/medarcy/primitives';
import { useAppearance } from '@/components/medarcy/appearance';
import { meta } from '@/lib/medarcy-data';

export const Route = createFileRoute('/settings')({
  head: () => meta('Settings', 'Manage appearance and view profile and service information for the Medarcy interface demo.', '/settings'),
  component: Settings,
});

export function Settings() {
  const { dark, setAppearance } = useAppearance();
  return <div className="space-y-8">
    <PageHeading eyebrow="Workspace / Preferences" title="Settings" description="Your workspace preferences and information." />
    <div className="max-w-3xl divide-y divide-border">
      <section aria-labelledby="profile-heading" className="grid gap-4 py-7 first:pt-0 sm:grid-cols-[180px_1fr]">
        <div><h2 id="profile-heading" className="text-base font-semibold">Profile</h2><p className="mt-1 text-xs text-muted-foreground">Sample workspace</p></div>
        <div className="flex items-center gap-3"><span className="grid size-10 shrink-0 place-items-center rounded-full bg-secondary text-xs font-semibold">DR</span><div><p className="text-sm font-medium">Doctor Workspace</p><p className="text-xs text-muted-foreground">Interface demo · No personal account is connected.</p></div></div>
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