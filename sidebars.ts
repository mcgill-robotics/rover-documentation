import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    // 'PCB-intro',{
    //   type: 'autogenerated',
    //   dirName: 'PCBs', // Generate sidebar slice from docs/api
    // },
    'rover-document',
    {
      type: 'category',
      label: 'PCBs',
      collapsed: false,
      items: [
        // 'PCB-intro',
        {
          type: 'autogenerated',
          dirName: 'PCBs', // Generate sidebar slice from docs/tutorials/easy
        },
      ],
    },
    {
      type: 'category',
      label: 'Mechanical Assembly',
      collapsed: false,
      items: [
        // 'PCB-intro',
        {
          type: 'autogenerated',
          dirName: 'mechanicalAssembly', // Generate sidebar slice from docs/tutorials/easy
        },
      ],
    },
    {
      type: 'category',
      label: 'Tutorial - Doc How To',
      items: [
        {
          type: 'autogenerated',
          dirName: 'tutorial-doc-how_to', // Generate sidebar slice from docs/tutorials/easy
        },
      ],
    },
  ],
  fundamentalsSidebar: [
    {
      type: 'autogenerated',
      dirName: 'fundamentals',
    },
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
  // fundamentalSidebar: [{type: 'autogenerated', dirName: '.'}],
};

export default sidebars;
