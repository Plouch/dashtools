/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

interface ImportMetaEnv {
  readonly VITE_PORT?: string
  readonly VITE_API_URL?: string
  readonly VITE_DEFAULT_THEME?: string
  readonly VITE_DEFAULT_THEME_VARIANT?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
  readonly url: string
}

