import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type ThemeMode = 'light' | 'dark' | 'system';

interface ThemeState {
  theme: ThemeMode;
  setTheme: (theme: ThemeMode) => void;
  resolved: 'light' | 'dark';
  resolve: () => 'light' | 'dark';
  apply: () => void;
}

function getSystemTheme(): 'light' | 'dark' {
  if (typeof window === 'undefined') return 'dark';
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyDom(theme: ThemeMode) {
  if (typeof document === 'undefined') return;
  const root = document.documentElement;
  root.classList.remove('light', 'dark');
  if (theme === 'system') {
    const resolved = getSystemTheme();
    root.classList.add(resolved);
  } else {
    root.classList.add(theme);
  }
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      theme: 'system',
      resolved: 'dark',
      setTheme: (theme) => {
        set({ theme, resolved: theme === 'system' ? getSystemTheme() : theme });
        applyDom(theme);
      },
      resolve: () => {
        const t = get().theme;
        return t === 'system' ? getSystemTheme() : t;
      },
      apply: () => {
        const t = get().theme;
        const resolved = t === 'system' ? getSystemTheme() : t;
        set({ resolved });
        applyDom(t);
      }
    }),
    {
      name: 'nevara-theme',
      partialize: (s) => ({ theme: s.theme }),
      onRehydrateStorage: () => (state) => {
        state?.apply();
      }
    }
  )
);

export function initTheme() {
  const store = useThemeStore.getState();
  store.apply();

  if (typeof window !== 'undefined') {
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const onChange = () => {
      if (useThemeStore.getState().theme === 'system') {
        useThemeStore.getState().apply();
      }
    };
    mq.addEventListener?.('change', onChange);
  }
}
