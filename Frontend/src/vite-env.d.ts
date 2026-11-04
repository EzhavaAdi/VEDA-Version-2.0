/// <reference types="vite/client" />

/**
 * VEDA V2 — Vite Environment Variable Type Declarations
 * Extends ImportMetaEnv with all VITE_* variables used in this project.
 */
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_APP_NAME: string
  readonly VITE_APP_ENV: 'development' | 'staging' | 'production'
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
