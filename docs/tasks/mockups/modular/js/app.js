/**
 * Lingourmet Mockup Main App Logic
 */
const BLUEPRINT_PATH = '../a1_u04_unit_blueprint_v0.json';

const elements = {
    unitTitle: document.getElementById('unitTitle'),
    unitSub: document.getElementById('unitSub'),
    metaGrid: document.getElementById('unitMetaGrid'),
    canDo: document.getElementById('canDoList'),
    rolePills: document.getElementById('rolePills'),
    progressText: document.getElementById('progressText'),
    progressFill: document.getElementById('progressFill'),
    followupsBox: document.getElementById('followupsBox'),
    nodeList: document.getElementById('nodeList'),
    roleSummaryBox: document.getElementById('roleSummaryBox'),
    detailHeader: document.getElementById('detailHeader'),
    detailSummary: document.getElementById('detailSummary'),
    detailBody: document.getElementById('detailBody'),
    prevBtn: document.getElementById('prevBtn'),
    nextBtn: document.getElementById('nextBtn'),
    markDoneBtn: document.getElementById('markDoneBtn'),
    markReviewBtn: document.getElementById('markReviewBtn'),
    resetProgressBtn: document.getElementById('resetProgressBtn'),
    jumpNextIncompleteBtn: document.getElementById('jumpNextIncompleteBtn'),
    jumpNextReviewBtn: document.getElementById('jumpNextReviewBtn'),
    jumpFirstOutputBtn: document.getElementById('jumpFirstOutputBtn'),
    jumpReviewSummaryBtn: document.getElementById('jumpReviewSummaryBtn'),
    bilingualToggle: document.getElementById('bilingualToggle'),
    ttsVoiceSelect: document.getElementById('ttsVoiceSelect'),
    ttsTestBtn: document.getElementById('ttsTestBtn'),
    ttsVoiceHint: document.getElementById('ttsVoiceHint')
};

// --- Sidebar & Progress Rendering ---

window.renderSidebar = function () {
    const unit = window.state.data.unit;
    elements.unitTitle.textContent = `${unit.unit_id} ${unit.title_zh_tw}`;
    elements.unitSub.textContent = `${unit.target_language.toUpperCase()} · ${unit.learner_locale_source} · ${unit.level}`;

    elements.metaGrid.innerHTML = `
    <div class="meta-box"><span class="k">主題</span><span class="v">${unit.theme_zh_tw}</span></div>
    <div class="meta-box"><span class="k">預期輸出</span><span class="v">${Math.round(unit.output_ratio_target * 100)}%</span></div>
    <div class="meta-box"><span class="k">節點數</span><span class="v">${window.state.data.sequence.length}</span></div>
    <div class="meta-box"><span class="k">版本</span><span class="v">v1.1 Modular</span></div>
  `;

    elements.canDo.innerHTML = unit.can_do_zh_tw.map(x => `<li>${window.escapeHtml(x)}</li>`).join('');

    const counts = {};
    window.state.data.sequence.forEach(n => counts[n.learning_role] = (counts[n.learning_role] || 0) + 1);
    elements.rolePills.innerHTML = Object.entries(counts).map(([k, v]) => `<span class="pill">${k}: ${v}</span>`).join('');

    elements.bilingualToggle.checked = window.showBilingual();
    if (elements.ttsVoiceSelect && window.state.progress.prefs.ttsVoiceName) {
        elements.ttsVoiceSelect.value = window.state.progress.prefs.ttsVoiceName;
    }
    window.renderRoleSummary();

    if (window.state.data.scheduled_followups?.length) {
        elements.followupsBox.innerHTML = '<h2>跨單元複習排程</h2>' + window.state.data.scheduled_followups.map(f => `
      <div class="meta-box" style="text-align:left; margin-bottom:8px;">
        <div class="k">${f.timing} -> ${f.transfer_to}</div>
        <div class="v" style="font-size:12px;">${f.goal_zh_tw}</div>
      </div>
    `).join('');
    } else {
        elements.followupsBox.innerHTML = '';
    }
};

