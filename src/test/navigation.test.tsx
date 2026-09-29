import { QueryClient } from '@tanstack/react-query';
import { createMemoryHistory, createRootRoute, createRoute, createRouter, Outlet, RouterProvider } from '@tanstack/react-router';
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { nav } from '../lib/medarcy-data';
import { AppShell } from '../components/medarcy/shell';
import { Index } from '../routes/index';
import { ClinicalReview } from '../routes/clinical-review';

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
  const routes = nav.map(({ to, label }) => createRoute({
    getParentRoute: () => root,
    path: to,
    component: to === '/' ? Index : to === '/clinical-review' ? ClinicalReview : () => <h1>{label}</h1>,
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

  it('searches workspaces and opens the profile menu without context errors', async () => {
    const user = userEvent.setup();
    await renderAt('/');
    await user.type(screen.getByRole('textbox', { name: 'Global search' }), 'Medication safety');
    expect((await screen.findAllByText('Demo interaction screen')).some((item) => item.closest('a')?.getAttribute('href') === '/drug-intelligence')).toBe(true);
    await user.click(screen.getByRole('button', { name: 'Profile menu' }));
    expect(await screen.findByRole('menuitem', { name: 'Profile settings' })).toBeInTheDocument();
    await user.keyboard('{Escape}');
    expect(screen.queryByRole('menuitem', { name: 'Profile settings' })).not.toBeInTheDocument();
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
    await renderAt('/clinical-review');
    await user.click(screen.getByRole('button', { name: 'Switch to dark mode' }));
    expect(document.documentElement).toHaveClass('dark');
    expect(localStorage.getItem('medarcy-theme')).toBe('dark');
    expect(screen.getByRole('button', { name: 'Switch to light mode' })).toHaveAttribute('aria-pressed', 'true');
    await user.click(screen.getByRole('button', { name: 'Approve Review' }));
    const dialog = await screen.findByRole('dialog', { name: 'Confirm clinician review' });
    expect(dialog).toBeInTheDocument();
    await user.click(within(dialog).getByRole('button', { name: 'Cancel' }));
    await user.click(screen.getByRole('button', { name: 'Switch to light mode' }));
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
    await user.click(screen.getByRole('button', { name: 'Switch to dark mode' }));
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