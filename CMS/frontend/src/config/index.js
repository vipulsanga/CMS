const trimTrailingSlash = (value) => value.replace(/\/+$/, '');

const apiBaseUrl = trimTrailingSlash(import.meta.env.VITE_API_BASE_URL || '');

export const config = {
  apiBaseUrl,
};

export const apiUrl = (path) => `${config.apiBaseUrl}${path}`;
