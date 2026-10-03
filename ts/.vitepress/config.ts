import { createRequire } from 'node:module';
import path from 'node:path';
import { defineConfig } from 'vitepress';

// The pages live in ../docs, outside this package, so resolve Vue from here.
const require = createRequire(import.meta.url);
const vueDir = path.dirname(require.resolve('vue/package.json'));

export default defineConfig({
  title: 'Sourcefold Wiki',
  description:
    'Public documentation and reference CLI for folding repositories into a single Markdown artifact.',
  srcDir: '../docs',
  // graft/README.md links to license files that are not pages.
  ignoreDeadLinks: [/LICENSE/],
  cleanUrls: true,
  vite: {
    resolve: {
      alias: [{ find: /^vue(\/.*)?$/, replacement: `${vueDir}$1` }],
    },
  },
  themeConfig: {
    nav: [
      { text: 'Quick start', link: '/quick-start' },
      { text: 'Format spec', link: '/format-spec' },
      { text: 'CLI reference', link: '/cli-reference' },
      { text: 'Techniques', link: '/exploration-techniques-and-use-cases' },
    ],
    sidebar: [
      {
        text: 'Guide',
        items: [
          { text: 'Home', link: '/' },
          { text: 'Quick start', link: '/quick-start' },
          { text: 'Format spec', link: '/format-spec' },
          {
            text: 'Ignore and inclusion rules',
            link: '/ignore-and-inclusion-rules',
          },
          {
            text: 'Security and threat model',
            link: '/security-and-threat-model',
          },
          { text: 'CLI reference', link: '/cli-reference' },
          {
            text: 'Exploration techniques and use cases',
            link: '/exploration-techniques-and-use-cases',
          },
          { text: 'Contributing', link: '/contributing' },
        ],
      },
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/ao3575911/sourcefold' },
    ],
  },
});
