import { Link, useNavigate, useRouterState } from '@tanstack/react-router';
import { useState, useEffect, type ReactNode } from 'react';
import { Bell, ChevronDown, Command, Menu, PanelLeftClose, PanelLeftOpen, Plus, Search, Settings as SettingsIcon, X } from 'lucide-react';
import { nav, sessions } from '@/lib/medarcy-data';
import { Button, buttonVariants } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Toaster } from '@/components/ui/sonner';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { toast } from 'sonner';
import lightLogo from '@/assets/medarcy-light-full.png.asset.json';
import darkLogo from '@/assets/medarcy-dark-full.png.asset.json';
import lightMark from '@/assets/medarcy-light-mark.png.asset.json';
import darkMark from '@/assets/medarcy-dark-mark.png.asset.json';
import { AppearanceContext } from './appearance';
import { ProfileContext } from './profile';
import { defaultProfile, profileInitials, profileSchema, PROFILE_STORAGE_KEY, readProfile, type Profile } from '@/lib/profile';

export function AppShell({ children }: { children: ReactNode }) {
  const path = useRouterState({ select: (s) => s.location.pathname });
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [search, setSearch] = useState('');
  const [searchOpen, setSearchOpen] = useState(false);
  const [dark, setDark] = useState(false);
  const [profile, setProfile] = useState<Profile>(defaultProfile);
  useEffect(() => { setDark(document.documentElement.classList.contains('dark')); }, []);
  useEffect(() => { setProfile(readProfile()); }, []);
  const saveProfile = (draft: Profile) => {
    const parsed = profileSchema.safeParse(draft);
    if (!parsed.success) return false;
    try {
      localStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(parsed.data));
      setProfile(parsed.data);
      return true;
    } catch { return false; }
  };
  const setAppearance = (mode: 'light' | 'dark') => {
    const next = mode === 'dark';
    const root = document.documentElement;
    root.classList.add('theme-transition');
    window.setTimeout(() => root.classList.remove('theme-transition'), 400);
    root.classList.toggle('dark', next);
    document.documentElement.style.colorScheme = next ? 'dark' : 'light';
    setDark(next);
    try { localStorage.setItem('medarcy-theme', mode); } catch (_) { /* Appearance still changes when storage is unavailable. */ }
  };
  useEffect(() => { setMobileOpen(false); setSearchOpen(false); }, [path]);
  const current = path === '/settings' ? 'Settings' : nav.find((item) => item.to === path)?.label ?? 'Workspace';
  const results = [...nav.map((item) => ({ label: item.label, to: item.to, detail: 'Workspace' })), { label: 'Settings', to: '/settings' as const, detail: 'Preferences and about' }, ...sessions.map((item) => ({ label: item.title, to: item.to, detail: item.detail }))].filter((item) => `${item.label} ${item.detail}`.toLowerCase().includes(search.toLowerCase()));
  return <AppearanceContext.Provider value={{ dark, setAppearance }}><ProfileContext.Provider value={{ profile, saveProfile }}><div className="min-h-screen bg-background text-foreground">
    {mobileOpen && <div className="fixed inset-0 z-40 bg-overlay lg:hidden" onClick={() => setMobileOpen(false)} aria-hidden="true" />}
    <aside className={`fixed inset-y-0 left-0 z-50 flex flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground transition-[width,transform] duration-200 ${collapsed ? 'lg:w-[76px]' : 'lg:w-[252px]'} w-[252px] ${mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}>
       <div className={`relative flex h-[148px] shrink-0 items-center justify-center border-b border-sidebar-border bg-card px-4 dark:bg-sidebar ${collapsed ? 'lg:h-[80px] lg:px-2' : ''}`}>
         <Link to="/" className="flex min-w-0 flex-col items-center gap-1" aria-label="Medarcy workspace" onClick={() => setMobileOpen(false)}>
           <span className={collapsed ? 'lg:hidden' : ''}>
             <img src={lightLogo.url} alt="Medarcy logo" className="h-[98px] w-[114px] object-contain dark:hidden" />
             <img src={darkLogo.url} alt="Medarcy logo" className="hidden h-[98px] w-[114px] object-contain dark:block" />
           </span>
           <span className={`text-center text-[9px] font-semibold uppercase text-sidebar-action-foreground dark:text-sidebar-muted tracking-widest ${collapsed ? 'lg:hidden' : ''}`}>Clinical Intelligence Platform</span>
           <span className={collapsed ? 'hidden lg:block' : 'hidden'}>
             <img src={lightMark.url} alt="Medarcy logo" className="size-11 object-contain dark:hidden" />
             <img src={darkMark.url} alt="Medarcy logo" className="hidden size-11 object-contain dark:block" />
           </span>
         </Link>
         <Button variant="ghost" size="icon" className="absolute right-2 top-2 text-sidebar-action-foreground dark:text-sidebar-muted lg:hidden" aria-label="Close navigation" onClick={() => setMobileOpen(false)}><X /></Button>
      </div>
      <div className="px-4 pt-5"><Link to="/" onClick={() => setMobileOpen(false)} className={buttonVariants({ className: `h-10 w-full justify-start bg-sidebar-action text-sidebar-action-foreground hover:bg-sidebar-action/90 ${collapsed ? 'lg:justify-center lg:px-0' : ''}` })}><Plus className="size-4 shrink-0" /><span className={collapsed ? 'lg:hidden' : ''}>New Session</span></Link></div>
      <nav className="mt-8 flex-1 overflow-y-auto px-3" aria-label="Workspace navigation"><p className={`mb-3 px-3 text-[10px] font-semibold uppercase text-sidebar-muted tracking-widest ${collapsed ? 'lg:hidden' : ''}`}>Workspace</p><div className="space-y-1">{nav.map(({ label, to, icon: Icon }) => <Link key={to} to={to} title={label} className={`flex h-10 items-center gap-3 rounded-md px-3 text-[13px] transition-colors ${collapsed ? 'lg:justify-center' : ''} ${path === to ? 'bg-sidebar-accent text-sidebar-foreground font-medium' : 'text-sidebar-muted hover:bg-sidebar-accent hover:text-sidebar-foreground'}`}><Icon className={`size-[17px] shrink-0 ${path === to ? 'text-gold' : ''}`} strokeWidth={1.8} /><span className={collapsed ? 'lg:hidden' : ''}>{label}</span></Link>)}</div>
      <div className={`mt-9 ${collapsed ? 'lg:hidden' : ''}`}><p className="mb-3 px-3 text-[10px] font-semibold uppercase text-sidebar-muted tracking-widest">Recent sessions</p>{sessions.slice(0, 3).map((item) => <Link to={item.to} key={item.title} className="block truncate rounded-md px-3 py-2 text-xs text-sidebar-muted hover:bg-sidebar-accent hover:text-sidebar-foreground">{item.title}</Link>)}</div></nav>
       <div className="border-t border-sidebar-border p-3"><Link to="/settings" title="Settings" onClick={() => setMobileOpen(false)} className={`mb-2 flex h-10 items-center gap-3 rounded-md px-3 text-[13px] transition-colors ${collapsed ? 'lg:justify-center' : ''} ${path === '/settings' ? 'bg-sidebar-accent text-sidebar-foreground font-medium' : 'text-sidebar-muted hover:bg-sidebar-accent hover:text-sidebar-foreground'}`}><SettingsIcon className="size-[17px] shrink-0" strokeWidth={1.8} /><span className={collapsed ? 'lg:hidden' : ''}>Settings</span></Link><div className={`flex items-center gap-3 rounded-md px-2 py-2 ${collapsed ? 'lg:justify-center' : ''}`}><span className="grid size-8 shrink-0 place-items-center rounded-full bg-sidebar-accent text-xs font-semibold text-sidebar-foreground">{profileInitials(profile.displayName)}</span><div className={`min-w-0 flex-1 ${collapsed ? 'lg:hidden' : ''}`}><p className="truncate text-xs font-medium">{profile.displayName}</p><p className="truncate text-[11px] text-sidebar-muted">{profile.clinicalRole || 'Interface demo'}</p></div><ChevronDown className={`size-3 text-sidebar-muted ${collapsed ? 'lg:hidden' : ''}`} /></div></div>
    </aside>
    <div className={`min-w-0 transition-[margin] duration-200 ${collapsed ? 'lg:ml-[76px]' : 'lg:ml-[252px]'}`}>
      <header className="sticky top-0 z-30 flex h-[72px] items-center justify-between gap-3 border-b border-border bg-background/95 px-4 backdrop-blur-sm sm:px-8">
        <div className="flex min-w-0 items-center gap-3"><Button variant="ghost" size="icon" className="shrink-0 lg:hidden" aria-label="Open navigation" onClick={() => setMobileOpen(true)}><Menu /></Button><Button variant="ghost" size="icon" className="hidden shrink-0 text-muted-foreground lg:inline-flex" aria-label={collapsed ? 'Expand navigation' : 'Collapse navigation'} title={collapsed ? 'Expand navigation' : 'Collapse navigation'} onClick={() => setCollapsed(!collapsed)}>{collapsed ? <PanelLeftOpen /> : <PanelLeftClose />}</Button><div className="min-w-0"><p className="truncate text-sm font-semibold sm:text-base">{current}</p><p className="truncate text-[10px] text-muted-foreground sm:text-[11px]">Medarcy · Clinical Intelligence Workspace</p></div></div>
        <div className="flex items-center gap-1 sm:gap-2"><div className="relative"><div className="hidden w-[230px] items-center gap-2 rounded-md border border-input bg-muted/40 px-3 md:flex"><Search className="size-4 shrink-0 text-muted-foreground" /><Input aria-label="Global search" placeholder="Search workspace..." value={search} onFocus={() => setSearchOpen(true)} onChange={(e) => { setSearch(e.target.value); setSearchOpen(true); }} className="h-9 border-0 bg-transparent px-0 text-xs shadow-none focus-visible:ring-0" /></div><Button variant="ghost" size="icon" className="md:hidden" aria-label="Search workspace" onClick={() => setSearchOpen(!searchOpen)}><Search /></Button>{searchOpen && <div className="absolute right-0 top-11 z-50 w-[min(90vw,340px)] border border-border bg-popover p-2 shadow-lg"><div className="flex items-center gap-2 md:hidden"><Input autoFocus aria-label="Search workspaces and sessions" placeholder="Search..." value={search} onChange={(e) => setSearch(e.target.value)} /><Button variant="ghost" size="icon" aria-label="Close search" onClick={() => setSearchOpen(false)}><X /></Button></div><p className="px-2 py-2 text-[10px] font-semibold uppercase text-muted-foreground tracking-widest">Workspaces & sample sessions</p><div className="max-h-72 overflow-y-auto">{results.length ? results.map((item, index) => <Link to={item.to} key={`${item.label}-${index}`} className="block rounded px-2 py-2 hover:bg-muted"><span className="block text-xs font-medium">{item.label}</span><span className="text-[11px] text-muted-foreground">{item.detail}</span></Link>) : <p className="px-2 py-4 text-xs text-muted-foreground">No matches in this demo.</p>}</div></div>}</div>
           <Button variant="ghost" size="icon" aria-label="Notifications" title="Notifications" onClick={() => toast.info('No notifications in this interface demo.')}><Bell /></Button><DropdownMenu><DropdownMenuTrigger aria-label="Profile menu" title="Profile menu" className={buttonVariants({ variant: 'ghost', size: 'icon', className: 'rounded-full' })}><span className="grid size-8 place-items-center rounded-full bg-secondary text-xs font-semibold">{profileInitials(profile.displayName)}</span></DropdownMenuTrigger><DropdownMenuContent align="end" className="w-52"><DropdownMenuLabel>{profile.displayName}<span className="block text-xs font-normal text-muted-foreground">{profile.clinicalRole || 'Interface demo'}{profile.specialty ? ` · ${profile.specialty}` : ''}</span></DropdownMenuLabel><DropdownMenuSeparator /><DropdownMenuItem onSelect={() => navigate({ to: '/settings' })}>Settings</DropdownMenuItem><DropdownMenuItem onClick={() => toast.info('Authentication is not part of this prototype.')}>Sign out</DropdownMenuItem></DropdownMenuContent></DropdownMenu></div>
      </header>
      <main key={path} className="page-enter mx-auto w-full max-w-[1540px] px-4 py-7 sm:px-8 sm:py-9 xl:px-10">{children}</main>
      <footer className="mx-auto flex max-w-[1540px] items-center justify-between gap-3 border-t border-border px-4 py-5 text-[11px] text-muted-foreground sm:px-8 xl:px-10"><span>© Medarcy · Clinical Intelligence Platform</span><span className="hidden items-center gap-1 sm:flex"><Command className="size-3" /> Interface prototype · No live clinical analysis</span></footer>
     </div><Toaster position="bottom-right" theme={dark ? 'dark' : 'light'} />
  </div></ProfileContext.Provider></AppearanceContext.Provider>;
}
