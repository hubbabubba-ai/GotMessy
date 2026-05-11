/**
 * Got Messy brand color tokens.
 * Source of truth: the :root block in Final/gotmessy-brand-guidelines.html
 * Regenerate with: python3 scripts/generate-tokens.py
 * Drift check runs in CI via scripts/check-token-drift.py.
 */

export const colors = {
  /** Primary text on dark backgrounds */
  cream: '#FAF7F2',
  /** Warm neutral / light-mode page background */
  warm: '#F2EDE4',
  /** Default page background (dark) */
  ink: '#1A1612',
  /** Secondary background */
  inkSoft: '#3D3530',
  /** Muted text / labels / metadata */
  dust: '#C4B5A0',
  /** Primary accent — links, buttons, terminal dot */
  clay: '#C4673A',
  /** Clay hover / pressed state */
  clayDk: '#9B4A28',
  /** Clay focus ring / large hero accents */
  clayLt: '#E8896A',
  /** Success / live status */
  sage: '#5C7A62',
  /** Secondary accent (categorisation) */
  lav: '#8B7BAB',
  /** Secondary accent (categorisation) */
  sky: '#5B8FA8',
  /** Highlight — use sparingly */
  yellow: '#E8C84A',
  /** Card surface */
  card: '#1E1A16',
  /** Card border */
  cardBd: 'rgba(255,255,255,0.08)',
} as const;

export type ColorToken = keyof typeof colors;
export type ColorValue = (typeof colors)[ColorToken];

/**
 * Accent budget: at most three of clay / sage / lav / sky / yellow per screen.
 * Never use pure white (#FFF) or pure black (#000) backgrounds.
 */
export const accentTokens = ['clay', 'sage', 'lav', 'sky', 'yellow'] as const satisfies ColorToken[];
export const ACCENT_BUDGET = 3;
