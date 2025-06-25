/**
 * Gets a cookie value by name
 * @param {string} name - The name of the cookie to retrieve
 * @returns {string|undefined} The cookie value or undefined if not found
 */
export function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return undefined;
}