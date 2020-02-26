module.exports = {
  base: "/researchhub-dataset-manager/",
  title: "Research Hub Dataset Manager",
  head: [
    [
      "link",
      {
        rel: "icon",
        href: "/assets/icjia-default.jpg"
      }
    ],
    [
      "link",
      {
        rel: "stylesheet",
        href: "https://fonts.googleapis.com/icon?family=Material+Icons"
      }
    ]
  ],
  themeConfig: {
    logo: "/assets/icjia-logo.png",
    nav: [
      { text: "Guide", link: "/guide/" },
      { text: "Developer Guide", link: "/dev-guide/" }
    ],
    sidebar: {
      "/guide/": [
        "/guide/",
        "/guide/prerequisites",
        "/guide/start",
        {
          title: "Tasks",
          children: [
            "/guide/tasks/",
            "/guide/tasks/1-data",
            "/guide/tasks/2-bridgepop",
            "/guide/tasks/3-dataset"
          ]
        },
        "/guide/output"
      ],
      "/dev-guide/": [
        "/dev-guide/",
        {
          title: "App",
          children: [
            "/dev-guide/app/",
            "/dev-guide/app/main",
            "/dev-guide/app/packages"
          ]
        },
        {
          title: "Database",
          children: ["/dev-guide/database/", "/dev-guide/database/tables"]
        },
        "/dev-guide/sources",
        "/dev-guide/doc",
        "/dev-guide/misc"
      ]
    },
    repo: "icjia/researchhub-dataset-manager",
    repoLabel: "GitHub",
    lastUpdated: "Last Updated"
  }
};