window.renderRoleSummary = function () {
    const roles = ['immersion_input', 'structure_pattern', 'structure_grammar', 'controlled_output', 'immersion_output', 'review_retrieval'];
    const roleNames = {
        'immersion_input': '沉浸輸入',
        'structure_pattern': '句型結構',
        'structure_grammar': '最小語法',
        'controlled_output': '可控輸出',
        'immersion_output': '任務輸出',
        'review_retrieval': '總結複習'
    };

    const stats = {};
    roles.forEach(r => stats[r] = { total: 0, done: 0 });

    window.state.data.sequence.forEach(node => {
        if (stats[node.learning_role]) {
            stats[node.learning_role].total++;
            if (window.isDone(node.id)) stats[node.learning_role].done++;
        }
    });

    let html = '<h2>學習歷程摘要</h2><div style="display:grid; gap:6px;">';
    roles.forEach(r => {
        if (stats[r].total > 0) {
            const percent = Math.round((stats[r].done / stats[r].total) * 100);
            const isComplete = stats[r].done === stats[r].total;
            html += `
        <div style="font-size:11px; display:flex; justify-content:space-between; align-items:center;">
          <span class="${isComplete ? 'muted-text' : ''}" style="font-weight:${isComplete ? '400' : '600'}">${roleNames[r]}</span>
          <span style="color:${isComplete ? 'var(--ok)' : 'var(--muted)'}">${stats[r].done}/${stats[r].total} (${percent}%)</span>
        </div>
        <div style="height:3px; background:#eeeae3; border-radius:2px; margin-bottom:4px; overflow:hidden;">
          <div style="height:100%; width:${percent}%; background:${isComplete ? 'var(--ok)' : 'var(--accent)'}; transition: width 0.3s;"></div>
        </div>
      `;
        }
    });
    html += '</div>';
    elements.roleSummaryBox.innerHTML = html;
};

window.renderProgress = function () {
    const total = window.state.data.sequence.length;
    const doneCount = window.state.progress.completedNodeIds.length;
    elements.progressText.textContent = `${doneCount}/${total}`;
    elements.progressFill.style.width = total ? `${(doneCount / total) * 100}%` : '0%';
};

window.renderNodeList = function () {
    elements.nodeList.innerHTML = window.state.data.sequence.map((node, idx) => `
    <div class="node-card role-lane-${node.learning_role} ${idx === window.state.currentIndex ? 'active' : ''} ${window.isDone(node.id) ? 'done' : ''} ${window.isReview(node.id) ? 'review-mark' : ''}" onclick="window.setIndex(${idx})">
      <div class="top-row">
        <span class="title">${idx + 1}. ${node.title_zh_tw}</span>
        <span class="tag tiny-text">${node.duration_min}m</span>
      </div>
      <div class="summary">${node.summary_zh_tw}</div>
      <div class="meta-tags">
        <span class="tag">${node.content_form}</span>
        <span class="tag">${node.learning_role}</span>
      </div>
    </div>
  `).join('');
};

window.setIndex = function (idx) {
    window.state.currentIndex = idx;
    window.renderCurrentNode();
};

// --- Core Master Render ---

window.renderCurrentNode = function () {
    const node = window.state.data.sequence[window.state.currentIndex];
    if (!node) return;

    window.renderNodeList();
    window.renderProgress();
    window.renderDetailHeader(node);
    window.renderDetailSummary(node);

    let bodyHtml = '';
    const p = node.payload || {};

    // --- Dispatch via Renderer Registry ---
    const { contentHtml, interactionHtml } = window.RendererRegistry.dispatch(node);
    bodyHtml += contentHtml;
    bodyHtml += interactionHtml;

    bodyHtml += window.renderFreeNote(node);

    elements.detailBody.innerHTML = bodyHtml;
    window.renderFooterButtons();

    document.getElementById('detailContent').scrollTop = 0;
};

window.renderFooterButtons = function () {
    const node = window.state.data.sequence[window.state.currentIndex];
    elements.prevBtn.disabled = window.state.currentIndex <= 0;
    elements.nextBtn.disabled = window.state.currentIndex >= window.state.data.sequence.length - 1;
    elements.markDoneBtn.textContent = window.isDone(node.id) ? '取消完成' : '標記完成';
    elements.markReviewBtn.textContent = window.isReview(node.id) ? '取消待回看' : '標記待回看';

    elements.markDoneBtn.classList.toggle('success', !window.isDone(node.id));
    elements.markReviewBtn.style.color = window.isReview(node.id) ? 'var(--warn)' : '';

    if (window.isDone(node.id)) {
        const nextNode = window.state.data.sequence[window.state.currentIndex + 1];
        if (nextNode) {
            const tip = document.createElement('div');
            tip.style = 'position:absolute; bottom:70px; right:24px; background:var(--ok-soft); border:1px solid var(--ok); padding:8px 12px; border-radius:8px; font-size:12px; animation: bounceIn 0.5s; cursor:pointer;';
            tip.innerHTML = `<strong>完成！</strong> 下一站：${nextNode.title_zh_tw} →`;
            tip.onclick = () => { window.state.currentIndex++; window.renderCurrentNode(); };
            elements.detailBody.appendChild(tip);
        }
    }
};

