import type { ReactNode } from 'react';
import { AlertTriangle, ArrowUpRight, FlaskConical } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';

export function PageHeading({ eyebrow, title, description, action }: { eyebrow: string; title: string; description: string; action?: ReactNode }) {
  return <div className="flex flex-col gap-5 border-b border-border pb-7 sm:flex-row sm:items-end sm:justify-between"><div className="min-w-0"><div className="mb-3 flex items-center gap-2 text-[11px] font-semibold uppercase text-muted-foreground tracking-widest"><span className="h-1.5 w-1.5 rounded-full bg-teal" />{eyebrow}</div><h1 className="font-display text-[28px] font-semibold text-foreground sm:text-[34px]">{title}</h1><p className="mt-2 max-w-2xl text-sm leading-6 text-muted-foreground">{description}</p></div>{action && <div className="shrink-0">{action}</div>}</div>;
}
export function SampleBadge() { return <span className="inline-flex items-center gap-1.5 rounded border border-gold/30 bg-gold-soft px-2 py-1 text-[10px] font-semibold uppercase text-gold-foreground tracking-wider"><FlaskConical className="size-3" /> Sample content</span>; }
export function SectionTitle({ title, action }: { title: string; action?: ReactNode }) { return <div className="mb-4 flex items-center justify-between gap-3"><h2 className="text-base font-semibold text-foreground">{title}</h2>{action}</div>; }
export function Notice({ children }: { children: ReactNode }) { return <div className="flex gap-3 border-l-2 border-gold bg-gold-soft p-4 text-xs leading-5 text-foreground"><AlertTriangle className="mt-0.5 size-4 shrink-0 text-gold-foreground" />{children}</div>; }
export function DemoButton({ label, message, icon: Icon = ArrowUpRight, variant = 'outline' }: { label: string; message?: string; icon?: typeof ArrowUpRight; variant?: 'outline' | 'default' | 'ghost' }) { return <Button variant={variant} onClick={() => toast.info(message ?? `${label} is available in this interface demo only.`)}><Icon />{label}</Button>; }
export function EmptyState({ query }: { query: string }) { return <div className="border border-dashed border-border px-6 py-14 text-center"><p className="font-medium">No sample results for “{query}”</p><p className="mt-2 text-sm text-muted-foreground">Try another term or clear the search.</p></div>; }
