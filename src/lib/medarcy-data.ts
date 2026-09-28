import { Activity, BookOpen, ClipboardList, FileText, FlaskConical, History, LayoutGrid, LibraryBig, Pill, SearchCheck, ShieldCheck, Stethoscope, TestTube2 } from 'lucide-react';

export const nav = [
  { label: 'Workspace', to: '/', icon: LayoutGrid },
  { label: 'Clinical Review', to: '/clinical-review', icon: ClipboardList },
  { label: 'Medical Research', to: '/medical-research', icon: BookOpen },
  { label: 'Evidence Engine', to: '/evidence-engine', icon: SearchCheck },
  { label: 'Drug Intelligence', to: '/drug-intelligence', icon: Pill },
  { label: 'Diagnostics', to: '/diagnostics', icon: Activity },
  { label: 'Knowledge Base', to: '/knowledge-base', icon: LibraryBig },
  { label: 'History', to: '/history', icon: History },
] as const;

export const quickActions = [
  { title: 'Review a Patient Case', description: 'Organize findings into a structured review', icon: Stethoscope, to: '/clinical-review' },
  { title: 'Explore Medical Evidence', description: 'Compare source quality and relevance', icon: SearchCheck, to: '/evidence-engine' },
  { title: 'Analyze Laboratory Results', description: 'Interpret findings in clinical context', icon: TestTube2, to: '/diagnostics' },
  { title: 'Review Medication Safety', description: 'Assess warnings and interactions', icon: ShieldCheck, to: '/drug-intelligence' },
  { title: 'Research a Clinical Question', description: 'Frame and compare sample studies', icon: FlaskConical, to: '/medical-research' },
  { title: 'Generate a Clinical Summary', description: 'Review a structured draft report', icon: FileText, to: '/clinical-review' },
] as const;

export const sessions = [
  { title: 'Clinical case review', detail: 'Fictional case · Respiratory symptoms', date: 'Today, 09:42', type: 'Clinical Review', to: '/clinical-review' },
  { title: 'Evidence review', detail: 'Sample literature · Outpatient care', date: 'Yesterday', type: 'Evidence Engine', to: '/evidence-engine' },
  { title: 'Medication safety analysis', detail: 'Demo interaction screen', date: 'Sep 24', type: 'Drug Intelligence', to: '/drug-intelligence' },
  { title: 'Research question', detail: 'Sample study comparison', date: 'Sep 22', type: 'Medical Research', to: '/medical-research' },
] as const;

export const report = [
  { title: 'Executive Summary', text: 'Fictional adult outpatient with four days of cough and fatigue. The sample findings are presented for interface demonstration only; no live clinical analysis has been performed.' },
  { title: 'Clinical Assessment', text: 'The recorded symptoms suggest a respiratory presentation requiring clinician assessment. Consider the overall history, examination, and local protocols before drawing conclusions.' },
  { title: 'Clinical Reasoning', text: 'Fever history, oxygen saturation, symptom duration, and examination findings would influence the clinical interpretation. Missing information limits confidence.' },
  { title: 'Differential Diagnosis', text: 'Possible categories for clinician consideration include self-limited respiratory illness and other respiratory causes. This is not a diagnosis or ranked clinical output.' },
  { title: 'Recommended Investigations', text: 'A clinician may determine whether additional history, examination, or testing is appropriate. No patient-specific investigation is recommended by this prototype.' },
  { title: 'Management Considerations', text: 'Management must follow clinician judgment and applicable local guidance. The demonstration does not prescribe treatment.' },
  { title: 'Medication Considerations', text: 'Reconcile current medications and allergies against trusted prescribing references before any medication decision. No doses are provided.' },
  { title: 'Follow-up', text: 'A clinician should define follow-up based on the full presentation and any evolving symptoms.' },
  { title: 'Patient Education', text: 'Use clear, individualized communication about symptoms, follow-up, and when to seek urgent care, as determined by the clinician.' },
  { title: 'Evidence and References', text: 'No verified sources are connected. References shown in this prototype are explicitly fictional sample entries and must not be used for care.' },
  { title: 'Limitations and Uncertainty', text: 'This report is static sample content. Clinical context is incomplete, sources are not verified, and no live reasoning or safety checks were performed.' },
] as const;

export const studies = [
  { id: 'S-01', title: 'Sample study: Ambulatory respiratory assessment', year: '2024', type: 'Guideline', summary: 'Fictional source record illustrating how clinical guidance might be summarized and traced.', relevance: 'High' },
  { id: 'S-02', title: 'Sample study: Primary care symptom evaluation', year: '2023', type: 'Systematic review', summary: 'Fictional synthesis entry for comparison layout only; not a real publication.', relevance: 'High' },
  { id: 'S-03', title: 'Sample study: Follow-up pathways', year: '2022', type: 'Randomized trial', summary: 'Fictional trial entry to demonstrate evidence comparison. No real findings are represented.', relevance: 'Moderate' },
  { id: 'S-04', title: 'Sample study: Outpatient monitoring', year: '2021', type: 'Observational study', summary: 'Fictional observational source for a sample evidence library.', relevance: 'Moderate' },
  { id: 'S-05', title: 'Sample study: Clinical decision support', year: '2020', type: 'Review', summary: 'Fictional review entry. Verify original sources in a real evidence system.', relevance: 'Lower' },
] as const;

export const meta = (title: string, description: string, path: string) => ({ meta: [
  { title: `${title} | Medarcy` }, { name: 'description', content: description },
  { property: 'og:title', content: `${title} | Medarcy` }, { property: 'og:description', content: description },
  { property: 'og:type', content: 'website' }, { property: 'og:url', content: path }, { name: 'twitter:card', content: 'summary' },
], links: [{ rel: 'canonical', href: path }] });
