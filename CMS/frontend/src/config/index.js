const trimTrailingSlash = (value) => value.replace(/\/+$/, '');

const configuredApiBaseUrl = trimTrailingSlash(import.meta.env.VITE_API_BASE_URL || '');
const isBrowser = typeof window !== 'undefined';
const isLocalBrowser = isBrowser && ['localhost', '127.0.0.1'].includes(window.location.hostname);
const isExampleUrl = configuredApiBaseUrl.includes('your-production-backend.example.com');
const isLocalApiUrl = /:\/\/localhost(?::\d+)?$|:\/\/127\.0\.0\.1(?::\d+)?$/.test(configuredApiBaseUrl);

// A Django-served frontend and API share an origin in production.  Avoid
// sending visitors to Vite's example URL (or their own localhost) when a
// deployment has not supplied a real external API URL.
const apiBaseUrl = isExampleUrl || (isLocalApiUrl && !isLocalBrowser)
  ? ''
  : configuredApiBaseUrl;

export const config = {
  apiBaseUrl,
};

export const apiUrl = (path) => `${config.apiBaseUrl}${path}`;
