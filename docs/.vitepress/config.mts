import { defineConfig } from "vitepress";

export default defineConfig({
  title: "PhenoMCP",
  description: "Multi-language MCP SDK and runtime for the Phenotype ecosystem",
  base: process.env.GITHUB_PAGES === "true" ? "/PhenoMCP/" : "/",
  cleanUrls: true,
  themeConfig: {
    nav: [
      { text: "Overview", link: "/" },
      { text: "Research", link: "/research/" },
      { text: "Reference", link: "/reference/" },
      { text: "Worklogs", link: "/worklogs/" },
    ],
    sidebar: [
      {
        text: "Getting Started",
        items: [
          { text: "Overview", link: "/" },
          { text: "Current State", link: "/#what-actually-exists-today" },
        ],
      },
      {
        text: "Docs",
        items: [
          { text: "State of the Art: MCP", link: "/research/SOTA-MCP" },
          { text: "Feature Matrix", link: "/reference/fr_coverage_matrix" },
          { text: "Worklogs", link: "/worklogs/" },
        ],
      },
    ],
    socialLinks: [
      { icon: "github", link: "https://github.com/KooshaPari/PhenoMCP" },
    ],
  },
});
