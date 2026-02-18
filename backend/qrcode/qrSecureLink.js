export function buildSecureLink(baseUrl, token) {
  return `${baseUrl.replace(/\/$/, '')}/qr/${token}`;
}
