# Documentation

This documentation site for Research Hub Dataset Manager is powered by [VuePress](https://vuepress.vuejs.org/), the Vue-powered Static Site Generator.

::: warning NOTE

This page only provides a high-level description of the documentation site. To investigate the code in detail, go to [the project's GitHub repository](https://github.com/icjia/researchhub-dataset-manager) or clone the repository to your local workstation.

Also, please refer to [the VuePress documentation](https://vuepress.vuejs.org/) for more general information on VuePress.

:::

## Project setup

```bash
# install VuePress globally
yarn global add vuepress
# OR npm install -g vuepress

# start dev server
vuepress dev docs

# build to static files
vuepress build docs
```

## File structure

```
/docs/
├─ .vuepress/
|   ├─ components/
|   ├─ public/
|   |   └─ assets/
|   ├─ styles/
|   └─ config.js
├─ dev-guide/
├─ guide/
├─ deploy.sh
└─ README.md
```

- `/docs/.vuepress/` includes custom Vue components (`components/`), static assets (`public/assets/`), style files (`styles/`) and `config.js` for specifying configurations.
- `/docs/dev-guide/` includes all markdown files corresponding to the Developer Guide pages.
- `/docs/guide/` includes all markdown files corresponding to the Guide pages.
- `deploy.sh` is a shell script to build and deploy this documentation to GitHub Pages.
- `/docs/REAMDE.md` is a markdown file for the documentation homepage.
