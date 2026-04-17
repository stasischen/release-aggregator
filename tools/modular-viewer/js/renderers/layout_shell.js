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
  const summary = node.displaySummary || window.getLabel('look_at_content');
  const expected = node.displayExpected || window.getLabel('understand_focus');
  el.innerHTML = `
    <div class="summary-grid animate-in" style="margin-bottom:12px;">
      <div class="summary-box">
        <span class="label">${window.getLabel('node_goal')}</span>
        ${window.escapeHtml(summary)}
      </div>
      <div class="summary-box">
        <span class="label">${window.getLabel('expected_output')}</span>
        ${window.escapeHtml(expected)}
      </div>
    </div>
  `;
};

window.renderFreeNote = function (node) {
  return `
      <div class="free-note-box animate-in">
        <textarea placeholder="${window.getLabel('free_note_placeholder')}"></textarea>
      </div>
    `;
};
