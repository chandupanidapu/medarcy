import { QueryClient } from '@tanstack/react-query';
import { createMemoryHistory, createRootRoute, createRoute, createRouter, Outlet, RouterProvider } from '@tanstack/react-router';
import { cleanup, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { nav, quickActions } from '../lib/medarcy-data';
import { AppShell } from '../components/medarcy/shell';
import { Index } from '../routes/index';
import { ClinicalReview } from '../routes/clinical-review';
import { Settings } from '../routes/settings';
import { PROFILE_STORAGE_KEY } from '../lib/profile';

let consoleErrors: string[] = [];
let uncaughtErrors: string[] = [];

beforeEach(() => {
  consoleErrors = [];
  uncaughtErrors = [];
  vi.spyOn(console, 'error').mockImplementation((...args) => consoleErrors.push(args.map(String).join(' ')));
  window.addEventListener('error', captureError);
  window.addEventListener('unhandledrejection', captureRejection);
});

afterEach(() => {
  window.removeEventListener('error', captureError);
  window.removeEventListener('unhandledrejection', captureRejection);
  expect(consoleErrors, `React console errors: ${consoleErrors.join('\n')}`).toEqual([]);
  expect(uncaughtErrors, `Uncaught errors: ${uncaughtErrors.join('\n')}`).toEqual([]);
});

function captureError(event: ErrorEvent) { uncaughtErrors.push(event.message); }
function captureRejection(event: PromiseRejectionEvent) { uncaughtErrors.push(String(event.reason)); }

async function renderAt(path: string) {
  const root = createRootRoute({ component: () => <AppShell><Outlet /></AppShell> });
  const routes = [...nav, { to: '/settings', label: 'Settings' }].map(({ to, label }) => createRoute({
    getParentRoute: () => root,
    path: to,
    component: to === '/' ? Index : to === '/clinical-review' ? ClinicalReview : to === '/settings' ? Settings : () => <h1>{label}</h1>,
  }));
  const router = createRouter({
    routeTree: root.addChildren(routes),
    history: createMemoryHistory({ initialEntries: [path] }),
    context: { queryClient: new QueryClient() },
    defaultPreloadStaleTime: 0,
  });
  render(<RouterProvider router={router} />);
  await screen.findByRole('heading', { level: 1 });
  return router;
}

describe('Medarcy navigation and interactive controls', () => {
  it('renders every workspace link and navigates to a clinical workspace', async () => {
    const user = userEvent.setup();
    await renderAt('/');
    const navigation = screen.getByRole('navigation', { name: 'Workspace navigation' });
    for (const item of nav) {
      expect(within(navigation).getByRole('link', { name: item.label })).toHaveAttribute('href', item.to);
    }
    expect(within(navigation).getByRole('link', { name: 'Clinical case review' })).toBeInTheDocument();
    await user.click(within(navigation).getByRole('link', { name: 'Clinical Review' }));
    expect(await screen.findByRole('heading', { name: 'Clinical Review', level: 1 })).toBeInTheDocument();
  });

  it('opens the mobile drawer and closes it through New Session', async () => {
    const user = userEvent.setup();
    await renderAt('/clinical-review');
    await user.click(screen.getByRole('button', { name: 'Open navigation' }));
    expect(screen.getByRole('button', { name: 'Close navigation' }).closest('aside')).toHaveClass('translate-x-0');
    await user.click(screen.getByRole('link', { name: 'New Session' }));
    expect(await screen.findByRole('heading', { name: 'Medarcy Clinical Intelligence Workspace', level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Close navigation' }).closest('aside')).toHaveClass('-translate-x-full');
  });

  it('searches workspaces and opens Settings from the profile menu without context errors', async () => {
    const user = userEvent.setup();
    await renderAt('/');
    await user.type(screen.getByRole('textbox', { name: 'Global search' }), 'Medication safety');
    expect((await screen.findAllByText('Demo interaction screen')).some((item) => item.closest('a')?.getAttribute('href') === '/drug-intelligence')).toBe(true);
    await user.click(screen.getByRole('button', { name: 'Profile menu' }));
    await user.click(await screen.findByRole('menuitem', { name: 'Settings' }));
    expect(await screen.findByRole('heading', { name: 'Settings', level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Profile' })).toBeInTheDocument();
    expect(screen.getByText(/Connected clinical services: none/)).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Help' })).not.toBeInTheDocument();
  });

  it('edits and saves a local profile, updates the shell, and restores it after remount', async () => {
    const user = userEvent.setup();
    await renderAt('/settings');
    await user.clear(screen.getByRole('textbox', { name: 'Display name' }));
    await user.click(screen.getByRole('button', { name: 'Save profile' }));
    expect(screen.getByRole('alert')).toHaveTextContent('Enter a display name.');
    expect(localStorage.getItem(PROFILE_STORAGE_KEY)).toBeNull();
    await user.type(screen.getByRole('textbox', { name: 'Display name' }), 'Dr. Maya Patel');
    await user.type(screen.getByRole('textbox', { name: 'Clinical role' }), 'Physician');
    await user.type(screen.getByRole('textbox', { name: 'Specialty' }), 'Internal medicine');
    await user.click(screen.getByRole('button', { name: 'Save profile' }));
    expect(screen.getByRole('status')).toHaveTextContent('Profile saved in this browser.');
    expect(screen.getByRole('textbox', { name: 'Display name' })).toHaveValue('Dr. Maya Patel');
    expect(localStorage.getItem(PROFILE_STORAGE_KEY)).toContain('Internal medicine');
    expect(screen.getByText('Physician · Internal medicine')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Settings' }).parentElement).toHaveTextContent('Dr. Maya Patel');
    await user.click(screen.getByRole('button', { name: 'Profile menu' }));
    expect(await screen.findByText('Dr. Maya Patel', { selector: '[role="menu"] *' })).toBeInTheDocument();
    cleanup();
    await renderAt('/settings');
    expect(await screen.findByRole('textbox', { name: 'Display name' })).toHaveValue('Dr. Maya Patel');
    expect(screen.getByRole('textbox', { name: 'Specialty' })).toHaveValue('Internal medicine');
  });

  it('reports a local storage failure without claiming the profile was saved', async () => {
    const user = userEvent.setup();
    await renderAt('/settings');
    await user.clear(screen.getByRole('textbox', { name: 'Display name' }));
    await user.type(screen.getByRole('textbox', { name: 'Display name' }), 'Dr. Test');
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => { throw new Error('Storage blocked'); });
    await user.click(screen.getByRole('button', { name: 'Save profile' }));
    expect(screen.getByRole('alert')).toHaveTextContent('Could not save in this browser.');
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
  });

  it('downloads the saved profile as a JSON backup file', async () => {
    const user = userEvent.setup();
    await renderAt('/settings');
    await user.clear(screen.getByRole('textbox', { name: 'Display name' }));
    await user.type(screen.getByRole('textbox', { name: 'Display name' }), 'Dr. Maya Patel');
    await user.type(screen.getByRole('textbox', { name: 'Clinical role' }), 'Physician');
    await user.type(screen.getByRole('textbox', { name: 'Specialty' }), 'Internal medicine');
    await user.click(screen.getByRole('button', { name: 'Save profile' }));
    expect(screen.getByRole('status')).toHaveTextContent('Profile saved in this browser.');
    const createObjectURL = vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:mock-download');
    const revokeObjectURL = vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => {});
    const anchorClick = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {});
    await user.click(screen.getByRole('button', { name: 'Download profile' }));
    const blob = createObjectURL.mock.calls[0]?.[0] as Blob;
    const exported = JSON.parse(await blob.text());
    expect(exported.app).toBe('Medarcy');
    expect(exported.type).toBe('profile-backup');
    expect(exported.exportedAt).toEqual(expect.any(String));
    expect(exported.profile).toEqual({ displayName: 'Dr. Maya Patel', clinicalRole: 'Physician', specialty: 'Internal medicine' });
    expect(anchorClick).toHaveBeenCalled();
    expect(revokeObjectURL).toHaveBeenCalledWith('blob:mock-download');
    createObjectURL.mockRestore();
    revokeObjectURL.mockRestore();
    anchorClick.mockRestore();
  });

  it('keeps clinical review approval behind a confirmation dialog', async () => {
    const user = userEvent.setup();
    await renderAt('/clinical-review');
    await user.click(screen.getByRole('button', { name: 'Approve Review' }));
    const dialog = await screen.findByRole('dialog', { name: 'Confirm clinician review' });
    expect(within(dialog).getByText(/records nothing/)).toBeInTheDocument();
    await user.click(within(dialog).getByRole('button', { name: 'Cancel' }));
    expect(screen.getByRole('button', { name: 'Approve Review' })).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Approve Review' }));
    await user.click(within(await screen.findByRole('dialog')).getByRole('button', { name: 'Mark reviewed in demo' }));
    expect(screen.getByRole('button', { name: 'Reviewed in demo' })).toBeInTheDocument();
  });

  it('switches appearance and keeps the selected mode across remounts', async () => {
    const user = userEvent.setup();
    localStorage.removeItem('medarcy-theme');
    document.documentElement.classList.remove('dark');
    await renderAt('/settings');
    await user.click(screen.getByRole('button', { name: 'Dark' }));
    expect(document.documentElement).toHaveClass('dark');
    expect(localStorage.getItem('medarcy-theme')).toBe('dark');
    expect(screen.getByRole('button', { name: 'Dark' })).toHaveAttribute('aria-pressed', 'true');
    await user.click(screen.getByRole('link', { name: 'Clinical Review' }));
    await user.click(screen.getByRole('button', { name: 'Approve Review' }));
    const dialog = await screen.findByRole('dialog', { name: 'Confirm clinician review' });
    expect(dialog).toBeInTheDocument();
    await user.click(within(dialog).getByRole('button', { name: 'Cancel' }));
    await user.click(screen.getByRole('link', { name: 'Settings' }));
    await user.click(screen.getByRole('button', { name: 'Light' }));
    expect(document.documentElement).not.toHaveClass('dark');
    expect(localStorage.getItem('medarcy-theme')).toBe('light');
  });

  it('shows the supplied Medarcy marks in the navigation for each appearance', async () => {
    const user = userEvent.setup();
    await renderAt('/');
    const brand = screen.getByRole('link', { name: 'Medarcy workspace' });
    const images = brand.querySelectorAll('img');
    expect(images).toHaveLength(4);
    expect(images[0]).toHaveAttribute('src', expect.stringContaining('medarcy-light-full.png'));
    expect(images[1]).toHaveAttribute('src', expect.stringContaining('medarcy-dark-full.png'));
    await user.click(screen.getByRole('link', { name: 'Settings' }));
    await user.click(screen.getByRole('button', { name: 'Dark' }));
    expect(document.documentElement).toHaveClass('dark');
    await user.click(screen.getByRole('button', { name: 'Collapse navigation' }));
    expect(images[3]).toHaveAttribute('src', expect.stringContaining('medarcy-dark-mark.png'));
  });

  it('renders fully and navigates when the OS requests reduced motion', async () => {
    const matchMedia = vi.spyOn(window, 'matchMedia').mockImplementation((query: string) => ({
      matches: query.includes('prefers-reduced-motion'),
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }) as MediaQueryList);
    const user = userEvent.setup();
    await renderAt('/');
    expect(screen.getByRole('heading', { name: 'Medarcy Clinical Intelligence Workspace', level: 1 })).toBeVisible();
    for (const { title } of quickActions) {
      expect(screen.getByRole('link', { name: new RegExp(title) })).toBeVisible();
    }
    const navigation = screen.getByRole('navigation', { name: 'Workspace navigation' });
    await user.click(within(navigation).getByRole('link', { name: 'Clinical Review' }));
    expect(await screen.findByRole('heading', { name: 'Clinical Review', level: 1 })).toBeVisible();
    matchMedia.mockRestore();
  });
});