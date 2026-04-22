import React, { useMemo, useState } from 'react';

type DeviceMode = 'desktop' | 'tablet' | 'mobile';

const FRAME_SIZES: Record<DeviceMode, { width: string; height: string; label: string }> = {
  desktop: { width: '100%', height: '720px', label: 'Desktop' },
  tablet: { width: '820px', height: '1180px', label: 'Tablet' },
  mobile: { width: '390px', height: '844px', label: 'Mobile' },
};

/**
 * PreviewWorkbench
 *
 * A top-bar preview launcher component for local app testing in the project UI.
 *
 * - "Launch Live App Preview" button
 * - interactive mode on/off
 * - device simulator switching (desktop/tablet/mobile)
 */
export function PreviewWorkbench({ previewUrl }: { previewUrl: string }) {
  const [isOpen, setIsOpen] = useState(false);
  const [interactiveMode, setInteractiveMode] = useState(true);
  const [deviceMode, setDeviceMode] = useState<DeviceMode>('desktop');

  const frameSize = useMemo(() => FRAME_SIZES[deviceMode], [deviceMode]);

  return (
    <section style={{ border: '1px solid #e5e7eb', borderRadius: 12, overflow: 'hidden' }}>
      <header
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '12px 16px',
          background: '#0f172a',
          color: '#fff',
        }}
      >
        <strong>Top Menu • App Preview</strong>

        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <button
            type="button"
            onClick={() => setInteractiveMode((v) => !v)}
            style={{
              border: '1px solid #334155',
              background: interactiveMode ? '#16a34a' : '#475569',
              color: '#fff',
              padding: '8px 10px',
              borderRadius: 8,
              cursor: 'pointer',
            }}
          >
            {interactiveMode ? 'Interactive: ON' : 'Interactive: OFF'}
          </button>

          <button
            type="button"
            onClick={() => setIsOpen(true)}
            style={{
              background: '#2563eb',
              border: 'none',
              color: '#fff',
              padding: '8px 12px',
              borderRadius: 8,
              cursor: 'pointer',
              fontWeight: 600,
            }}
          >
            Launch Live App Preview
          </button>
        </div>
      </header>

      {isOpen ? (
        <div style={{ padding: 16, background: '#f8fafc' }}>
          <div style={{ display: 'flex', gap: 8, marginBottom: 12, flexWrap: 'wrap' }}>
            {(Object.keys(FRAME_SIZES) as DeviceMode[]).map((mode) => (
              <button
                key={mode}
                type="button"
                onClick={() => setDeviceMode(mode)}
                style={{
                  border: '1px solid #cbd5e1',
                  background: deviceMode === mode ? '#dbeafe' : '#fff',
                  color: '#0f172a',
                  padding: '6px 10px',
                  borderRadius: 8,
                  cursor: 'pointer',
                }}
              >
                {FRAME_SIZES[mode].label}
              </button>
            ))}
          </div>

          <div
            style={{
              width: frameSize.width,
              height: frameSize.height,
              margin: '0 auto',
              border: '1px solid #cbd5e1',
              borderRadius: 12,
              overflow: 'hidden',
              background: '#fff',
              transition: 'all 0.2s ease-in-out',
              pointerEvents: interactiveMode ? 'auto' : 'none',
            }}
          >
            <iframe
              title="APBUILDER Live Preview"
              src={previewUrl}
              style={{ width: '100%', height: '100%', border: 0 }}
              sandbox={interactiveMode ? 'allow-scripts allow-same-origin allow-forms allow-popups' : ''}
            />
          </div>
        </div>
      ) : null}
    </section>
  );
}
