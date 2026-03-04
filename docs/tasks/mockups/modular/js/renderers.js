/**
 * Lingourmet Mockup Content Renderers & Registry logic
 */

window.showBilingual = function () {
  return window.state.progress.prefs.showBilingual !== false;
};

// --- Renderer Registry Contract ---

window.RendererRegistry = {
  contentRenderers: {},     // keyed by content_form
  interactionRenderers: {}, // keyed by output_mode
  combinedRenderers: {},    // keyed by "form:mode" for special cases

  registerContent(form, fn) {
    this.contentRenderers[form] = fn;
  },

  registerInteraction(mode, fn) {
    this.interactionRenderers[mode] = fn;
  },

  registerCombined(form, mode, fn) {
    this.combinedRenderers[`${form}:${mode}`] = fn;
  },

  /**
   * Dispatch rendering for a node.
   * Returns: { contentHtml, interactionHtml }
   */
  dispatch(node) {
    const payload = node.payload || {};
    const form = node.content_form || 'unknown';
    const mode = node.output_mode || 'none';

    let contentHtml = '';
    let interactionHtml = '';

    // 1. Combined Priority
    const combinedKey = `${form}:${mode}`;
    if (this.combinedRenderers[combinedKey]) {
      // Note: Combined renderers return an object or handle both
      const result = this.combinedRenderers[combinedKey](payload, node);
      if (typeof result === 'string') {
        contentHtml = result;
      } else {
        contentHtml = result.contentHtml || '';
        interactionHtml = result.interactionHtml || '';
      }
    } else {
      // 2. Standard content dispatch
      if (this.contentRenderers[form]) {
        contentHtml = this.contentRenderers[form](payload, node);
      } else {
        contentHtml = this.renderUnknownForm(form, payload);
      }

      // 3. Standard interaction dispatch
      if (mode !== 'none' && mode !== 'unknown') {
        if (this.interactionRenderers[mode]) {
          interactionHtml = this.interactionRenderers[mode](node);
        } else {
          interactionHtml = this.renderUnsupportedMode(mode);
        }
      }
    }

    return { contentHtml, interactionHtml };
  },

  // --- Fallback Renderers ---

  renderUnknownForm(form, payload) {
    return `
            <div class="interaction-panel" style="border-color:var(--warn); background:var(--warn-soft);">
                <div class="interaction-label" style="color:var(--warn);">⚠️ 未知的內容形式 (Unknown Form)</div>
                <div class="muted-text" style="margin-bottom:12px;">
                    系統無法識別 <code>content_form: "${window.escapeHtml(form)}"</code>。
                </div>
                <details style="font-size:11px; color:var(--muted);">
                    <summary>檢視原始數據 (Payload)</summary>
                    <pre style="background:#fff; padding:8px; border-radius:4px; margin-top:4px; overflow:auto;">${window.escapeHtml(JSON.stringify(payload, null, 2))}</pre>
                </details>
            </div>
        `;
  },

  renderUnsupportedMode(mode) {
    return `
            <div class="interaction-panel" style="border-style:dashed; opacity:0.7;">
                <div class="interaction-label" style="color:var(--muted);">ℹ️ 不支援的互動模式 (Unsupported Mode)</div>
                <div class="muted-text">
                    當前 Viewer 尚未實作 <code>output_mode: "${window.escapeHtml(mode)}"</code> 的互動邏輯。
                </div>
            </div>
        `;
  },

  renderMalformedPayload(form, mode, missingFields) {
    return `
             <div class="interaction-panel" style="border-color:var(--accent); background:var(--accent-soft);">
                <div class="interaction-label">❌ 數據格式錯誤 (Malformed Payload)</div>
                <div class="muted-text">
                    <code>${form}:${mode}</code> 缺漏必要欄位: <strong>${missingFields.join(', ')}</strong>
                </div>
            </div>
        `;
  }
};

// --- Detail Rendering Helpers ---

window.renderDetailHeader = function (node) {
  const header = document.getElementById('detailHeader');
  header.innerHTML = `
    <div class="content-header animate-in">
      <div class="type-tags">
        <span class="type-tag">${node.learning_role}</span>
        <span class="type-tag" style="background:var(--accent2-soft); color:var(--accent2);">${node.candidate_type}</span>
      </div>
      <h1>${node.title_zh_tw}</h1>
    </div>
  `;
};

