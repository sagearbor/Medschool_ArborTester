/**
 * pages/_app.js
 *
 * This is the root component for your Next.js application. Next.js uses this
 * App component to initialize pages. By importing your global CSS file here,
 * you ensure that your Tailwind styles are available on every single page.
 * This is the only place you should import `globals.css`.
 */
import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  // This is the component for the current page.
  // pageProps are the initial props that were preloaded for the page.
  return <Component {...pageProps} />;
}

export default MyApp;