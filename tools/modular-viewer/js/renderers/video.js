/**
 * Video Subtitle Renderer Component
 */

(function () {
  function renderVideo(node) {
    const payload = node.payload || {};
    const isBilingual = showBilingual();

    // Use normalized segments
    const normalized = payload.normalized_segments;
    if (!normalized || !normalized.segments || normalized.segments.length === 0) {
      return `
        <div class="video-container animate-in">
          <div class="bubble-stream">
            <div class="system-message">${window.getLabel('no_video_subtitle')}</div>
          </div>
        </div>
      `;
    }

    const segments = normalized.segments;

    const subtitleHtml = `
        <div class="subtitle-stream">
            ${segments.map(seg => renderVideoSegment(seg, isBilingual)).join('')}
        </div>
    `;

    return `
      <div class="video-container animate-in">
        ${window.renderNotice ? window.renderNotice(payload) : ''}
        <div class="video-player-placeholder">
            <div class="placeholder-icon">🎬</div>
            <div class="placeholder-text">${window.getLabel('video_preview_soft')}</div>
        </div>
        ${subtitleHtml}
      </div>
    `;
  }

  function renderVideoSegment(seg, isBilingual) {
    const timeStr = formatMs(seg.start_ms);
    const showTrans = isBilingual && seg.translation;
    
    return `
      <div class="subtitle-row" data-segment-id="${seg.segment_id}" onclick="APP.selectSegment('${seg.segment_id}')">
        <div class="timestamp">${timeStr}</div>
        <div class="texts">
          <div class="target">${window.APP.renderKoreanSegmentation(seg)}</div>
          ${showTrans ? `<div class="translation">${window.escapeHtml(seg.translation || '')}</div>` : ''}
          <div class="action-row" style="margin-top:4px;">
            ${window.renderSpeakButton(seg.ko)}
          </div>
        </div>
      </div>
    `;
  }

  function formatMs(ms) {
    if (ms === undefined || ms === null) return '00:00';
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }

  function renderAtomsInline(atoms) {
    if (!atoms || atoms.length === 0) return '';
    return `
      <div class="inline-atoms">
        ${atoms.map(a => `
            <span class="atom-tag" title="${a.pos || ''}">${window.escapeHtml(a.text)}</span>
        `).join('')}
      </div>
    `;
  }

  window.RendererRegistry.registerContent('video', renderVideo);
})();
