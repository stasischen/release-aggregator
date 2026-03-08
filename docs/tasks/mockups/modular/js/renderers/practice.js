/**
 * Practice & Review Renderer Component
 */

(function () {
  function renderPracticeCard(node) {
    const payload = node.payload || {};
    const locale = window.currentLocale();

    const modeLabel = {
      chunk_assembly: '拼句型練習',
      response_builder: '回應建構',
      guided: '引導式練習',
      flashcard_review: '閃卡複習',
      review_retrieval: '回想練習'
    }[payload.mode || node.output_mode] || '練習卡';

    const total = (payload.tasks || payload.items || payload.cards || []).length;

    return `
      <div class="practice-container animate-in">
        <div class="card-block">
          <div class="block-title">Practice Card</div>
          <div class="muted-text" style="margin-bottom:10px;">${window.escapeHtml(modeLabel)}</div>
          ${window.i18nText(payload.prompt_i18n, locale, payload.prompt_zh_tw || '') ? `
            <div style="margin-bottom:10px;">${window.escapeHtml(window.i18nText(payload.prompt_i18n, locale, payload.prompt_zh_tw || ''))}</div>
          ` : ''}
          ${total ? `<div class="tiny-text muted">本節練習題數：${total}</div>` : ''}
          <div class="tiny-text muted" style="margin-top:8px;">互動內容請見下方練習區塊。</div>
        </div>
        <div id="interactionArea"></div>
      </div>
    `;
  }

  function renderReviewCard(node) {
    renderPracticeCard(node); // Reuse practice card shell for now
  }

  // --- Interaction Modes ---

  function renderChunkAssemblyMode(node) {
    const locale = window.currentLocale();
    const payload = node.payload || {};
    const tasks = payload.tasks || [];
    const area = document.getElementById('interactionArea') || document.getElementById('detailBody');

    if (!tasks.length) {
      area.innerHTML = `<div class="interaction-panel"><div class="muted-text">無可用題目。</div></div>`;
      return;
    }

    const s = window.getNodeInteractionState(node.id);
    if (!s.taskOrder || s.taskOrder.length !== tasks.length) {
      s.taskOrder = [...Array(tasks.length).keys()].sort(() => Math.random() - 0.5);
      s.activeTaskIndex = 0;
      s.answers = [];
      window.setNodeInteractionState(node.id, s);
    }

    const taskIdx = s.activeTaskIndex || 0;
    const task = tasks[s.taskOrder[taskIdx]];
    const currentAnswers = s.answers || [];
    const feedback = (s.feedbackByTaskIndex || {})[s.taskOrder[taskIdx]];

    const answerHtml = currentAnswers.map((a, i) => `
      <div class="chip" onclick="window.removeChunk(${i})">
        ${window.escapeHtml(a)} <button onclick="event.stopPropagation(); window.speakKo('${window.escapeJsSingle(a)}')" class="mini-speak">▶</button>
      </div>
    `).join('');

    const bank = (task.chunks || []).map(c => `
      <div class="chip" onclick="window.addChunk('${window.escapeJsSingle(c)}')">
        ${window.escapeHtml(c)}
      </div>
    `).join('');

    area.innerHTML = `
      <div class="interaction-panel animate-in">
        <div class="interaction-label">🧩 詞塊組句練習 (${taskIdx + 1}/${tasks.length})</div>
        <div class="muted-text" style="margin-bottom:12px;">${window.escapeHtml(window.i18nText(task.prompt_i18n, locale, task.prompt_zh_tw || ''))}</div>
        
        <div class="assembly-zone">
          <div class="assembly-answer">${answerHtml || '<div class="tiny-text muted">請選擇詞塊...</div>'}</div>
          <div class="chunk-cloud" style="margin-top:16px;">${bank}</div>
        </div>

        <div class="btn-row" style="margin-top:20px;">
          <button class="btn" onclick="window.clearAssembly()">清空</button>
          <button class="btn primary" onclick="window.checkAssembly()">檢查</button>
          <button class="btn" onclick="window.nextTask()">下一題</button>
        </div>
        ${feedback ? `<div class="feedback-box ${feedback.kind}">${window.escapeHtml(feedback.message)}</div>` : ''}
      </div>
    `;
  }

  function renderResponseBuilderMode(node) {
    const locale = window.currentLocale();
    const items = node.payload.items || [];
    const area = document.getElementById('interactionArea') || document.getElementById('detailBody');
    const s = window.getNodeInteractionState(node.id);
    const chosen = s.chosenByIndex || {};

    const html = items.map((item, idx) => `
      <div class="interaction-panel-item" style="margin-bottom:20px; padding-bottom:16px; border-bottom:1px dashed var(--line);">
        <div class="muted-text" style="font-weight:700; margin-bottom:8px;">情境 ${idx + 1}: ${window.escapeHtml(item.prompt_ko || '')}</div>
        <div class="btn-group" style="flex-wrap:wrap; gap:8px;">
          ${(item.response_choices_ko || []).map(choice => `
            <button class="btn ${chosen[idx] === choice ? 'success' : ''}" onclick="window.pickResponse(${idx}, '${window.escapeJsSingle(choice)}')">
              ${window.escapeHtml(choice)}
            </button>
          `).join('')}
        </div>
      </div>
    `).join('');

    area.innerHTML = `
      <div class="interaction-panel animate-in">
        <div class="interaction-label">💬 回應選擇練習</div>
        ${html}
      </div>
    `;
  }

  function renderFlashcardReviewMode(node) {
    const locale = window.currentLocale();
    const payload = node.payload || {};
    const cards = payload.cards || payload.items || [];
    const area = document.getElementById('interactionArea') || document.getElementById('detailBody');

    if (!cards.length) {
      area.innerHTML = `<div class="interaction-panel"><div class="muted-text">無可用閃卡。</div></div>`;
      return;
    }

    const s = window.getNodeInteractionState(node.id);
    if (!s.cardOrder || s.cardOrder.length !== cards.length) {
      s.cardOrder = [...Array(cards.length).keys()].sort(() => Math.random() - 0.5);
      s.activeCardIndex = 0;
      s.revealedCard = false;
      window.setNodeInteractionState(node.id, s);
    }

    const activeIdx = s.activeCardIndex || 0;
    const card = cards[s.cardOrder[activeIdx]];
    const revealed = !!s.revealedCard;

    area.innerHTML = `
      <div class="interaction-panel animate-in">
        <div class="interaction-label">🗂️ 閃卡複習 (${activeIdx + 1}/${cards.length})</div>
        <div class="summary-box" style="background:#fff; border-radius:12px; padding:20px; text-align:center;">
          <div class="tiny-text muted" style="margin-bottom:8px;">Front</div>
          <div style="font-size:24px; font-weight:800; color:var(--accent);">${window.escapeHtml(card.front_ko || '')}</div>
          <div class="muted-text" style="margin-top:10px;">${window.escapeHtml(window.i18nText(card.prompt_i18n, locale, ''))}</div>
        </div>
        
        <div class="btn-row" style="margin-top:16px;">
          <button class="btn primary" onclick="window.toggleFlashcardReveal()">${revealed ? '隱藏答案' : '顯示答案'}</button>
        </div>

        ${revealed ? `
          <div class="summary-box animate-in" style="margin-top:16px; background:var(--ok-soft); border-color:var(--ok);">
            <div class="tiny-text muted" style="margin-bottom:8px;">Back / Answer</div>
            <div style="font-size:20px; font-weight:700;">${window.escapeHtml(card.back_ko || '')}</div>
            <div class="muted-text" style="margin-top:6px;">${window.escapeHtml(window.i18nText(card.answer_i18n, locale, ''))}</div>
            ${card.note_i18n ? `<div class="tiny-text" style="margin-top:10px; border-top:1px dashed #ccc; padding-top:8px;">💡 ${window.escapeHtml(window.i18nText(card.note_i18n, locale, ''))}</div>` : ''}
          </div>
        ` : ''}

        <div class="btn-row" style="margin-top:20px;">
          <button class="btn" onclick="window.prevFlashcard()">上一張</button>
          <button class="btn" onclick="window.nextFlashcard()">下一張</button>
        </div>
      </div>
    `;
  }

  // Registry
  window.RendererRegistry.registerContent('practice_card', renderPracticeCard);
  window.RendererRegistry.registerContent('review_card', renderReviewCard);

  window.RendererRegistry.registerInteraction('chunk_assembly', renderChunkAssemblyMode);
  window.RendererRegistry.registerInteraction('response_builder', renderResponseBuilderMode);
  window.RendererRegistry.registerInteraction('flashcard_review', renderFlashcardReviewMode);
  window.RendererRegistry.registerInteraction('review_retrieval', renderFlashcardReviewMode); // Shared for now

  // --- Global Helpers ---

  window.renderCurrentInteractionOnly = function () {
    const node = window.state.data.sequence[window.state.currentIndex];
    const mode = node.payload.mode || node.output_mode || 'none';
    const renderer = window.RendererRegistry.renderers[mode];
    if (renderer) renderer(node);
  };

  window.addChunk = (txt) => {
    const node = window.state.data.sequence[window.state.currentIndex];
    const s = window.getNodeInteractionState(node.id);
    if (!s.answers) s.answers = [];
    s.answers.push(txt);
    window.setNodeInteractionState(node.id, s);
    window.renderCurrentInteractionOnly();
  };

  window.removeChunk = (idx) => {
    const node = window.state.data.sequence[window.state.currentIndex];
    const s = window.getNodeInteractionState(node.id);
    if (s.answers) s.answers.splice(idx, 1);
    window.setNodeInteractionState(node.id, s);
    window.renderCurrentInteractionOnly();
  };

  window.clearAssembly = () => {
    const node = window.state.data.sequence[window.state.currentIndex];
    const s = window.getNodeInteractionState(node.id);
    s.answers = [];
    s.feedbackByTaskIndex = {};
    window.setNodeInteractionState(node.id, s);
    window.renderCurrentInteractionOnly();
  };

  window.checkAssembly = () => {
    const node = window.state.data.sequence[window.state.currentIndex];
    const s = window.getNodeInteractionState(node.id);
    const tasks = node.payload.tasks || [];
    const taskIdx = s.taskOrder[s.activeTaskIndex || 0];
    const task = tasks[taskIdx];
    const answer = (s.answers || []).join(' ').trim();

    let kind = 'incorrect';
    let message = '不完全正確，再試試看！';
    if ((task.target_examples || []).includes(answer)) {
      kind = 'best_fit';
      message = '完全正確！';
    }

    if (!s.feedbackByTaskIndex) s.feedbackByTaskIndex = {};
    s.feedbackByTaskIndex[taskIdx] = { kind, message };
    window.setNodeInteractionState(node.id, s);
    window.renderCurrentInteractionOnly();
  };

  window.nextTask = () => {
    const node = window.state.data.sequence[window.state.currentIndex];
    const s = window.getNodeInteractionState(node.id);
    const tasks = node.payload.tasks || [];
    s.activeTaskIndex = (s.activeTaskIndex || 0) + 1;
    if (s.activeTaskIndex >= tasks.length) s.activeTaskIndex = 0;
    s.answers = [];
    window.setNodeInteractionState(node.id, s);
    window.renderCurrentInteractionOnly();
  };

  window.pickResponse = (idx, choice) => {
    const node = window.state.data.sequence[window.state.currentIndex];
    const s = window.getNodeInteractionState(node.id);
    if (!s.chosenByIndex) s.chosenByIndex = {};
    s.chosenByIndex[idx] = choice;
    window.setNodeInteractionState(node.id, s);
    window.renderCurrentInteractionOnly();
  };

  window.toggleFlashcardReveal = () => {
    const node = window.state.data.sequence[window.state.currentIndex];
    const s = window.getNodeInteractionState(node.id);
    s.revealedCard = !s.revealedCard;
    window.setNodeInteractionState(node.id, s);
    window.renderCurrentInteractionOnly();
  };

  window.nextFlashcard = () => {
    const node = window.state.data.sequence[window.state.currentIndex];
    const s = window.getNodeInteractionState(node.id);
    const count = (node.payload.cards || node.payload.items || []).length;
    s.activeCardIndex = (s.activeCardIndex || 0) + 1;
    if (s.activeCardIndex >= count) s.activeCardIndex = 0;
    s.revealedCard = false;
    window.setNodeInteractionState(node.id, s);
    window.renderCurrentInteractionOnly();
  };

  window.prevFlashcard = () => {
    const node = window.state.data.sequence[window.state.currentIndex];
    const s = window.getNodeInteractionState(node.id);
    const count = (node.payload.cards || node.payload.items || []).length;
    s.activeCardIndex = (s.activeCardIndex || 0) - 1;
    if (s.activeCardIndex < 0) s.activeCardIndex = count - 1;
    s.revealedCard = false;
    window.setNodeInteractionState(node.id, s);
    window.renderCurrentInteractionOnly();
  };

})();