window.renderDetailSummary = function (node) {
  const summaryBox = document.getElementById('detailSummary');
  summaryBox.innerHTML = `
    <div class="content-summary animate-in">
      <div style="font-weight:700; margin-bottom:8px;">本節目標</div>
      <div class="muted-text">${node.summary_zh_tw}</div>
      <div class="summary-grid">
        <div class="summary-box">
          <span class="label">預期輸出</span>
          ${node.expected_output_zh_tw || '觀察與理解'}
        </div>
        <div class="summary-box">
          <span class="label">技能焦查</span>
          ${(node.skill_focus || []).join(' / ')}
        </div>
      </div>
    </div>
  `;
};

// --- Content Form implementation functions ---

const renderDialogue = function (payload) {
  const turns = payload.dialogue_turns || [];
  if (!payload.dialogue_turns) return window.RendererRegistry.renderMalformedPayload('dialogue', 'none', ['dialogue_turns']);

  const html = turns.map((t, idx) => {
    const isRight = idx % 2 !== 0;
    return `
      <div class="dialogue-turn ${isRight ? 'turn-right' : 'turn-left'}">
        <div class="speaker-label">${window.escapeHtml(t.speaker)}</div>
        <div class="bubble">
          <div class="bubble-ko">${window.escapeHtml(t.text)} ${window.renderSpeakButton(t.text)}</div>
          ${window.showBilingual() && t.zh_tw ? `<div class="bubble-zh">${window.escapeHtml(t.zh_tw)}</div>` : ''}
        </div>
      </div>
    `;
  }).join('');
  return `<div class="content-block"><div class="block-title">情境對話</div><div class="dialogue-wrap">${html}</div></div>`;
};

const renderNotice = function (payload) {
  const items = payload.notice_items || [];
  const itemZh = payload.notice_items_zh_tw || [];
  if (!payload.notice_items) return window.RendererRegistry.renderMalformedPayload('notice', 'none', ['notice_items']);

  const html = items.map((ko, idx) => `
    <div class="notice-item">
      <span class="notice-ko">${window.escapeHtml(ko)} ${window.renderSpeakButton(ko)}</span>
      ${window.showBilingual() && itemZh[idx] ? `<span class="notice-zh">${window.escapeHtml(itemZh[idx])}</span>` : ''}
    </div>
  `).join('');
  return `<div class="content-block"><div class="block-title">告示與看板</div><div class="notice-board">${html}</div></div>`;
};

const renderMessageThread = function (payload) {
  const msgs = payload.messages || [];
  if (!payload.messages) return window.RendererRegistry.renderMalformedPayload('message_thread', 'none', ['messages']);

  const html = msgs.map((m, idx) => {
    const isMe = typeof m.is_self === 'boolean' ? m.is_self : idx % 2 === 0;
    return `
      <div class="msg-group ${isMe ? 'msg-right' : 'msg-left'}">
        <div class="msg-sender">${window.escapeHtml(m.sender)}</div>
        <div class="msg-bubble">
          <div class="msg-ko">${window.escapeHtml(m.text)} ${window.renderSpeakButton(m.text)}</div>
          ${window.showBilingual() && m.zh_tw ? `<div class="msg-zh">${window.escapeHtml(m.zh_tw)}</div>` : ''}
        </div>
      </div>
    `;
  }).join('');
  return `<div class="content-block"><div class="block-title">簡訊對話</div><div class="message-container">${html || '<div class="empty-state">無訊息</div>'}</div></div>`;
};

const renderComparison = function (payload) {
  const opts = payload.options || [];
  if (!payload.options) return window.RendererRegistry.renderMalformedPayload('comparison_card', 'none', ['options']);

  const html = opts.map(o => `
    <div class="compare-card">
      <span class="card-id">${o.id}</span>
      <h4>
        ${window.escapeHtml(o.label_ko || o.label_zh_tw || '')}
        ${(window.showBilingual() && o.label_zh_tw && o.label_ko) ? `<div class="tiny-text muted" style="font-weight:500; margin-top:4px;">${window.escapeHtml(o.label_zh_tw)}</div>` : ''}
      </h4>
      <div class="price-tag">${(o.price_krw || 0).toLocaleString()} KRW</div>
      <div class="compare-pros">
        ${(o.pros_ko || o.pros_zh_tw || []).map((p, idx) => `
          <div class="pro-item">
            ${window.escapeHtml(p)}
            ${(window.showBilingual() && o.pros_ko && o.pros_zh_tw && o.pros_zh_tw[idx]) ? `<div class="tiny-text muted" style="margin-top:2px;">${window.escapeHtml(o.pros_zh_tw[idx])}</div>` : ''}
          </div>
        `).join('')}
      </div>
    </div>
  `).join('');

  let frameNote = '';
  if (payload.reason_frame_ko || payload.reason_frame_zh_tw) {
    frameNote = `<div class="summary-box" style="margin-top:20px; border-style:solid; border-color:var(--accent2-soft); background:var(--accent2-soft);">
      <span class="label" style="color:var(--accent2);">推薦理由句型</span>
      ${window.escapeHtml(payload.reason_frame_ko || payload.reason_frame_zh_tw || '')}
      ${(window.showBilingual() && payload.reason_frame_ko && payload.reason_frame_zh_tw) ? `<div class="tiny-text muted" style="margin-top:4px;">${window.escapeHtml(payload.reason_frame_zh_tw)}</div>` : ''}
    </div>`;
  }

  return `<div class="content-block"><div class="block-title">方案比較</div><div class="comparison-grid">${html}</div>${frameNote}</div>`;
};

