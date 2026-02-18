export function convertFormat(input, targetFormat) {
  return { ...input, targetFormat, converted: true };
}
