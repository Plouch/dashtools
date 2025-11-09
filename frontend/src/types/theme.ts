/**
 * Theme type definitions
 */

export type ThemeName = 'rose-pine' | 'everforest'
export type ThemeVariant = 'light' | 'dark'

export interface Theme {
  name: ThemeName
  variant: ThemeVariant
}

export const THEMES: Theme[] = [
  { name: 'rose-pine', variant: 'light' },
  { name: 'rose-pine', variant: 'dark' },
  { name: 'everforest', variant: 'light' },
  { name: 'everforest', variant: 'dark' },
]

