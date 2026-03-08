/**
 * Dialogue Renderer Component
 */

(function () {
    function renderDialogue(node) {
        const payload = node.payload || {};
        const body = document.getElementById('detailBody');
        const locale = currentLocale();
        const isBilingual = showBilingual();

        // 1. Dialogue Area
        let dialogueHtml = '';
        const scenes = payload.dialogue_scenes || [];
        const legacyTurns = payload.dialogue_turns || [];

        if (scenes.length > 0) {
            dialogueHtml = scenes.map(scene => `
        <div class="dialogue-scene">
          <div class="scene-header">${window.escapeHtml(window.i18nText(scene.title_i18n, locale, scene.title_zh_tw || '對話片段'))}</div>
          ${scene.note_zh_tw ? `<div class="scene-note">${window.escapeHtml(scene.note_zh_tw)}</div>` : ''}
          <div class="bubble-stream">
            ${scene.turns.map(t => renderTurn(t, locale, isBilingual)).join('')}
          </div>
        </div>
      `).join('');
        } else if (legacyTurns.length > 0) {
            dialogueHtml = `
        <div class="bubble-stream">
          ${legacyTurns.map(t => renderTurn(t, locale, isBilingual)).join('')}
        </div>
      `;
        }

        body.innerHTML = `
      <div class="dialogue-container animate-in">
        ${window.renderNotice(payload)}
        ${dialogueHtml}
        ${window.renderLessonSupportModule(payload.lesson_support_module)}
        ${payload.pattern_builder_demo ? window.renderPatternBuilderBlock(payload.pattern_builder_demo) : ''}
        ${(payload.pattern_builder_demos || []).map(d => window.renderPatternBuilderBlock(d)).join('')}
      </div>
    `;
    }

    function renderTurn(t, locale, isBilingual) {
        const translation = window.i18nText(t.translations_i18n, locale, t.zh_tw || t.en || '');
        return `
      <div class="bubble-row ${t.speaker === 'A' ? 'left' : 'right'} ${t.register || ''}">
        <div class="avatar">${t.speaker}</div>
        <div class="bubble">
          <div class="target">${window.escapeHtml(t.text)}</div>
          ${isBilingual ? `<div class="translation">${window.escapeHtml(translation)}</div>` : ''}
        </div>
      </div>
    `;
    }

    window.RendererRegistry.registerContent('dialogue', renderDialogue);
})();
