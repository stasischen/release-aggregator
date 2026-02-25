/**
 * Lingourmet Mockup TTS Integration
 */
window.ttsSupported = function () {
    return typeof window !== 'undefined' && 'speechSynthesis' in window && typeof SpeechSynthesisUtterance !== 'undefined';
};

window.getKoreanVoices = function () {
    if (!window.ttsSupported()) return [];
    return window.speechSynthesis.getVoices().filter(v => (v.lang || '').toLowerCase().startsWith('ko'));
};

window.pickPreferredKoreanVoice = function (voices) {
    const list = Array.isArray(voices) ? voices : [];
    return list.find(v => /yuna/i.test(v.name || '')) ||
        list.find(v => (v.lang || '').toLowerCase() === 'ko-kr' && v.localService) ||
        list.find(v => (v.lang || '').toLowerCase() === 'ko-kr') ||
        list[0] ||
        null;
};

window.getSelectedKoreanVoice = function () {
    const voices = window.getKoreanVoices();
    const saved = window.state.progress.prefs.ttsVoiceName || '';
    return voices.find(v => v.name === saved) ||
        window.pickPreferredKoreanVoice(voices) ||
        null;
};

window.speakKo = function (text) {
    if (!text || !window.ttsSupported()) return;
    const utter = new SpeechSynthesisUtterance(String(text));
    utter.lang = 'ko-KR';
    const voice = window.getSelectedKoreanVoice();
    if (voice) utter.voice = voice;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utter);
};

window.renderSpeakButton = function (text) {
    if (!text || !window.ttsSupported()) return '';
    return `<button class="btn tiny-text" style="padding:2px 6px; margin-left:6px;" onclick="event.stopPropagation(); window.speakKo('${window.escapeJsSingle(text)}'); return false;" title="播放韓文">▶</button>`;
};

window.renderSpeakInline = function (text) {
    if (!text || !window.ttsSupported()) return '';
    return `<span class="tiny-text" style="display:inline-block; margin-left:6px; padding:1px 5px; border:1px solid var(--line); border-radius:999px; background:#fff;" onclick="event.stopPropagation(); window.speakKo('${window.escapeJsSingle(text)}'); return false;" title="播放韓文">▶</span>`;
};

window.refreshTtsVoices = function () {
    const select = document.getElementById('ttsVoiceSelect');
    const hint = document.getElementById('ttsVoiceHint');
    const testBtn = document.getElementById('ttsTestBtn');

    if (!select) return;
    if (!window.ttsSupported()) {
        select.disabled = true;
        testBtn.disabled = true;
        hint.textContent = '此瀏覽器不支援語音播放 (Web Speech API)。';
        return;
    }
    const voices = window.getKoreanVoices();
    const saved = window.state.progress.prefs.ttsVoiceName || '';
    select.innerHTML = '<option value="">系統預設韓文語音</option>' +
        voices.map(v => `<option value="${window.escapeHtml(v.name)}">${window.escapeHtml(v.name)} (${window.escapeHtml(v.lang)})${v.localService ? ' · local' : ''}</option>`).join('');

    const match = voices.find(v => v.name === saved);
    if (match) {
        select.value = saved;
    } else if (voices.length) {
        const preferred = window.pickPreferredKoreanVoice(voices);
        if (!saved) {
            window.state.progress.prefs.ttsVoiceName = preferred.name;
            window.saveProgress(true);
        }
        select.value = window.state.progress.prefs.ttsVoiceName || preferred.name;
    } else {
        select.value = '';
    }
    hint.textContent = voices.length
        ? `找到 ${voices.length} 個韓文語音，可選你安裝的高品質語音。`
        : '未找到韓文語音，將嘗試用系統預設語音。';
};
