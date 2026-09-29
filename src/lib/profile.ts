import { z } from 'zod';

export const PROFILE_STORAGE_KEY = 'medarcy-profile-v1';

export const profileSchema = z.object({
  displayName: z.string().trim().min(1, 'Enter a display name.').max(80, 'Keep the name under 80 characters.'),
  clinicalRole: z.string().trim().max(80, 'Keep the role under 80 characters.'),
  specialty: z.string().trim().max(80, 'Keep the specialty under 80 characters.'),
});

export type Profile = z.infer<typeof profileSchema>;

export const defaultProfile: Profile = { displayName: 'Doctor Workspace', clinicalRole: '', specialty: '' };

export function readProfile(): Profile {
  try {
    const stored = window.localStorage.getItem(PROFILE_STORAGE_KEY);
    if (stored) {
      const parsed = profileSchema.safeParse(JSON.parse(stored));
      if (parsed.success) return parsed.data;
    }
  } catch { /* Storage may be blocked or contain invalid data. */ }
  return defaultProfile;
}

export function profileInitials(name: string) {
  return name.trim().split(/\s+/).slice(0, 2).map((word) => word[0]?.toUpperCase() ?? '').join('');
}

export function buildProfileExport(profile: Profile) {
  return {
    app: 'Medarcy',
    type: 'profile-backup',
    exportedAt: new Date().toISOString(),
    profile: {
      displayName: profile.displayName,
      clinicalRole: profile.clinicalRole,
      specialty: profile.specialty,
    },
  };
}

export type ProfileImportResult = { ok: true; profile: Profile } | { ok: false; error: string };

export function parseProfileImport(json: string): ProfileImportResult {
  let data: unknown;
  try {
    data = JSON.parse(json);
  } catch {
    return { ok: false, error: 'That file is not valid JSON. Choose a Medarcy profile backup file.' };
  }
  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    return { ok: false, error: 'That file is not a Medarcy profile backup.' };
  }
  const record = data as Record<string, unknown>;
  const candidate = 'profile' in record ? record['profile'] : record;
  const parsed = profileSchema.safeParse(candidate);
  if (!parsed.success) {
    return { ok: false, error: parsed.error.issues[0]?.message ?? 'The profile details in that file are not valid.' };
  }
  return { ok: true, profile: parsed.data };
}