const renderPatternCard = function (payload) {
  const frames = payload.frames || [];
  const html = frames.map(f => `
    <div class="pattern-entry">
      <div class="pattern-formula">${window.escapeHtml(f.frame)}</div>
      <div class="pattern-use-case">${window.escapeHtml(f.use_zh_tw)}</div>
      <div class="slot-tags">
        <span class="slot-label">詞類/插槽:</span>
        ${(f.slots_zh_tw || []).map(s => `<span class="slot-tag">${window.escapeHtml(s)}</span>`).join('')}
      </div>
    </div>
  `).join('');
  return `<div class="content-block"><div class="block-title">句型重點</div><div class="pattern-card-box">${html || '<div class="empty-state">無資料</div>'}</div></div>`;
};

const renderPracticeCardHead = function (payload, node) {
  const modeLabel = {
    chunk_assembly: '拼句型練習',
    response_builder: '回應建構',
    guided: '引導式練習'
  }[payload.mode || node.output_mode] || '練習卡';

  const taskCount = Array.isArray(payload.tasks) ? payload.tasks.length : 0;
  const itemCount = Array.isArray(payload.items) ? payload.items.length : 0;
  const total = taskCount || itemCount;

  return `
    <div class="card-block animate-in">
      <div class="block-title">Practice Card</div>
      <div class="muted-text" style="margin-bottom:10px;">${window.escapeHtml(modeLabel)}</div>
      ${payload.prompt_zh_tw ? `<div style="margin-bottom:10px;">${window.escapeHtml(payload.prompt_zh_tw)}</div>` : ''}
      ${total ? `<div class="tiny-text muted">本節練習題數：${total}</div>` : ''}
      <div class="tiny-text muted" style="margin-top:8px;">互動內容請見下方練習區塊。</div>
    </div>
  `;
};

const renderComprehensionCheck = function (payload) {
  const items = payload.items || [];
  const qType = payload.question_type || 'unknown';
  const html = items.map((item, idx) => `
    <div class="pattern-entry">
      <div class="tiny-text muted">題目 ${idx + 1}</div>
      <div style="font-weight:600; margin:4px 0 8px;">${window.escapeHtml(item.prompt_zh_tw || item.prompt_ko || '')}</div>
      ${(item.response_choices_ko || []).length ? `
        <div class="chip-cloud">
          ${(item.response_choices_ko || []).map(c => `
            <span class="word-chip">
              ${window.escapeHtml(c)}
              ${window.renderSpeakInline(c)}
              ${window.showBilingual() && item.response_gloss_by_ko && item.response_gloss_by_ko[c] ? `
                <span class="tiny-text muted" style="display:block; margin-top:3px;">${window.escapeHtml(item.response_gloss_by_ko[c])}</span>
              ` : ''}
            </span>
          `).join('')}
        </div>
      ` : ''}
    </div>
  `).join('');

  return `
    <div class="content-block">
      <div class="block-title">理解檢核</div>
      <div class="tiny-text muted" style="margin-bottom:10px;">題型：${window.escapeHtml(qType)}</div>
      <div class="pattern-card-box">${html || '<div class="empty-state">無題目資料</div>'}</div>
    </div>
  `;
};

const renderRoleplayPrompt = function (payload) {
  return `
    <div class="card-block animate-in">
      <div class="block-title">Roleplay Prompt</div>
      ${payload.scenery_ko ? `
        <div style="margin-bottom:8px;">
          <div class="tiny-text muted">情境（韓文）</div>
          <div>${window.escapeHtml(payload.scenery_ko)}</div>
          ${window.showBilingual() && payload.scenery_zh_tw ? `<div class="tiny-text muted" style="margin-top:4px;">${window.escapeHtml(payload.scenery_zh_tw)}</div>` : ''}
        </div>` : ''
    }
      ${Array.isArray(payload.constraints_zh_tw) && payload.constraints_zh_tw.length ? `
        <div style="margin-bottom:8px;">
          <div class="tiny-text muted">限制條件</div>
          <ul style="margin:6px 0 0 18px;">${payload.constraints_zh_tw.map(v => `<li>${window.escapeHtml(v)}</li>`).join('')}</ul>
        </div>` : ''
    }
      ${Array.isArray(payload.required_patterns_zh_tw) && payload.required_patterns_zh_tw.length ? `
        <div>
          <div class="tiny-text muted">必用句型</div>
          <div class="chip-cloud" style="margin-top:6px;">
            ${payload.required_patterns_zh_tw.map(v => `<span class="word-chip">${window.escapeHtml(v)}</span>`).join('')}
          </div>
        </div>` : ''
    }
    </div>
  `;
};

