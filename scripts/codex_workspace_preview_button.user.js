// ==UserScript==
// @name         Codex Workspace Preview Button
// @namespace    apbuilder
// @version      1.0.0
// @description  Adds a "Launch App Preview" button in Codex workspace UI (toolbar or floating fallback).
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function () {
  'use strict';

  const LABEL = 'Launch App Preview';
  const STORAGE_KEY = 'apbuilder_preview_url';
  const DEFAULT_URL = 'http://127.0.0.1:8000/docs';

  function getPreviewUrl() {
    const saved = window.localStorage.getItem(STORAGE_KEY);
    return saved && saved.trim() ? saved : DEFAULT_URL;
  }

  function onPreviewClick() {
    const current = getPreviewUrl();
    const next = window.prompt('Preview URL', current);
    if (!next) return;

    window.localStorage.setItem(STORAGE_KEY, next);
    window.open(next, '_blank', 'noopener,noreferrer');
  }

  function makeButton() {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = LABEL;
    btn.style.padding = '8px 10px';
    btn.style.borderRadius = '8px';
    btn.style.border = '1px solid #2563eb';
    btn.style.background = '#2563eb';
    btn.style.color = '#fff';
    btn.style.fontWeight = '600';
    btn.style.cursor = 'pointer';
    btn.style.marginLeft = '8px';
    btn.addEventListener('click', onPreviewClick);
    return btn;
  }

  function attachToToolbar() {
    const selectors = [
      'header',
      '[role="banner"]',
      '[data-testid*="header"]',
      '[data-testid*="topbar"]',
      '[class*="header"]',
      '[class*="toolbar"]',
    ];

    for (const selector of selectors) {
      const target = document.querySelector(selector);
      if (!target) continue;
      if (target.querySelector('[data-apbuilder-preview-btn="true"]')) return true;

      const button = makeButton();
      button.setAttribute('data-apbuilder-preview-btn', 'true');
      target.appendChild(button);
      return true;
    }

    return false;
  }

  function attachFloatingFallback() {
    if (document.querySelector('[data-apbuilder-preview-floating="true"]')) return;

    const wrapper = document.createElement('div');
    wrapper.setAttribute('data-apbuilder-preview-floating', 'true');
    wrapper.style.position = 'fixed';
    wrapper.style.top = '12px';
    wrapper.style.right = '12px';
    wrapper.style.zIndex = '999999';

    const button = makeButton();
    wrapper.appendChild(button);

    document.body.appendChild(wrapper);
  }

  function installButton() {
    const attached = attachToToolbar();
    if (!attached) attachFloatingFallback();
  }

  const observer = new MutationObserver(() => {
    installButton();
  });

  observer.observe(document.documentElement, { childList: true, subtree: true });
  installButton();
})();
