/**
 * Core Helpers & Utilities for Renderers
 * Shared logic for text processing and state access.
 */

// --- Markdown & Text Processing ---

window.applyInlineMarkdown = function (text) {
  return String(text || '')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/\[id:([^\]|]+)\]/g, (m, id) => {
      const bank = window.APP?.libSentences || {};
      const s = bank[id];
      const ko = s?.source?.ko || s?.source?.surface_ko || s?.ko || id;
      const zh = s?.i18n?.translation || s?.translation || window.getLabel('no_translation');
      const audioCall = `APP.playOriginalOrTTS('${window.escapeJsSingle(ko)}')`;
      return `<span class="inline-sentence-chip" onclick="${audioCall}" title="${window.getLabel('click_to_play')}">
                <span class="ko">${window.escapeHtml(ko)}</span>
                <span class="view-translation">${window.escapeHtml(zh)}</span>
              </span>`;
    })
    .replace(/\[ko:(.*?)\|zh:(.*?)(?:\|id:(.*?))?\]/g, (m, ko, zh, id) => {
      const audioCall = `APP.playOriginalOrTTS('${window.escapeJsSingle(ko)}')`;
      return `<span class="inline-sentence-chip" onclick="${audioCall}" title="${window.getLabel('click_to_play')}">
                <span class="ko">${window.escapeHtml(ko)}</span>
                <span class="view-translation">${window.escapeHtml(zh)}</span>
              </span>`;
    })
    .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');
};