const renderMessagePrompt = function (payload) {
  return `
    <div class="card-block animate-in">
      <div class="block-title">Message Prompt</div>
      ${payload.prompt_ko ? `<div style="font-weight:700;">${window.escapeHtml(payload.prompt_ko)}</div>` : ''}
      ${window.showBilingual() && payload.prompt_zh_tw ? `<div class="tiny-text muted" style="margin-top:6px;">${window.escapeHtml(payload.prompt_zh_tw)}</div>` : ''}
      ${Array.isArray(payload.must_include_zh_tw) && payload.must_include_zh_tw.length ? `
        <div style="margin-top:10px;">
          <div class="tiny-text muted">需包含</div>
          <ul style="margin:6px 0 0 18px;">${payload.must_include_zh_tw.map(v => `<li>${window.escapeHtml(v)}</li>`).join('')}</ul>
        </div>` : ''
    }
      ${Array.isArray(payload.example_shape_ko) && payload.example_shape_ko.length ? `
        <div style="margin-top:10px;">
          <div class="tiny-text muted">句型輪廓</div>
          ${(payload.example_shape_ko || []).map((ko, i) => `
            <div style="padding:8px 10px; background:#faf7f1; border-radius:8px; margin-top:6px;">
              <div>${window.escapeHtml(ko)}</div>
              ${window.showBilingual() && payload.example_shape_zh_tw && payload.example_shape_zh_tw[i] ? `<div class="tiny-text muted">${window.escapeHtml(payload.example_shape_zh_tw[i])}</div>` : ''}
            </div>
          `).join('')}
        </div>` : ''
    }
    </div>
  `;
};

const renderReviewCard = function (payload) {
  const prompts = payload.prompts_zh_tw || [];
  return `
    <div class="card-block animate-in">
      <div class="block-title">Review Card</div>
      <div class="muted-text" style="margin-bottom:8px;">先回想，再用下方互動區塊檢視提示與答案。</div>
      ${payload.hint_policy ? `<div class="tiny-text muted" style="margin-bottom:8px;">提示策略：${window.escapeHtml(payload.hint_policy)}</div>` : ''}
      ${prompts.length ? `
        <ol style="margin:0 0 0 18px; padding:0;">
          ${prompts.map(p => `<li style="margin-bottom:6px;">${window.escapeHtml(p)}</li>`).join('')}
        </ol>` : ''
    }
    </div>
  `;
};

const renderQuizItem = function (payload) {
  const item = payload.item || {};
  const choices = Array.isArray(item.choices) ? item.choices : [];
  const answer = item.answer_key ? item.answer_key.value : '';
  const answerText = Array.isArray(answer) ? answer.join(' / ') : String(answer || '');
  return `
    <div class="content-block">
      <div class="block-title">題庫題目</div>
      <div class="summary-box" style="margin-bottom:12px;">
        <span class="label">題型 / 技能 / 難度</span>
        ${window.escapeHtml(item.item_type || 'unknown')} / ${window.escapeHtml(item.skill || 'unknown')} / ${window.escapeHtml(item.difficulty_tier || 'L1')}
      </div>
      <div style="font-weight:700; margin-bottom:6px;">${window.escapeHtml(item.prompt_zh_tw || '')}</div>
      ${item.prompt_ko ? `<div style="padding:10px; background:#fff; border:1px solid var(--line); border-radius:8px; margin-bottom:10px;">
        <div style="font-size:16px; font-weight:700;">${window.escapeHtml(item.prompt_ko)} ${window.renderSpeakButton(item.prompt_ko)}</div>
      </div>` : ''}
      ${choices.length ? `
        <div class="chip-cloud" style="margin-bottom:10px;">
          ${choices.map((c, idx) => `<span class="word-chip">${idx + 1}. ${window.escapeHtml(c)} ${window.renderSpeakInline(c)}</span>`).join('')}
        </div>
      ` : ''}
      <details>
        <summary style="cursor:pointer; color:var(--accent2); font-weight:700;">顯示答案與解析</summary>
        <div class="summary-box" style="margin-top:8px; border-color:var(--ok-soft); background:var(--ok-soft);">
          <span class="label" style="color:var(--ok);">答案</span>
          ${window.escapeHtml(answerText)}
          ${item.explanation_zh_tw ? `<div class="tiny-text muted" style="margin-top:6px;">${window.escapeHtml(item.explanation_zh_tw)}</div>` : ''}
        </div>
      </details>
      ${item.tags?.length ? `<div class="tiny-text muted" style="margin-top:10px;">tags: ${item.tags.map(t => window.escapeHtml(t)).join(', ')}</div>` : ''}
    </div>
  `;
};

