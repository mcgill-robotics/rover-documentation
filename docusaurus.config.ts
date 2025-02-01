import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Rover Documentation',
  tagline: 'Doc or Cry',
  favicon: 'img/favicon_mcgillrobotics.ico',

  // Set the production url of your site here
  url: 'https://github.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/rover-documentation',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'mcgill-robotics', // Usually your GitHub org/user name.
  projectName: 'rover-documentation', // Usually your repo name.
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'McGill Robotics',
      logo: {
        alt: 'McGill Robotics',
        src: 'img/Logo_white_on_black.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {
          href: 'https://github.com/orgs/mcgill-robotics/projects/50',
          label: 'Taskboard',
          position: 'right',
        },
        // {
        //   href: 'https://github.com/mcgill-robotics/rover-documentation',
        //   label: 'GitHub',
        //   position: 'right',
        // },
        {
          href: 'https://docs.google.com/spreadsheets/d/1Oeg_WPtlBZXyiplVIpyahuClL3fWfGzlk_3tDz--Uok/edit?gid=0#gid=0',
          label: 'SpecIndex',
          position: 'left',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Quick Links',
          items: [
            {
              label: 'Documentation',
              to: '/docs/rover-document',
            },
            {
              label: 'SpecIndex',
              href: 'https://docs.google.com/spreadsheets/d/1Oeg_WPtlBZXyiplVIpyahuClL3fWfGzlk_3tDz--Uok/edit?gid=0#gid=0',
            },
            {
              label: 'Elec Taskboard',
              href: 'https://github.com/orgs/mcgill-robotics/projects/50',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Main Website',
              href: 'https://mcgillrobotics.com/',
            },
            {
              label: 'Youtube',
              href: 'https://youtube.com/@mcgillrobotics',
            },
            {
              label: 'Instagram',
              href: 'https://instagram.com/mcgillrobotics',
            },
            {
              label: 'Facebook',
              href: 'https://facebook.com/mcgillrobotics',
            },
            {
              label: 'McGill',
              href: 'https://www.mcgill.ca/engineeringdesign/design-teams/mcgill-robotics',
            },
          ],
        },
        {
          title: 'More',
          items: [
            // {
            //   label: 'Blog',
            //   to: '/blog',
            // },
            {
              label: 'GitHub Repo',
              href: 'https://github.com/mcgill-robotics/rover-documentation',
            },
          ],
        },
      ],
      //copyright: `Copyright © ${new Date().getFullYear()} My Project, Inc. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
