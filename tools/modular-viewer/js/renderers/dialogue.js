/**
 * Dialogue Renderer Component
 */

(function () {
  function renderDialogue(node) {
    const payload = node.payload || {};
    const isBilingual = showBilingual();

    // Use normalized segments if available
    const normalized = payload.normalized_segments;
    if (!normalized || !normalized.segments || normalized.segments.length === 0) {
      return `
        <div class="dialogue-container animate-in">
          ${window.renderNotice(payload)}
          <div class="bubble-stream">
            <div class="system-message">未找到對話內容。</div>
          </div>
        </div>
      `;
    }

    const segments = normalized.segments;
    
    // Group segments by scene for logical display
    const scenes = [];
    let currentSceneId = null;
    let currentScene = null;

    segments.forEach(seg => {
        const sceneId = seg.source_meta?.scene_id || 'default';
        if (sceneId !== currentSceneId || !currentScene) {
            currentSceneId = sceneId;
            currentScene = {
                title: seg.source_meta?.scene_title || '對話片段',
                segments: []
            };
            scenes.push(currentScene);
        }
        currentScene.segments.push(seg);
    });

    const dialogueHtml = scenes.map(scene => `
        <div class="dialogue-scene">
          <div class="scene-header">${window.escapeHtml(scene.title)}</div>
          <div class="bubble-stream">
            ${scene.segments.map(seg => renderSegment(seg, isBilingual)).join('')}
          </div>
        </div>
    `).join('');

    return `
      <div class="dialogue-container animate-in">
        ${window.renderNotice(payload)}
        ${dialogueHtml}
        ${window.renderLessonSupportModule(payload.lesson_support_module)}
        ${payload.pattern_builder_demo ? window.renderPatternBuilderBlock(payload.pattern_builder_demo) : ''}
        ${(payload.pattern_builder_demos || []).map(d => window.renderPatternBuilderBlock(d)).join('')}
      </div>
    `;
  }

  function renderSegment(seg, isBilingual) {
    return `
        <div class="dialogue-turn ${seg.speaker === 'A' ? 'A' : 'B'}" data-segment-id="${seg.segment_id}" onclick="APP.selectSegment('${seg.segment_id}')">
            <div class="avatar">${seg.speaker}</div>
            <div class="content bubble">
                <div class="target">${window.APP.renderKoreanSegmentation(seg)}</div>
                ${isBilingual ? `<div class="translation">${window.escapeHtml(seg.translation || '')}</div>` : ''}
                <div style="margin-top:8px; text-align: right;">
                    ${window.renderSpeakButton(seg.ko)}
                </div>
            </div>
        </div>
    `;
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

  window.RendererRegistry.registerContent('dialogue', renderDialogue);
})();
