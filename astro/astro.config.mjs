// Astro spike for it-journey.dev. See README.md.
import { defineConfig } from 'astro/config';

import { repoAssets } from './src/integrations/repo-assets.mjs';

export default defineConfig({
  site: 'https://it-journey.dev',
  // Jekyll serves every page at `/path/` (permalink: pretty). Match it exactly so
  // existing links, the sitemap and saved progress (keyed by permalink) carry over.
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [repoAssets()],
  markdown: {
    shikiConfig: {
      // Both palettes are emitted as CSS variables; src/styles picks one with
      // light-dark(), so code blocks follow the theme without a second render.
      themes: { light: 'github-light', dark: 'github-dark' },
      defaultColor: false,
    },
  },
});
