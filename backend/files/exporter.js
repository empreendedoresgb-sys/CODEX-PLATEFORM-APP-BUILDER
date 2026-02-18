const SUPPORTED_EXPORTS = ['mp3', 'wav', 'srt', 'txt', 'json', 'preset'];

export function exportFile(jobId, format) {
  if (!SUPPORTED_EXPORTS.includes(format)) throw new Error(`Unsupported export format: ${format}`);
  return { jobId, format, status: 'queued' };
}
