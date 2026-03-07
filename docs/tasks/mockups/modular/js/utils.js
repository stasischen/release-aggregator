/**
 * Lingourmet Mockup Utilities
 */
window.escapeHtml = function (str) {
    if (!str) return '';
    return String(str).replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": "&#39;" }[m]));
};

window.escapeJsSingle = function (str) {
    return String(str || '')
        .replace(/\\/g, '\\\\')
        .replace(/'/g, "\\'")
        .replace(/\n/g, '\\n');
};

window.showToast = function (msg) {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const t = document.createElement('div');
    t.className = 'toast';
    t.textContent = msg;
    container.appendChild(t);
    setTimeout(() => {
        t.classList.add('out');
        setTimeout(() => t.remove(), 300);
    }, 2000);
};

window.i18nText = function (obj, locale = 'zh_tw', fallback = '') {
    if (!obj) return fallback;
    if (typeof obj === 'string') return obj;
    if (obj[locale]) return obj[locale];
    if (obj.zh_tw) return obj.zh_tw;
    if (obj.en) return obj.en;
    const first = Object.values(obj).find(v => typeof v === 'string' && v);
    return first || fallback;
};

window.currentTeachingLocale = function () {
    return window.state?.progress?.prefs?.teachingLocale || 'zh_tw';
};
