/**
 * Theme composable for managing theme state
 */
import { ref, watch } from 'vue'
import type { ThemeName, ThemeVariant } from '@/types/theme'

const THEME_STORAGE_KEY = 'dashtools-theme'

// Get default theme from environment variables or use defaults
function getDefaultTheme(): { theme: ThemeName; variant: ThemeVariant } {
  const defaultTheme = (import.meta.env.VITE_DEFAULT_THEME || 'rose-pine') as ThemeName
  const defaultVariant = (import.meta.env.VITE_DEFAULT_THEME_VARIANT || 'dark') as ThemeVariant
  
  // Validate theme name
  const validThemes: ThemeName[] = ['rose-pine', 'everforest']
  const validVariants: ThemeVariant[] = ['light', 'dark']
  
  const theme = validThemes.includes(defaultTheme) ? defaultTheme : 'rose-pine'
  const variant = validVariants.includes(defaultVariant) ? defaultVariant : 'dark'
  
  return { theme, variant }
}

// Initialize theme from localStorage or use defaults from env
function loadTheme(): { theme: ThemeName; variant: ThemeVariant } {
  const defaults = getDefaultTheme()
  
  if (typeof window === 'undefined') {
    return defaults
  }
  
  const saved = localStorage.getItem(THEME_STORAGE_KEY)
  if (saved) {
    try {
      const parsed = JSON.parse(saved)
      return {
        theme: parsed.theme || defaults.theme,
        variant: parsed.variant || defaults.variant
      }
    } catch (e) {
      console.error('Failed to load theme from localStorage', e)
    }
  }
  return defaults
}

const { theme: initialTheme, variant: initialVariant } = loadTheme()
const currentTheme = ref<ThemeName>(initialTheme)
const currentVariant = ref<ThemeVariant>(initialVariant)

// Apply theme immediately
function applyTheme(theme: ThemeName, variant: ThemeVariant) {
  if (typeof document !== 'undefined') {
    const root = document.documentElement
    root.setAttribute('data-theme', theme)
    root.setAttribute('data-variant', variant)
  }
}

// Apply initial theme
applyTheme(initialTheme, initialVariant)

export function useTheme() {
  // Watch for theme changes and apply them
  watch([currentTheme, currentVariant], ([theme, variant]) => {
    applyTheme(theme, variant)
    if (typeof window !== 'undefined') {
      localStorage.setItem(THEME_STORAGE_KEY, JSON.stringify({ theme, variant }))
    }
  })

  function setTheme(theme: ThemeName, variant: ThemeVariant) {
    currentTheme.value = theme
    currentVariant.value = variant
  }

  return {
    currentTheme,
    currentVariant,
    setTheme,
  }
}

