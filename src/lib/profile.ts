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