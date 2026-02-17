import React from 'react';

type Template = { template_name: string; behavior_category: string };

export function TemplateSelector({ templates }: { templates: Template[] }) {
  return (
    <ul>
      {templates.map((t) => (
        <li key={t.template_name}>{t.template_name} ({t.behavior_category})</li>
      ))}
    </ul>
  );
}
