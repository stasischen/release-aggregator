/**
 * Lingourmet Viewer Adapter
 * Normalizes curriculum-source build artifacts for the modular viewer.
 */

window.LessonAdapter = {
    /**
     * Resolves i18n or legacy string fields.
     * Priority: locale > zh_tw > en > first available string
     */
    resolveText(obj, locale = 'zh_tw', fallback = '') {
        if (!obj) return fallback;
        if (typeof obj === 'string') return obj;

        // If it's an i18n object
        if (obj[locale]) return obj[locale];
        if (obj.zh_tw) return obj.zh_tw;
        if (obj.en) return obj.en;

        // Fallback to first non-empty string value
        const first = Object.values(obj).find(v => typeof v === 'string' && v);
        return first || fallback;
    },

    /**
     * Normalizes the unit metadata.
     */
    normalizeUnit(unit, locale = 'zh_tw') {
        if (!unit) return {};

        return {
            ...unit,
            displayTitle: this.resolveText(unit.title_i18n, locale, unit.title_zh_tw || unit.unit_id || ''),
            displayTheme: this.resolveText(unit.theme_i18n, locale, unit.theme_zh_tw || ''),
            displayCanDo: Array.isArray(unit.can_do_i18n)
                ? unit.can_do_i18n.map(v => this.resolveText(v, locale)).filter(Boolean)
                : (unit.can_do_zh_tw || [])
        };
    },

    /**
     * Normalizes a single node.
     */
    normalizeNode(node, locale = 'zh_tw') {
        if (!node) return {};

        const normalized = {
            ...node,
            displayTitle: this.resolveText(node.title_i18n, locale, node.title_zh_tw || this.getFallbackNodeTitle(node)),
            displaySummary: this.resolveText(node.summary_i18n, locale, node.summary_zh_tw || '先看這一節的內容。'),
            displayExpected: this.resolveText(node.expected_output_i18n, locale, node.expected_output_zh_tw || '先理解這一節的重點。'),
            payload: node.payload || {}
        };

        // Ensure content_form is present
        if (!normalized.content_form && normalized.id) {
            // Some legacy nodes might lack content_form but have hints in ID or role
            normalized.content_form = this.inferContentForm(normalized);
        }

        return normalized;
    },

    /**
     * Fallback title logic moved from renderers.js
     */
    getFallbackNodeTitle(node) {
        const id = node.id || '';
        const match = id.match(/-(L1|L2|L3|G1|G2|P1|P2|P5|R1)$/);
        const stage = match ? match[1] : '';

        const role = node.learning_role || '';
        const roleMap = {
            immersion_input: '沉浸輸入',
            structure_pattern: '句型結構',
            structure_grammar: '文法解說',
            explicit_rule: '規則整理',
            controlled_output: '可控輸出',
            immersion_output: '任務輸出',
            review_retrieval: '複習回想'
        };
        const roleName = roleMap[role] || '學習節點';

        return stage ? `${stage} ${roleName}` : roleName;
    },

    /**
     * Infers content form for legacy or incomplete data.
     */
    inferContentForm(node) {
        if (node.content_form) return node.content_form;
        if (node.payload?.dialogue_turns || node.payload?.dialogue_scenes) return 'dialogue';
        if (node.payload?.pattern_builder_demos || node.payload?.pattern_builder_demo) return 'pattern_lab';
        if (node.learning_role === 'structure_grammar') return 'grammar_summary';
        return 'unknown';
    }
};

// Global helper for quick access
window.i18nText = window.LessonAdapter.resolveText;
