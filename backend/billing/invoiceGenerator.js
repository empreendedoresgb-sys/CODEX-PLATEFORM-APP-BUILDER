export function generateInvoice(orgId, amountCents) {
  return { orgId, amountCents, status: 'issued' };
}
