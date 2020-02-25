<template>
  <p class="vuepress">
    <a href="https://vuepress.vuejs.org/" target="_blank" rel="noreferrer">
      <span>This documentation is powered by</span>
      <img alt="vuepress" src="https://vuepress.vuejs.org/hero.png" />
      <span style="color:rgba(0,0,0,.87)">VuePress</span>
    </a>
  </p>
</template>

<style scoped>
.vuepress {
  font-family: "Lato", sans-serif;
  background-color: #f3f6f8;
  padding: 0.6em 1.2em;
  border-radius: 8px;
  display: inline-block;
  margin: 1em 0 !important;
}

.vuepress a {
  color: #999;
  font-weight: bold;
}

.vuepress a:hover {
  text-decoration: none !important;
}

.vuepress img {
  height: 40px;
  margin-left: 10px;
}

.vuepress img,
.vuepress span {
  vertical-align: middle;
}
</style>
