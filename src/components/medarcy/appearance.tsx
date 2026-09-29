import { createContext, useContext } from 'react';

type Appearance = { dark: boolean; setAppearance: (mode: 'light' | 'dark') => void };

export const AppearanceContext = createContext<Appearance | null>(null);

export function useAppearance() {
  const appearance = useContext(AppearanceContext);
  if (!appearance) throw new Error('Appearance controls must be inside the Medarcy shell.');
  return appearance;
}