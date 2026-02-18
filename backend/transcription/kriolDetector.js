export function detectKriol(text) {
  const lower = (text || '').toLowerCase();
  return lower.includes('kriol') || lower.includes('nka') || lower.includes('ka');
}
