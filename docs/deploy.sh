#!/usr/bin/env sh

# abort on errors
set -e

# build
# vuepress build docs

# navigate into the build output directory
cd docs/.vuepress/dist

git init
git add -A
git commit -m 'deploy'

# if you are deploying to https://<USERNAME>.github.io/<REPO>
git push -f https://github.com/icjia/researchhub-dataset-manager.git master:gh-pages

cd -