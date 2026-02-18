export function parseMedia(asset) {
  return { assetId: asset?.id ?? null, parsed: true, markers: [] };
}
