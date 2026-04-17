/**
 * Fallback & Inspection Renderers
 * Safe-guard UI for missing or corrupted data.
 */

window.renderDataInspection = function (payload, reason = 'Data Inspection Required') {
  return `
      <div class="data-inspection-box animate-in">
        <div class="empty-state">
          <div class="icon" style="font-size:24px; margin-bottom:8px;">🧐</div>
          <div><strong style="color:var(--warn);">${window.escapeHtml(reason)}</strong></div>
          <p class="muted-text tiny-text" style="margin-top:4px;">此節點資料格式不符或遺漏關鍵欄位，請聯繫內容小組。</p>
          <pre class="json-viewer">${window.escapeHtml(JSON.stringify(payload, null, 2))}</pre>
        </div>
      </div>
    `;
};
