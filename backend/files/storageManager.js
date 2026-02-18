export function buildStoragePath(orgId, projectId, filename) {
  return `orgs/${orgId}/projects/${projectId}/${filename}`;
}