// --- Events ---

function wireEvents() {
    elements.prevBtn.onclick = () => { if (window.state.currentIndex > 0) { window.state.currentIndex--; window.renderCurrentNode(); } };
    elements.nextBtn.onclick = () => { if (window.state.currentIndex < window.state.data.sequence.length - 1) { window.state.currentIndex++; window.renderCurrentNode(); } };
    elements.markDoneBtn.onclick = () => window.toggleDone(window.state.data.sequence[window.state.currentIndex].id);
    elements.markReviewBtn.onclick = () => window.toggleReview(window.state.data.sequence[window.state.currentIndex].id);
    elements.bilingualToggle.onchange = (e) => {
        window.state.progress.prefs.showBilingual = !!e.target.checked;
        window.saveProgress(true);
        window.renderCurrentNode();
    };
    elements.ttsVoiceSelect.onchange = (e) => {
        window.state.progress.prefs.ttsVoiceName = e.target.value || '';
        window.saveProgress(true);
        window.showToast('已切換韓文語音');
    };
    elements.ttsTestBtn.onclick = () => window.speakKo('안녕하세요. 주문하시겠어요?');

    elements.resetProgressBtn.onclick = () => {
        if (confirm('確定清除及重置所有記錄？')) {
            localStorage.removeItem(window.storageKey());
            location.reload();
        }
    };
    elements.jumpNextIncompleteBtn.onclick = () => {
        const idx = window.state.data.sequence.findIndex((n, i) => i > window.state.currentIndex && !window.isDone(n.id));
        if (idx > -1) { window.state.currentIndex = idx; window.renderCurrentNode(); }
        else {
            const idx2 = window.state.data.sequence.findIndex((n) => !window.isDone(n.id));
            if (idx2 > -1) { window.state.currentIndex = idx2; window.renderCurrentNode(); }
            else window.showToast('全部節點已完成！');
        }
    };
    elements.jumpNextReviewBtn.onclick = () => {
        const idx = window.state.data.sequence.findIndex((n, i) => i > window.state.currentIndex && window.isReview(n.id));
        if (idx > -1) { window.state.currentIndex = idx; window.renderCurrentNode(); }
        else {
            const idx2 = window.state.data.sequence.findIndex((n) => window.isReview(n.id));
            if (idx2 > -1) { window.state.currentIndex = idx2; window.renderCurrentNode(); }
            else window.showToast('沒有標記回看的節點。');
        }
    };
    elements.jumpFirstOutputBtn.onclick = () => {
        const roles = new Set(['controlled_output', 'immersion_output']);
        const idx = window.state.data.sequence.findIndex(n => roles.has(n.learning_role));
        if (idx > -1) { window.state.currentIndex = idx; window.renderCurrentNode(); }
        else window.showToast('未找到輸出練習節點。');
    };
    elements.jumpReviewSummaryBtn.onclick = () => {
        const idx = window.state.data.sequence.findIndex(n => n.learning_role === 'review_retrieval');
        if (idx > -1) { window.state.currentIndex = idx; window.renderCurrentNode(); }
        else window.showToast('未找到總結複習節點。');
    };
}

async function bootstrap() {
    try {
        const resp = await fetch(BLUEPRINT_PATH);
        if (!resp.ok) throw new Error('Blueprint load failed');
        window.state.data = await resp.json();

        window.loadProgress();
        window.refreshTtsVoices();
        if (window.ttsSupported() && 'onvoiceschanged' in window.speechSynthesis) {
            window.speechSynthesis.onvoiceschanged = window.refreshTtsVoices;
        }
        window.renderSidebar();
        wireEvents();
        window.renderCurrentNode();
    } catch (e) {
        elements.detailHeader.innerHTML = `<div class="empty-state">載入數據失敗: ${e.message}</div>`;
    }
}

bootstrap();