const applyInlineMarkdown = function (text) {
  return window.escapeHtml(text || '')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');
};

const markdownToHtmlLite = function (md) {
  const src = String(md || '').replace(/\r\n/g, '\n');
  const lines = src.split('\n');
  const out = [];
  let i = 0;

  const isTableSeparator = (line) => /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line);
  const isTableRow = (line) => line.includes('|');

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    if (!trimmed) {
      i += 1;
      continue;
    }

    // Table block
    if (i + 1 < lines.length && isTableRow(lines[i]) && isTableSeparator(lines[i + 1])) {
      const headerCells = lines[i].split('|').map(c => c.trim()).filter(Boolean);
      i += 2;
      const bodyRows = [];
      while (i < lines.length && isTableRow(lines[i]) && lines[i].trim()) {
        const rowCells = lines[i].split('|').map(c => c.trim()).filter(Boolean);
        if (rowCells.length) bodyRows.push(rowCells);
        i += 1;
      }
      out.push(`
        <div class="md-table-wrap">
          <table class="md-table">
            <thead><tr>${headerCells.map(c => `<th>${applyInlineMarkdown(c)}</th>`).join('')}</tr></thead>
            <tbody>${bodyRows.map(r => `<tr>${r.map(c => `<td>${applyInlineMarkdown(c)}</td>`).join('')}</tr>`).join('')}</tbody>
          </table>
        </div>
      `);
      continue;
    }

    // Bullet list
    if (trimmed.startsWith('- ')) {
      const items = [];
      while (i < lines.length && lines[i].trim().startsWith('- ')) {
        items.push(lines[i].trim().slice(2));
        i += 1;
      }
      out.push(`<ul class="grammar-point-list">${items.map(p => `<li>${applyInlineMarkdown(p)}</li>`).join('')}</ul>`);
      continue;
    }

    // Paragraph
    out.push(`<p class="md-paragraph">${applyInlineMarkdown(trimmed)}</p>`);
    i += 1;
  }

  return out.join('');
};

const renderGrammar = function (payload) {
  const sections = payload.sections || [];
  const html = sections.map(s => `
    <details open>
      <summary>${window.escapeHtml(s.title_zh_tw)}</summary>
      <div class="grammar-body">
        ${s.explanation_md
      ? `<div class="md-block">${markdownToHtmlLite(s.explanation_md)}</div>`
      : `<ul class="grammar-point-list">
              ${(s.points_zh_tw || []).map(p => `<li>${window.escapeHtml(p)}</li>`).join('')}
            </ul>`
    }
      </div>
    </details>
  `).join('');
  return `<div class="content-block"><div class="block-title">文法詳解</div><div class="grammar-accordion">${html || '<div class="empty-state">無資料</div>'}</div></div>`;
};

const renderDictionary = function (payload) {
  const sections = payload.sections || [];
  const html = sections.map(s => {
    const gloss = s.item_gloss_by_ko || {};
    return `
      <div class="dict-section">
        <span class="dict-box-title">${window.escapeHtml(s.title_zh_tw)}</span>
        <div class="chunk-cloud">
          ${(s.items || []).map(it => `
            <div class="cloud-chunk">
              <strong>${window.escapeHtml(it)}</strong> ${window.renderSpeakButton(it)}
              ${window.showBilingual() && gloss[it] ? `<span class="chunk-zh">${window.escapeHtml(gloss[it])}</span>` : ''}
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }).join('');
  return `<div class="content-block"><div class="block-title">核心詞彙與短語</div><div>${html || '<div class="empty-state">無資料</div>'}</div></div>`;
};

// --- Interaction Mode implement functions ---

