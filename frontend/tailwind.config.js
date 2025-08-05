/**
 * tailwind.config.js
 *
 * This is your Tailwind CSS configuration file.
 * You can customize your theme, add plugins, and most importantly,
 * specify the paths to all of your template files in the `content` array.
 * Tailwind will scan these files for class names and generate the corresponding styles.
 */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',    // Scan all pages
    './components/**/*.{js,ts,jsx,tsx}', // Scan all components
    // Add other directories here if you have them
  ],
  theme: {
    extend: {
      // You can extend the default Tailwind theme here.
      // For example, adding custom colors, fonts, or spacing.
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [
    // Add any Tailwind plugins here.
    // e.g., require('@tailwindcss/forms'),
  ],
};
