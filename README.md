# Qalab Abbas AI Portfolio

Personal portfolio and job-search site for Qalab Abbas, a Senior ML Engineer (voice AI, clinical NLP, real-time audio ML) open to remote roles, full-time or contract. It lists experience, projects, and contact details for recruiters, and offers a CV download. Built with React, TypeScript, Vite, and Framer Motion.

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

The included GitHub Actions workflow builds and deploys the site to GitHub Pages on pushes to `main` only.

If you rename the repository later, update the `base` value in `vite.config.ts` to match the new repository name.
