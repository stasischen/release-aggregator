/**
 * Layout Shell Renderers
 * Responsible for the UI frame surrounding the node content.
 */

window.renderDetailHeader = function (node) {
  const el = document.getElementById('detailHeader');
  if (!el) return;
  const stage = window.nodeStageLabel(node.id) || '';
  const skillFocus = window.nodeSkillFocusText(node);

  el.innerHTML = `
    <div class="detail-header-card animate-in">
      <div class="tiny-text muted">${window.escapeHtml(stage || node.learning_role || 'node')}</div>
      <h2 style="margin:4px 0 8px;">${window.escapeHtml(node.displayTitle || '')}</h2>
      <div class="meta-tags">
        <span class="tag">${window.escapeHtml(node.content_form || 'unknown')}</span>
        <span class="tag">${window.escapeHtml(node.learning_role || 'learning')}</span>
        <span class="tag">${window.escapeHtml(skillFocus)}</span>
      </div>
    </div>
  `;
};

window.renderDetailSummary = function (node) {
  const el = document.getElementById('detailSummary');
  if (!el) return;
  const summary = node.displaySummary || '先看這一節的內容。';
  const expected = node.displayExpected || '先理解這一節的重點。';
  el.innerHTML = `
    <div class="summary-grid animate-in" style="margin-bottom:12px;">
      <div class="summary-box">
        <span class="label">本節目標</span>
        ${window.escapeHtml(summary)}
      </div>
      <div class="summary-box">
        <span class="label">預期輸出</span>
        ${window.escapeHtml(expected)}
      </div>
    </div>
  `;
};

window.renderFreeNote = function (node) {
  return `
      <div class="free-note-box animate-in">
        <textarea placeholder="隨手筆記 (Free Note)..."></textarea>
      </div>
    `;
};
