# Qalab Abbas AI Portfolio

Personal portfolio site built with React, TypeScript, Vite, and Framer Motion.

## Local development

```bash
npm install
npm run dev
```

## Production checks

```bash
npm run lint
npm run build
```

## GitHub Pages deployment

This repository is configured as a GitHub Pages project site, so the Vite base path is set to:

```txt
/qalab-abbas-ai-portfolio/
```

The included GitHub Actions workflow builds and deploys the site to GitHub Pages on pushes to `main` or `ML-Engineer`.

If you rename the repository later, update the `base` value in `vite.config.ts` to match the new repository name.
