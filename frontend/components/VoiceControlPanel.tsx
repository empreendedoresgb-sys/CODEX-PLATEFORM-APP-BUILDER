import React from 'react';

type Props = {
  voiceIdentity: string;
  onGenerate: () => void;
};

export function VoiceControlPanel({ voiceIdentity, onGenerate }: Props) {
  return (
    <section>
      <h2>Voice Labs Control Panel</h2>
      <div>{voiceIdentity}</div>
      <button onClick={onGenerate}>Generate Voice</button>
    </section>
  );
}
