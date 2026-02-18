export function semanticAnalyze(text) {
  return { intent: 'informative', markers: [], length: (text || '').length };
}
