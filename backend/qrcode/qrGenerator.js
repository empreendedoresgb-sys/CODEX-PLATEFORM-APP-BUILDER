export function generateQrPayload(targetType, targetId) {
  return { targetType, targetId, token: crypto.randomUUID?.() || `${Date.now()}` };
}