window.markdownToHtmlLite = function (md) {
  const src = String(md || '').replace(/\r\n/g, '\n');
  const lines = src.split('\n');
  const out = [];
  let i = 0;
  let currentContainerType = null; // 'formula', 'alert', 'context', or null

  const isTableSeparator = (line) => /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line);
  const isTableRow = (line) => line.includes('|');

  const closeContainer = () => {
    if (currentContainerType) {
      out.push('</div></div>');
      currentContainerType = null;
    }
  };

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();
    
    if (!trimmed) { 
      i++; 
      continue; 
    }

    // Headers
    const hMatch = trimmed.match(/^(#{1,3})\s+(.*)/);
    if (hMatch) {
      const level = hMatch[1].length;
      const text = hMatch[2];
      
      // Detection of specialized Bento-style blocks
      if (level === 3) {
        if (text.includes('📐')) {
          closeContainer();
          currentContainerType = 'formula';
          out.push(`<div class="formula-box animate-in"><div class="box-header"><span class="icon">📐</span> ${window.applyInlineMarkdown(text.replace('📐', '').trim())}</div><div class="box-body">`);
          i++; continue;
        } else if (text.includes('⚠️')) {
          closeContainer();
          currentContainerType = 'alert';
          out.push(`<div class="alert-box animate-in"><div class="box-header"><span class="icon">⚠️</span> ${window.applyInlineMarkdown(text.replace('⚠️', '').trim())}</div><div class="box-body">`);
          i++; continue;
        } else if (text.includes('💬')) {
          closeContainer();
          currentContainerType = 'context';
          out.push(`<div class="context-box animate-in"><div class="box-header"><span class="icon">💬</span> ${window.applyInlineMarkdown(text.replace('💬', '').trim())}</div><div class="box-body">`);
          i++; continue;
        } else {
          // Normal H3 closes current container
          closeContainer();
        }
      } else if (level < 3) {
        // H1, H2 close any container
        closeContainer();
      }

      out.push(`<h${level} class="md-h${level}">${window.applyInlineMarkdown(text)}</h${level}>`);
      i++; continue;
    }

    // Tables
    if (i + 1 < lines.length && isTableRow(lines[i]) && isTableSeparator(lines[i + 1])) {
      const headerCells = lines[i].split('|').map(c => c.trim()).filter(Boolean);
      i += 2;
      const bodyRows = [];
      while (i < lines.length && isTableRow(lines[i]) && lines[i].trim()) {
        const rowCells = lines[i].split('|').map(c => c.trim()).filter(Boolean);
        if (rowCells.length) bodyRows.push(rowCells);
        i++;
      }
      out.push(`
        <div class="md-table-wrap">
          <table class="md-table">
            <thead><tr>${headerCells.map(c => `<th>${window.applyInlineMarkdown(c)}</th>`).join('')}</tr></thead>
            <tbody>${bodyRows.map(r => `<tr>${r.map(c => `<td>${window.applyInlineMarkdown(c)}</td>`).join('')}</tr>`).join('')}</tbody>
          </table>
        </div>
      `);
      continue;
    }

    // Unordered Lists
    if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      const items = [];
      while (i < lines.length && (lines[i].trim().startsWith('- ') || lines[i].trim().startsWith('* '))) {
        items.push(lines[i].trim().slice(2));
        i++;
      }
      out.push(`<ul class="grammar-point-list">${items.map(p => `<li>${window.applyInlineMarkdown(p)}</li>`).join('')}</ul>`);
      continue;
    }

    // Ordered Lists
    const olMatch = trimmed.match(/^(\d+\.)\s+(.*)/);
    if (olMatch) {
      const items = [];
      while (i < lines.length) {
        const current = lines[i].trim();
        const currentMatch = current.match(/^(\d+\.)\s+(.*)/);
        if (!currentMatch) break;

        const item = {
          text: currentMatch[2],
          subItems: []
        };
        i++;

        // Allow simple nested bullet lists under each numbered item.
        while (i < lines.length) {
          const lookahead = lines[i].trim();
          if (!lookahead) {
            i++;
            break;
          }
          if (/^\d+\.\s+/.test(lookahead)) break;
          if (/^[-*]\s+/.test(lookahead)) {
            item.subItems.push(lookahead.slice(2));
            i++;
            continue;
          }
          break;
        }

        items.push(item);
      }

      out.push(
        `<ol class="grammar-point-list" style="padding-left:24px;">` +
        items.map(item => {
          const nested = item.subItems.length
            ? `<ul class="grammar-point-list nested">${item.subItems.map(p => `<li>${window.applyInlineMarkdown(p)}</li>`).join('')}</ul>`
            : '';
          return `<li>${window.applyInlineMarkdown(item.text)}${nested}</li>`;
        }).join('') +
        `</ol>`
      );
      continue;
    }

    out.push(`<p class="md-paragraph">${window.applyInlineMarkdown(line)}</p>`);
    i++;
  }
  
  closeContainer();
  return out.join('');
};

// --- Global UI Context Helpers ---

window.currentLocale = () => window.state?.progress?.prefs?.teachingLocale || 'zh_tw';
window.currentTeachingLocale = window.currentLocale;
window.showBilingual = () => window.state?.progress?.prefs?.showBilingual !== false;

// --- Node Metadata Helpers ---

window.nodeTitleText = (node, locale) => node.displayTitle || window.LessonAdapter.resolveText(node && node.title_i18n, locale, window.LessonAdapter.getFallbackNodeTitle(node));
window.nodeSummaryText = (node, locale) => node.displaySummary || window.getLabel('look_at_content');
window.nodeExpectedText = (node, locale) => node.displayExpected || window.getLabel('understand_focus');

window.nodeSkillFocusText = function (node) {
  if (node.skill_focus && node.skill_focus.length > 0) return node.skill_focus.join(' · ');
  const id = node.id || '';
  if (id.includes('-L')) return 'listening · reading';
  if (id.includes('-G')) return 'grammar · reading';
  if (id.includes('-P')) return 'speaking · output';
  return 'learning';
};

window.nodeStageLabel = function (nodeId) {
  const match = String(nodeId || '').match(/-(L1|L2|L3|G1|G2|P1|P2|P5|R1)$/);
  return match ? match[1] : '';
};
