/**
 * Lingourmet Mockup State Management
 */
window.STORAGE_PREFIX = 'agg_gen_mockup_unit_v2:';

window.state = {
    data: null,
    currentIndex: 0,
    progress: {
        completedNodeIds: [],
        reviewNodeIds: [],
        notesByNodeId: {},
        interactionStateByNodeId: {},
        prefs: { showBilingual: true, teachingLocale: 'zh_tw', ttsVoiceName: '' }
    }
};

window.storageKey = function () {
    const unitId = window.state.data?.unit?.unit_id || 'unknown';
    return window.STORAGE_PREFIX + unitId;
};

window.loadProgress = function () {
    try {
        const raw = localStorage.getItem(window.storageKey());
        if (!raw) return;
        const parsed = JSON.parse(raw);
        window.state.progress = {
            completedNodeIds: Array.isArray(parsed.completedNodeIds) ? parsed.completedNodeIds : [],
            reviewNodeIds: Array.isArray(parsed.reviewNodeIds) ? parsed.reviewNodeIds : [],
            notesByNodeId: parsed.notesByNodeId || {},
            interactionStateByNodeId: parsed.interactionStateByNodeId || {},
            prefs: {
                showBilingual: parsed.prefs?.showBilingual !== false,
                teachingLocale: typeof parsed.prefs?.teachingLocale === 'string' ? parsed.prefs.teachingLocale : 'zh_tw',
                ttsVoiceName: typeof parsed.prefs?.ttsVoiceName === 'string' ? parsed.prefs.ttsVoiceName : ''
            }
        };
    } catch (e) {
        console.warn('Progress load failed', e);
    }
};

window.saveProgress = function (silent = false) {
    localStorage.setItem(window.storageKey(), JSON.stringify(window.state.progress));
    if (!silent) {
        if (window.renderProgress) window.renderProgress();
        if (window.renderNodeList) window.renderNodeList();
    }
};

window.isDone = function (id) { return window.state.progress.completedNodeIds.includes(id); };
window.isReview = function (id) { return window.state.progress.reviewNodeIds.includes(id); };

window.toggleDone = function (id) {
    const idx = window.state.progress.completedNodeIds.indexOf(id);
    if (idx > -1) window.state.progress.completedNodeIds.splice(idx, 1);
    else window.state.progress.completedNodeIds.push(id);
    window.saveProgress();
    if (window.renderFooterButtons) window.renderFooterButtons();
};

window.toggleReview = function (id) {
    const idx = window.state.progress.reviewNodeIds.indexOf(id);
    if (idx > -1) window.state.progress.reviewNodeIds.splice(idx, 1);
    else window.state.progress.reviewNodeIds.push(id);
    window.saveProgress();
    if (window.renderFooterButtons) window.renderFooterButtons();
};

window.getNodeInteractionState = function (id) {
    if (!window.state.progress.interactionStateByNodeId[id]) window.state.progress.interactionStateByNodeId[id] = {};
    return window.state.progress.interactionStateByNodeId[id];
};

window.setNodeInteractionState = function (id, patch) {
    const current = window.getNodeInteractionState(id);
    window.state.progress.interactionStateByNodeId[id] = { ...current, ...patch };
    window.saveProgress(true);
};
