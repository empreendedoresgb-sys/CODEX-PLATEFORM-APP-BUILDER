export function handlePaymentWebhook(payload) {
  return { providerRef: payload?.providerRef, accepted: true };
}
