export function upgradeTier(currentTier, nextTier) {
  return { from: currentTier, to: nextTier, status: 'active' };
}