const renderChunkAssemblyMode = function (node) {
  const payload = node.payload;
  const nodeState = window.getNodeInteractionState(node.id);
  const tasks = payload.tasks || [];
  const taskIdx = nodeState.activeTaskIndex || 0;
  const task = tasks[taskIdx];
  if (!task) {
    return `
      <div class="interaction-panel">
        <div class="interaction-label">ℹ️ 本節無互動題</div>
        <div class="muted-text">此節點目前是內容瀏覽模式，未提供可操作的 chunk_assembly tasks。</div>
      </div>
    `;
  }

  const currentAnswers = nodeState.answers || [];
  const gloss = task.chunk_gloss_by_ko || {};

  const answerHtml = currentAnswers.map((a, i) => `
    <div class="chip" onclick="removeChunk(${i})">
      ${window.escapeHtml(a)} ${window.showBilingual() && gloss[a] ? `<span class="tiny-text muted">(${gloss[a]})</span>` : ''} ${window.renderSpeakButton(a)}
    </div>
  `).join('');

  const bankHtml = (task.chunks || []).map((c, i) => {
    const usedCount = currentAnswers.filter(x => x === c).length;
    const totalCount = (task.chunks || []).filter(x => x === c).length;
    const isUsed = usedCount >= totalCount;
    return `<div class="chip ${isUsed ? 'used' : ''}" onclick="${isUsed ? '' : `addChunk('${c.replace(/'/g, "\\'")}')`}">
      ${window.escapeHtml(c)} ${window.showBilingual() && gloss[c] ? `<span class="tiny-text muted">(${gloss[c]})</span>` : ''} ${window.renderSpeakButton(c)}
    </div>`;
  }).join('');

  return `
    <div class="interaction-panel animate-in">
      <div class="interaction-label">🧩 詞塊組句練習 (${taskIdx + 1}/${tasks.length})</div>
      <div class="muted-text" style="margin-bottom:12px;">${window.escapeHtml(task.prompt_zh_tw)}</div>
      
      <div class="assembly-zone">
        <div class="block-title" style="margin-bottom:8px; font-size:11px;">你的組句 (點擊移除)</div>
        <div class="assembly-answer">${answerHtml || '<div class="tiny-text muted">請從下方選擇詞塊...</div>'}</div>
        
        <div class="block-title" style="margin-bottom:8px; font-size:11px; margin-top:16px;">詞塊庫</div>
        <div class="chunk-cloud">${bankHtml}</div>
      </div>

      <div class="btn-row">
        <button class="btn" onclick="clearAssembly()">清空</button>
        <button class="btn" onclick="toggleTaskExample()">查看示例</button>
        <button class="btn primary" ${taskIdx >= tasks.length - 1 ? 'disabled' : ''} onclick="nextTask()">下一題</button>
      </div>
      <div id="assemblyExample" class="summary-box" style="display:none; margin-top:16px; border-color:var(--ok-soft); background:var(--ok-soft);">
        <span class="label" style="color:var(--ok);">預期示例</span>
        ${(task.target_examples || []).join(' / ')}
        ${window.showBilingual() && task.target_examples_zh_tw ? `<div class="tiny-text" style="margin-top:4px;">中譯：${task.target_examples_zh_tw.join(' / ')}</div>` : ''}
      </div>
    </div>
  `;
};

const renderResponseBuilderMode = function (node) {
  const items = node.payload.items || [];
  const nodeState = window.getNodeInteractionState(node.id);
  const chosen = nodeState.chosenByIndex || {};
  if (!node.payload.items) return window.RendererRegistry.renderMalformedPayload('practice_card', 'response_builder', ['items']);

  const html = items.map((item, idx) => `
      <div style="margin-bottom:24px; border-bottom:1px dashed var(--line); padding-bottom:16px;">
      <div class="muted-text" style="font-weight:700; margin-bottom:8px;">情境 ${idx + 1}: ${window.escapeHtml(item.prompt_ko)} ${window.renderSpeakButton(item.prompt_ko)}</div>
      ${window.showBilingual() && item.prompt_zh_tw ? `<div class="tiny-text muted" style="margin-bottom:12px;">(${item.prompt_zh_tw})</div>` : ''}
      <div class="btn-group" style="flex-wrap:wrap;">
        ${(item.response_choices_ko || []).map(choice => `
          <button class="btn ${chosen[idx] === choice ? 'success' : ''}" style="font-size:12px; padding: 6px 12px;" onclick="pickResponse(${idx}, '${choice.replace(/'/g, "\\'")}')">
            ${window.escapeHtml(choice)} ${window.renderSpeakInline(choice)}
            ${window.showBilingual() && item.response_gloss_by_ko && item.response_gloss_by_ko[choice] ? `<span class="tiny-text muted" style="display:block; width:100%; margin-top:2px;">${window.escapeHtml(item.response_gloss_by_ko[choice])}</span>` : ''}
          </button>
        `).join('')}
      </div>
    </div>
  `).join('');

  return `
    <div class="interaction-panel animate-in">
      <div class="interaction-label">💬 回應選擇練習</div>
      ${html}
    </div>
  `;
};

const renderGuidedOutputMode = function (node) {
  const nodeState = window.getNodeInteractionState(node.id);
  const isSpeaking = (node.skill_focus || []).includes('speaking');
  return `
    <div class="interaction-panel animate-in">
      <div class="interaction-label">${isSpeaking ? '🎤 口說練習' : '✍️ 任務型寫作'}</div>
      <div class="muted-text" style="margin-bottom:12px;">${node.payload.prompt_zh_tw || node.summary_zh_tw}</div>
      <textarea placeholder="點擊此處輸入回答或練習筆記..." oninput="updateDraft(this.value)">${nodeState.draft || ''}</textarea>
      ${node.payload.must_include_zh_tw ? `<div class="tiny-text muted" style="margin-top:8px;">需包含: ${node.payload.must_include_zh_tw.join(' / ')}</div>` : ''}
    </div>
  `;
};

const renderFrameFillMode = function (node) {
  const frames = node.payload?.frames || [];
  if (!frames.length) {
    return `
      <div class="interaction-panel">
        <div class="interaction-label">ℹ️ Frame Fill</div>
        <div class="muted-text">此節點未提供 frames，請先檢查 payload.frames。</div>
      </div>
    `;
  }
  return `
    <div class="interaction-panel animate-in">
      <div class="interaction-label">🧩 句框填空練習</div>
      ${frames.map((f, idx) => `
        <div style="margin-top:10px; padding:10px; background:#fff; border:1px solid var(--line); border-radius:8px;">
          <div class="tiny-text muted">Frame ${idx + 1}</div>
          <div style="font-weight:700; margin:4px 0;">${window.escapeHtml(f.frame || '')}</div>
          ${f.use_zh_tw ? `<div class="tiny-text muted">${window.escapeHtml(f.use_zh_tw)}</div>` : ''}
        </div>
      `).join('')}
      <div class="tiny-text muted" style="margin-top:10px;">先口頭替換 slot，再到筆記區寫一版完整句子。</div>
    </div>
  `;
};

const renderPatternTransformMode = function (node) {
  const payload = node.payload || {};
  return `
    <div class="interaction-panel animate-in">
      <div class="interaction-label">🔁 句型變換練習</div>
      <div class="tiny-text muted">Transform Type: ${window.escapeHtml(payload.transform_type || 'unspecified')}</div>
      <div style="margin-top:8px;">${window.escapeHtml(payload.prompt_zh_tw || node.summary_zh_tw || '請根據本節句型完成變換。')}</div>
      ${(payload.must_include_zh_tw || []).length ? `
        <div style="margin-top:8px;">
          <div class="tiny-text muted">必含元素</div>
          <div class="chip-cloud">${payload.must_include_zh_tw.map(v => `<span class="word-chip">${window.escapeHtml(v)}</span>`).join('')}</div>
        </div>
      ` : ''}
    </div>
  `;
};

const renderReviewRetrievalMode = function (node) {
  const prompts = node.payload.prompts_zh_tw || [];
  const answers = node.payload.reference_answers_ko || node.payload.answers_ko || [];
  const nodeState = window.getNodeInteractionState(node.id);
  const retrievalDrafts = nodeState.retrievalDrafts || {};
  const revealedHints = nodeState.revealedHints || {};
  const revealedAnswers = nodeState.revealedAnswers || {};
  return `
    <div class="interaction-panel animate-in">
      <div class="interaction-label">🧠 單元複習回想</div>
      <div class="muted-text" style="margin-bottom:16px;">閱讀以下情境，先自己回想，再決定是否查看提示與答案（不自動評分）。</div>
      ${prompts.map((p, i) => `
        <div style="margin-bottom:12px; padding:12px; background:#fff; border-radius:8px; border:1px solid var(--line);">
          <div class="tiny-text muted">情境 ${i + 1}</div>
          <div>${window.escapeHtml(p)}</div>
          <textarea style="margin-top:10px; min-height:70px;" placeholder="先寫下你回想的答案..." oninput="updateRetrievalDraft(${i}, this.value)">${window.escapeHtml(retrievalDrafts[i] || '')}</textarea>
          <div class="btn-group" style="margin-top:8px; gap:6px; flex-wrap:wrap;">
            <button class="btn tiny-text" style="padding:4px 10px;" onclick="toggleRetrievalHint(${i})">${revealedHints[i] ? '隱藏提示' : '顯示提示'}</button>
            <button class="btn tiny-text" style="padding:4px 10px;" onclick="toggleRetrievalAnswer(${i})">${revealedAnswers[i] ? '隱藏答案' : '顯示答案'}</button>
          </div>
          ${revealedHints[i] ? `<div class="tiny-text muted" style="margin-top:8px; padding:8px; background:#faf7f1; border-radius:6px;">提示：先回想本單元的功能句型（點餐請求 / 回應店員 / 付款 / 約見）。</div>` : ''}
          ${revealedAnswers[i] ? `<div style="margin-top:8px; padding:8px; background:#eef8f0; border:1px solid #d0e6d6; border-radius:6px;"><div class="tiny-text muted">參考答案（韓文）</div><div style="font-weight:600;">${window.escapeHtml(answers[i] || '尚未定義')} ${answers[i] ? window.renderSpeakButton(answers[i]) : ''}</div></div>` : ''}
        </div>
      `).join('')}
    </div>
  `;
};

window.renderFreeNote = function (node) {
  const nodeState = window.getNodeInteractionState(node.id);
  return `
    <div style="margin-top:40px; border-top:1px solid var(--line); padding-top:20px;">
      <div class="block-title">個人筆記</div>
      <textarea style="min-height:80px; font-size:13px;" placeholder="記錄本節心得或卡關點..." oninput="updateNote(this.value)">${window.escapeHtml(nodeState.note || '')}</textarea>
    </div>
  `;
};

// --- Registry Initialization ---

window.RendererRegistry.registerContent('dialogue', renderDialogue);
window.RendererRegistry.registerContent('comprehension_check', renderComprehensionCheck);
window.RendererRegistry.registerContent('notice', renderNotice);
window.RendererRegistry.registerContent('message_thread', renderMessageThread);
window.RendererRegistry.registerContent('comparison_card', renderComparison);
window.RendererRegistry.registerContent('pattern_card', renderPatternCard);
window.RendererRegistry.registerContent('grammar_note', renderGrammar);
window.RendererRegistry.registerContent('functional_phrase_pack', renderDictionary);
window.RendererRegistry.registerContent('practice_card', renderPracticeCardHead);
window.RendererRegistry.registerContent('roleplay_prompt', renderRoleplayPrompt);
window.RendererRegistry.registerContent('message_prompt', renderMessagePrompt);
window.RendererRegistry.registerContent('review_card', renderReviewCard);
window.RendererRegistry.registerContent('quiz_item', renderQuizItem);

window.RendererRegistry.registerInteraction('chunk_assembly', renderChunkAssemblyMode);
window.RendererRegistry.registerInteraction('response_builder', renderResponseBuilderMode);
window.RendererRegistry.registerInteraction('frame_fill', renderFrameFillMode);
window.RendererRegistry.registerInteraction('pattern_transform', renderPatternTransformMode);
window.RendererRegistry.registerInteraction('guided', renderGuidedOutputMode);
window.RendererRegistry.registerInteraction('review_retrieval', renderReviewRetrievalMode);

// --- Global Interaction Wrappers ---

window.addChunk = (txt) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  if (!s.answers) s.answers = [];
  s.answers.push(txt);
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentNode();
};
window.removeChunk = (idx) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  s.answers.splice(idx, 1);
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentNode();
};
window.clearAssembly = () => {
  const node = window.state.data.sequence[window.state.currentIndex];
  window.setNodeInteractionState(node.id, { answers: [] });
  window.renderCurrentNode();
};
window.toggleTaskExample = () => {
  const box = document.getElementById('assemblyExample');
  if (!box) return;
  box.style.display = box.style.display === 'none' ? 'block' : 'none';
  if (box.style.display === 'block') window.showToast('已顯示示例');
};
window.nextTask = () => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  s.activeTaskIndex = (s.activeTaskIndex || 0) + 1;
  s.answers = [];
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentNode();
  window.showToast('載入下一題');
};
window.pickResponse = (idx, choice) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  if (!s.chosenByIndex) s.chosenByIndex = {};
  s.chosenByIndex[idx] = choice;
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentNode();
  window.showToast('已更新選擇');
};
window.updateDraft = (val) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  window.setNodeInteractionState(node.id, { draft: val });
};
window.updateRetrievalDraft = (idx, val) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  s.retrievalDrafts = { ...(s.retrievalDrafts || {}), [idx]: val };
  window.setNodeInteractionState(node.id, s);
};
window.toggleRetrievalHint = (idx) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  s.revealedHints = { ...(s.revealedHints || {}), [idx]: !((s.revealedHints || {})[idx]) };
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentNode();
};
window.toggleRetrievalAnswer = (idx) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  s.revealedAnswers = { ...(s.revealedAnswers || {}), [idx]: !((s.revealedAnswers || {})[idx]) };
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentNode();
};
window.updateNote = (val) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  window.setNodeInteractionState(node.id, { note: val });
};
