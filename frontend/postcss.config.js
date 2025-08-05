/**
 * postcss.config.js
 *
 * This file configures PostCSS. Next.js has built-in support for PostCSS.
 * You just need to tell it which plugins to use.
 *
 * - tailwindcss: Processes your Tailwind directives and configuration.
 * - autoprefixer: Adds vendor prefixes (like -webkit-, -moz-) to your CSS
 * for better cross-browser compatibility.
 */
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
