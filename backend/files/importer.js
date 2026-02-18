const SUPPORTED_IMPORTS = ['txt', 'docx', 'pdf', 'mp3', 'wav', 'mp4', 'mov', 'png', 'jpg', 'webm'];

export function importFile(filename) {
  const ext = filename.split('.').pop().toLowerCase();
  if (!SUPPORTED_IMPORTS.includes(ext)) throw new Error(`Unsupported import format: ${ext}`);
  return { status: 'queued', filename, ext };
}
