/**
 * Got Messy brand typography tokens.
 * Source of truth: CLAUDE.md — Typography section.
 */

export const fonts = {
  serif: 'Lora',
  sans: 'Poppins',
} as const;

export const fontWeights = {
  light: 300,
  regular: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
} as const;

/**
 * Type scale — rem values assume 16px root, px provided for React Native.
 * Display uses clamp(3rem,7vw,5.5rem) on web; use displayPx (88) on native.
 * Body range: 0.875rem (bodySmPx 14) to 1rem (bodyPx 16).
 */
export const typeScale = {
  display:   { rem: 5.5,   px: 88, weight: fontWeights.bold,     font: fonts.serif },
  h1:        { rem: 2.25,  px: 36, weight: fontWeights.bold,     font: fonts.serif },
  h2:        { rem: 1.5,   px: 24, weight: fontWeights.bold,     font: fonts.serif },
  h3:        { rem: 1.15,  px: 18, weight: fontWeights.bold,     font: fonts.serif },
  body:      { rem: 1,     px: 16, weight: fontWeights.regular,  font: fonts.sans  },
  bodySm:    { rem: 0.875, px: 14, weight: fontWeights.regular,  font: fonts.sans  },
  caption:   { rem: 0.75,  px: 12, weight: fontWeights.regular,  font: fonts.sans  },
} as const;

/** Line height values used alongside the type scale. */
export const lineHeights = {
  tight:    1.05,
  snug:     1.2,
  normal:   1.6,
  relaxed:  1.75,
} as const;

/**
 * Wordmark rules (enforced — do not override):
 * - "got" in Lora 400 italic
 * - "Messy" in Lora 700
 * - terminal "." in --clay
 * Never rebuild in Poppins, all-caps, or with independent rotation/skew/animation.
 */
export const wordmark = {
  got:      { font: fonts.serif, weight: fontWeights.regular, style: 'italic' as const },
  messy:    { font: fonts.serif, weight: fontWeights.bold,    style: 'normal' as const },
  dotColor: 'clay', // references colors.clay — do not recolour
} as const;
