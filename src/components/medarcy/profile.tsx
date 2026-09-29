import { createContext, useContext } from 'react';
import type { Profile } from '@/lib/profile';

type ProfileState = { profile: Profile; saveProfile: (profile: Profile) => boolean };

export const ProfileContext = createContext<ProfileState | null>(null);

export function useProfile() {
  const value = useContext(ProfileContext);
  if (!value) throw new Error('Profile controls must be inside the Medarcy shell.');
  return value;
}