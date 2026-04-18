/**
 * Lingourmet Stable App V2 - Full Feature Set
 */
const FIXTURES_INDEX = 'data/fixtures.json';

const APP = {
    elements: {},
    async init() {
        console.log("APP V2 FULL INIT");
        const ids = [
            'darkModeToggle', 'backToMapBtn', 'unitIndicator',
            'courseMapGrid', 'libraryGrid', 'lessonView', 'courseMapView', 'libraryView',
            'unitTitle', 'unitSub', 'unitMetaGrid', 'canDoList', 'rolePills',
            'progressText', 'progressFill', 'followupsBox', 'nodeList', 'roleSummaryBox',
            'detailHeader', 'detailSummary', 'detailBody', 'prevBtn', 'nextBtn',
            'markDoneBtn', 'markReviewBtn', 'bilingualToggle', 'libFilterTabsContainer',
            'libSidebar', 'libToc', 'libReader', 'libSearch', 'libMobileNav', 'libCurrentTitle'
        ];
        
        ids.forEach(id => {
            this.elements[id] = document.getElementById(id);
        });
        
        this.elements.mainNavTabs = document.querySelectorAll('#mainNavTabs .nav-tab');
        this.elements.libFilterTabs = document.querySelectorAll('#libraryFilterTabs .nav-tab');
        
        this.currentLibraryFilter = 'all';
        this.libSentences = {};
        this.libKnowledgeRuntime = [];
        this.libDictionaryRuntime = [];
        this.libExampleCache = {};
        this.currentView = 'courseMapView';
        this.wireEvents();
        this.primeAudioEngine(); 
        await this.bootstrap();
        await this.initLibrary();
    },

    wireEvents() {
        // Nav Tabs
        this.elements.mainNavTabs.forEach(btn => {
            btn.onclick = () => this.switchView(btn.dataset.target);
        });

        // Dark Mode
        if (this.elements.darkModeToggle) {
            this.elements.darkModeToggle.onclick = () => {
                document.body.classList.toggle('dark');
                const isDark = document.body.classList.contains('dark');
                localStorage.setItem('lingo_mock_dark_mode', isDark);
                this.elements.darkModeToggle.textContent = isDark ? window.getLabel('light_mode') : window.getLabel('dark_mode');
            };
            if (localStorage.getItem('lingo_mock_dark_mode') === 'true') {
                document.body.classList.add('dark');
                this.elements.darkModeToggle.textContent = window.getLabel('light_mode');
            }
        }

        if (this.elements.backToMapBtn) {
            this.elements.backToMapBtn.onclick = () => this.switchView('courseMapView');
        }

        // Lesson controls
        if (this.elements.prevBtn) this.elements.prevBtn.onclick = () => { if (window.state.currentIndex > 0) { window.state.currentIndex--; window.renderCurrentNode(); } };
        if (this.elements.nextBtn) this.elements.nextBtn.onclick = () => { if (window.state.currentIndex < window.state.data.sequence.length - 1) { window.state.currentIndex++; window.renderCurrentNode(); } };
        if (this.elements.markDoneBtn) this.elements.markDoneBtn.onclick = () => window.toggleDone(window.state.data.sequence[window.state.currentIndex].id);
        if (this.elements.markReviewBtn) this.elements.markReviewBtn.onclick = () => window.toggleReview(window.state.data.sequence[window.state.currentIndex].id);
        
        if (this.elements.bilingualToggle) {
            this.elements.bilingualToggle.onchange = (e) => {
                window.state.progress.prefs.showBilingual = !!e.target.checked;
                window.saveProgress(true);
                window.renderCurrentNode();
            };
        }

        // Library Search
        if (this.elements.libSearch) {
            this.elements.libSearch.oninput = (e) => this.filterLibToc(e.target.value);
        }

        // Global Event Delegation for Audio Buttons (Safari Gesture Preservation)
        document.body.addEventListener('click', (e) => {
            const btn = e.target.closest('.audio-btn');
            if (btn) {
                e.preventDefault();
                e.stopPropagation();
                const text = btn.dataset.text;
                const audio = btn.dataset.audio;
                this.playOriginalOrTTS(text, audio);
            }
        });
    },

    primeAudioEngine() {
        const handler = () => {
            // console.log("[Audio Engine] Priming for Safari/macOS...");

            // 1. Prime TTS
            if (window.speakKo) {
                // Speak a silent space to "unlock" the engine
                const utter = new SpeechSynthesisUtterance(" ");
                utter.volume = 0;
                window.speechSynthesis.speak(utter);
            }

            window.audioEngineIsPrimed = true;
            document.removeEventListener('click', handler);
            document.removeEventListener('touchstart', handler);
        };
        document.addEventListener('click', handler);
        document.addEventListener('touchstart', handler);
    },

    async bootstrap() {
        try {
            // Add cache busting to fixtures fetching
            const fResp = await fetch(`${FIXTURES_INDEX}?v=${Date.now()}`);
            let fixtures = { units: [] };
            if (fResp.ok) fixtures = await fResp.json();
            this.renderCourseMap(fixtures);

            const lastPath = localStorage.getItem('agg_gen_last_unit_path') || (fixtures.units[0]?.path);
            if (lastPath) this.loadUnit(lastPath, false);
        } catch (e) { console.error("Bootstrap error", e); }
        // Preserve the library view if it was already opened by initLibrary().
        if (this.currentView !== 'libraryView') {
            this.switchView('courseMapView');
        }
    },

    async loadUnit(path, autoSwitch = true) {
        try {
            // console.log(`[LOADER] Loading path: ${path}`);
            // Force state clearing to prevent leftovers
            window.state.data = null;
            window.state.currentNode = null;
            window.state.currentIndex = 0;

            const resp = await fetch(path + '?v=' + Date.now());
            if (!resp.ok) throw new Error('Load failed');
            let data = await resp.json();
            
            // 1. Ingest (standardize unit/node structure)
            data = window.LessonAdapter.ingest(data, window.currentLocale());

            // 2. Enrich (async assets merger)
            data = await window.LessonAdapter.enrich(data, window.currentLocale());

            window.state.data = data;
            window.state.currentIndex = 0;
            localStorage.setItem('agg_gen_last_unit_path', path);

            window.loadProgress();
            window.renderSidebar();
            window.renderCurrentNode();
            
            if (autoSwitch) this.switchView('lessonView');
            if (window.showToast) window.showToast(`${window.getLabel('unit_loaded')}${window.state.data.unit?.unit_id || window.getLabel('real_content')}`);
        } catch (e) { 
            console.error("LoadUnit Error:", e);
            if (window.showToast) window.showToast(window.getLabel('load_failed') + e.message, "error");
        }
    },


    selectSegment(id) {
        // console.log(`Segment selected: ${id}`);
        window.state.activeSegmentId = id;
        document.querySelectorAll('.subtitle-row, .dialogue-turn').forEach(el => el.classList.toggle('active', el.dataset.segmentId === id));
        // Deep integration: when a segment is selected, the first atom could be pre-selected?
    },

    selectAtom(id, event) {
        if (event) event.stopPropagation();
        // console.log(`Atom selected: ${id}`);
        // Highlight in UI
        document.querySelectorAll('.atom-seg').forEach(el => el.classList.toggle('active', el.dataset.atomId === id));
        
        // Find atom data in current state
        let atomData = this.getAtomData(id);
        
        // Fallback: If not in formal atoms (Fail-soft), try heuristic dictionary lookup
        if (!atomData && id.startsWith('fs-')) {
            const el = document.querySelector(`.atom-seg[data-atom-id="${id}"]`);
            const text = el ? el.dataset.text : null;
            if (text) {
                atomData = this.getAtomDataByText(text);
            }
        }

        if (atomData) {
            window.renderSupportDetail(atomData);
        }
    },

    getAtomData(id) {
        // Look into the currently normalized node state
        const segments = window.state.currentNode?.payload?.normalized_segments?.segments || [];
        
        for (const seg of segments) {
            if (seg.atoms) {
                // Check both fully qualified ID and text-pos composite ID
                const found = seg.atoms.find(a => a.id === id || (a.text + '-' + a.pos) === id);
                if (found) return found;
            }
        }
        return null;
    },

    getAtomDataByText(text) {
        if (!text) return null;
        // Search in the runtime library for a matching surface
        const entry = this.libKnowledgeRuntime.find(it => 
            (it.source?.surface || it.id || '').includes(text)
        );
        
        if (entry) {
            return {
                id: entry.id,
                text: text,
                lemma: entry.source?.surface || text,
                pos: entry.source?.kind || 'unknown',
                definition: entry.i18n?.summary || entry.i18n?.title || ''
            };
        }
        return { text: text, is_unknown: true };
    },

    renderKoreanSegmentation(seg) {
        const raw = seg.ko || seg.surface || '';
        if (!raw) return '';

        // Case 1: Alignment known to have failed or no atoms provided
        if (seg.alignment_failed || !seg.atoms || seg.atoms.length === 0) {
            if (seg.alignment_failed) {
                return `<span class="alignment-warning" title="資料對齊異常：單字分割已停用">${window.escapeHtml(raw)} <i class="fas fa-info-circle" style="font-size:0.7em;"></i></span>`;
            }
            
            // Standard space-based fail-soft (if no atoms exist)
            return raw.split(/(\s+)/).map((part, idx) => {
                if (/\s+/.test(part)) return part; // Preserve spaces
                const cleanText = part.replace(/[.,?!~]/g, '');
                if (!cleanText) return window.escapeHtml(part);
                return `<span class="atom-seg fail-soft" data-text="${window.escapeHtml(cleanText)}" data-atom-id="fs-${idx}">${window.escapeHtml(part)}</span>`;
            }).join('');
        }

        // Case 2: We have atoms. We must interleave them into the raw text to preserve punctuation/spaces.
        // We use a simple greedy matching for the pilot to ensure stability.
        let resultHtml = '';
        let remainingRaw = raw;
        
        // Sort atoms by their appearance in the raw text if possible, though they are usually ordered
        seg.atoms.forEach((a, idx) => {
            const atomText = a.text;
            if (!atomText) return;

            const pos = remainingRaw.indexOf(atomText);
            if (pos !== -1) {
                // Add skipped text (punctuation, spaces) as plain text
                resultHtml += window.escapeHtml(remainingRaw.substring(0, pos));
                
                // Add the atom as a span
                const cleanId = a.id || `${a.text}-${a.pos}-${idx}`;
                resultHtml += `<span class="atom-seg" data-atom-id="${cleanId}">${window.escapeHtml(atomText)}</span>`;
                
                // Move forward
                remainingRaw = remainingRaw.substring(pos + atomText.length);
            }
        });

        // Add any trailing punctuation
        resultHtml += window.escapeHtml(remainingRaw);
        return resultHtml;
    },


    switchView(viewId) {
        this.currentView = viewId;
        document.querySelectorAll('.view-container, .page').forEach(el => el.classList.remove('active'));
        const target = document.getElementById(viewId);
        if (target) target.classList.add('active');

        this.elements.mainNavTabs.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.target === viewId);
        });

        if (this.elements.unitIndicator) {
            if (viewId === 'lessonView' && window.state.data) {
                this.elements.unitIndicator.style.display = 'block';
                this.elements.unitIndicator.textContent = `${window.getLabel('navigating_unit')}${window.state.data.unit.unit_id}`;
            } else {
                this.elements.unitIndicator.style.display = 'none';
            }
        }
    },

    renderCourseMap(fixtures) {
        if (!this.elements.courseMapGrid) return;
        const units = fixtures.units || [];
        if (units.length === 0) {
            this.elements.courseMapGrid.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1; margin-top:80px;">
                    <div class="icon" style="font-size:48px;">🧹</div>
                    <h3>${window.getLabel('no_units')}</h3>
                    <p class="muted-text">${window.getLabel('no_units_desc')}</p>
                </div>
            `;
            return;
        }

        this.elements.courseMapGrid.innerHTML = units.map(u => {
            const progress = Math.floor(Math.random() * 60) + 20;
            return `
                <div class="unit-card" onclick="APP.loadUnit('${u.path}')">
                    <div class="unit-badge">Chapter ${u.id.split('-').pop()}</div>
                    <h3>${window.escapeHtml(u.title)}</h3>
                    <div class="unit-stats"><span>${u.id}</span> · <span>${u.level || 'A1'}</span></div>
                    <div class="progress-pill">
                        <div class="progress-fill" style="width: ${progress}%"></div>
                    </div>
                    <div class="tiny-text muted" style="margin-top:8px">${progress}% Complete</div>
                </div>
            `;
        }).join('');
    },

    // --- Knowledge Book (Grammar/Pattern Book) Logic ---

    async initLibrary() {
        try {
            const [manifestResp, knowledgeResp, sentenceResp, dictionaryResp] = await Promise.all([
                fetch(`data/library_manifest.json?v=${Date.now()}`),
                fetch(`data/runtime/zh_tw/knowledge.json?v=${Date.now()}`),
                fetch(`data/runtime/zh_tw/example_sentence.json?v=${Date.now()}`),
                fetch(`data/runtime/zh_tw/dictionary.json?v=${Date.now()}`)
            ]);
            
            if (manifestResp.ok) this.libManifest = await manifestResp.json();
            if (knowledgeResp.ok) this.libKnowledgeRuntime = await knowledgeResp.json();
            if (dictionaryResp.ok) this.libDictionaryRuntime = await dictionaryResp.json();
            
            if (sentenceResp.ok) {
                const runtimeSentences = await sentenceResp.json();
                this.libSentences = runtimeSentences.reduce((acc, item) => {
                    if (item && item.id) acc[item.id] = item;
                    return acc;
                }, {});
            }

            console.log(`[Library] Loaded ${this.libKnowledgeRuntime.length} knowledge items and ${this.libDictionaryRuntime.length} dictionary items.`);
            this.renderLibToc();
            this.renderLibFeatured();
        } catch (e) { 
            console.error("Library init error", e); 
        }
    },

    renderLibToc() {
        if (!this.elements.libToc || !this.libManifest) return;
        
        let html = '';
        this.libManifest.categories.forEach(cat => {
            html += `
                <div class="toc-category">
                    <div class="toc-category-title">${cat.title}</div>
                    ${(cat.sub || []).map(sub => `
                        <div class="toc-item" onclick="APP.selectLibCategory('${cat.id}', '${sub.id}')">
                            ${sub.title}
                        </div>
                    `).join('')}
                </div>
            `;
        });
        
        this.elements.libToc.innerHTML = html;
    },

    filterLibToc(query) {
        const q = query.toLowerCase();
        const items = document.querySelectorAll('.toc-item');
        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(q) ? 'block' : 'none';
        });
    },

    getCategoryTitle(cid) {
        const mapping = {
            "grammar": window.getLabel('grammar'),
            "pattern": window.getLabel('pattern'),
            "connector": window.getLabel('connector'),
            "expression": window.getLabel('expression'),
            "vocab": window.getLabel('vocab')
        };
        return mapping[cid] || cid.capitalize();
    },

    async selectLibCategory(catId, subId) {
        if (!this.libManifest) return;
        
        const sidLower = (subId || '').toLowerCase();
        const items = (this.libManifest.items || []).filter(item => 
            item.category === catId && (item.sub || '').toLowerCase() === sidLower
        );
        
        if (items.length === 0) {
            this.elements.libReader.innerHTML = `
                <div class="empty-state">
                    <h3>${subId} ${window.getLabel('content_preparing')}</h3>
                    <p>${window.getLabel('content_preparing_desc')}</p>
                </div>
            `;
            if (this.elements.libCurrentTitle) this.elements.libCurrentTitle.textContent = subId;
            this.toggleLibSidebar(false);
            return;
        }

        const listHtml = items.map(f => `
            <div class="unit-card" style="text-align:left; cursor:pointer; margin-bottom:12px; display:flex; align-items:center; gap:12px;" onclick="APP.loadLibRule('${f.runtime_id || f.id}')">
                <div class="level-badge ${f.level.toLowerCase()}">${f.level}</div>
                <div style="flex:1">
                    <h4 style="margin:0">${window.escapeHtml(f.title)}</h4>
                    <p class="tiny-text muted" style="margin:2px 0 0 0">${f.surface || ''}</p>
                </div>
                <div class="icon">→</div>
            </div>
        `).join('');

        // UI Optimization: Merge Breadcrumb and Category Title
        const catTitle = this.getCategoryTitle(catId);
        const isSame = catId.toLowerCase() === subId.toLowerCase() || subId.toLowerCase() === 'general';
        const displaySub = subId.charAt(0).toUpperCase() + subId.slice(1);

        this.elements.libReader.innerHTML = `
            <div class="animate-in" style="padding:20px 0;">
                <div class="lib-category-header" style="margin-bottom:32px; display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        ${isSame ? '' : `<div class="breadcrumb" style="font-size:12px; font-weight:700; color:var(--muted); margin-bottom:4px; text-transform:uppercase;">${catTitle}</div>`}
                        <h2 style="margin:0; font-size:24px;">${displaySub}</h2>
                        <div style="height:2px; width:40px; background:var(--accent); margin-top:12px;"></div>
                    </div>
                    <div style="display:flex; gap:8px;">
                        <button class="btn tiny-text" onclick="window.resetAudioEngine()" style="padding:4px 8px; border-radius:8px; opacity:0.8; color:var(--warn); border-color:var(--warn-soft);">${window.getLabel('reset_audio')}</button>
                        <button class="btn tiny-text" onclick="APP.showLibTOC()" style="padding:4px 8px; border-radius:8px; opacity:0.8;">${window.getLabel('all_topics')}</button>
                    </div>
                </div>
                <div class="list-grid">
                    ${listHtml}
                </div>
            </div>
        `;
        
        if (this.elements.libCurrentTitle) this.elements.libCurrentTitle.textContent = displaySub;
        this.toggleLibSidebar(false);
    },

    async loadLibRule(runtimeId) {
        try {
            const runtimeItem = this.libKnowledgeRuntime.find(item => item.id === runtimeId);
            if (!runtimeItem) throw new Error(`Rule load failed: unknown runtime id ${runtimeId}`);
            const meta = (this.libManifest.items || []).find(it => it.runtime_id === runtimeId || it.id === runtimeId) || {};
            const source = runtimeItem.source || {};
            const i18n = runtimeItem.i18n || {};
            const refs = meta.example_sentence_refs || source.example_sentence_refs || [];
            const exampleBank = refs.map(sid => {
                const sentence = this.libSentences[sid];
                if (!sentence) return null;
                return {
                    id: sid,
                    ko: sentence.source?.ko || sentence.source?.surface_ko || '',
                    translation: sentence.i18n?.translation || ''
                };
            }).filter(Boolean);

            const data = {
                id: runtimeItem.id,
                source,
                i18n,
                title_i18n: { zh_tw: i18n.title || runtimeItem.id },
                summary_i18n: { zh_tw: i18n.description || '' },
                explanation_md_i18n: { zh_tw: i18n.explanation_md || '' },
                usage_notes_i18n: { zh_tw: i18n.usage_notes || [] },
                example_sentence_refs: refs,
                resolved_examples: exampleBank
            };

            this.renderLibReader(data, meta);
            
            // UI Optimization: Mobile Nav shows breadcrumb context, Card shows Title
            const catTitle = this.getCategoryTitle(meta.category);
            if (this.elements.libCurrentTitle) {
                this.elements.libCurrentTitle.textContent = `${catTitle} > ${meta.sub}`;
            }
            
            this.toggleLibSidebar(false);
            if (this.elements.libReader) this.elements.libReader.scrollTop = 0;
        } catch (e) { console.error(e); }
    },

    renderLibReader(data, meta = {}) {
        if (!this.elements.libReader) return;
        
        const examplesHtml = (data.resolved_examples || []).map((ex, idx) => {
            const fallbackKo = window.escapeJsSingle(ex.ko);
            return `
                <div class="example-card animate-in">
                    <div class="example-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <div class="example-ko" style="font-weight:700; color:var(--text);">${window.escapeHtml(ex.ko)}</div>
                        <button type="button" class="audio-btn" onclick="event.stopPropagation(); APP.playOriginalOrTTS('${fallbackKo}'); return false;" title="${window.getLabel('play_tts')}">
                            <span class="icon">🔊</span>
                        </button>
                    </div>
                    <div class="example-zh" style="color:var(--muted); font-size:14px;">${window.escapeHtml(ex.translation || '')}</div>
                </div>
            `;
        }).join('');

        const levelClass = (meta.level || 'A1').toLowerCase();
        const explanationHtml = window.markdownToHtmlLite(window.i18nText(data.explanation_md_i18n, window.currentLocale(), ''));
        const hasExamples = (data.resolved_examples || []).length > 0;

        this.elements.libReader.innerHTML = `
            <article class="animate-in" style="padding-bottom: 60px;">
                <header class="rule-header" style="margin-bottom:32px;">
                    <div class="meta-strip" style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                        <span class="level-badge ${levelClass}">${meta.level || 'A1'}</span>
                        <span class="tiny-text muted" style="letter-spacing:0.05em;">${data.id || ''}</span>
                    </div>
                    <h2 style="margin:0; font-size:32px; color:var(--text); margin:0 0 16px 0; line-height:1.2;">${window.escapeHtml(window.i18nText(data.title_i18n, window.currentLocale(), data.id || ''))}</h2>
                    <div style="height:4px; width:60px; background:var(--accent); border-radius:2px; margin-bottom:24px;"></div>
                    <p class="lead" style="font-size:18px; font-weight:500; color:var(--muted); line-height:1.6; margin:0;">${window.escapeHtml(window.i18nText(data.summary_i18n, window.currentLocale(), ''))}</p>
                </header>

                <section class="content-block" style="margin-top:0; padding:22px; border:1px solid var(--line); border-radius:20px; background:var(--card);">
                    <div class="rule-body">
                        ${explanationHtml || `<p class="md-paragraph muted">${window.getLabel('no_rule_content')}</p>`}
                    </div>
                </section>

                ${(window.i18nText(data.usage_notes_i18n, window.currentLocale(), []) || []).length > 0 ? `
                    <h2 style="margin-top:48px;">${window.getLabel('usage_tips')}</h2>
                    <div class="usage-tips" style="margin-bottom:32px; display:flex; flex-wrap:wrap; gap:8px;">
                        ${(window.i18nText(data.usage_notes_i18n, window.currentLocale(), []) || []).map(note => `<div class="tag">${window.escapeHtml(note)}</div>`).join('')}
                    </div>
                ` : ''}

                <div class="example-section" style="margin-top:28px;">
                    <div class="section-subtitle">${window.getLabel('examples')}</div>
                    ${hasExamples ? `<div class="example-grid" style="display:grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap:16px;">${examplesHtml}</div>` : `<p class="muted-text">${window.getLabel('no_examples')}</p>`}
                </div>
            </article>
        `;
    },

    playOriginalOrTTS(text) {
        if (!text) return;
        // console.log("TTS-only test mode: speaking via Web Speech API.");
        if (window.speakKo) window.speakKo(text);
    },

    showLibTOC() {
        this.elements.libReader.innerHTML = `
            <div class="empty-state" style="margin-top:100px;">
                <div class="icon" style="font-size:48px;">📖</div>
                <h3>${window.getLabel('lib_welcome')}</h3>
                <p class="muted-text">${window.getLabel('lib_sidebar_prompt')}</p>
                <div class="featured-list" id="libFeaturedList" style="margin-top:32px;"></div>
            </div>
        `;
        this.renderLibFeatured();
        if (this.elements.libCurrentTitle) this.elements.libCurrentTitle.textContent = window.getLabel('lib_select_topic');
    },

    toggleLibSidebar(open) {
        if (this.elements.libSidebar) {
            this.elements.libSidebar.classList.toggle('open', open);
        }
    },

    renderLibFeatured() {
        const featured = this.libManifest.featured || [];
        const el = document.getElementById('libFeaturedList');
        if (!el) return;
        
        el.innerHTML = featured.map(f => `
            <div class="unit-card" style="text-align:left; cursor:pointer;" onclick="APP.loadLibRule('${f.runtime_id || f.id}')">
                <div class="unit-badge">${f.category}</div>
                <h4>${window.escapeHtml(f.title)}</h4>
                <p class="tiny-text muted">${window.getLabel('lib_featured_desc')}</p>
            </div>
        `).join('');
    },

    getFormColor(form) {
        if (form.includes('grammar') || form === 'pattern_card') return 'var(--accent3)';
        if (form.includes('vocab') || form === 'functional_phrase_pack') return 'var(--accent2)';
        return 'var(--accent)';
    },

    jumpToNode(nodeId) {
        const idx = window.state.data.sequence.findIndex(n => n.id === nodeId);
        if (idx !== -1) window.setIndex(idx);
    },

    toggleGrammarDetail(idx, knowledgeId) {
        const el = document.getElementById(`grammar_${idx}`);
        if (el) {
            const isHidden = el.style.display === 'none';
            el.style.display = isHidden ? 'block' : 'none';
            // Optional: log if needed
            // console.log(`Toggled grammar detail for item ${idx}, target: ${knowledgeId}`);
        }
    }
};

// --- View Rendering Shims (Legacy Alignment) ---

window.renderSidebar = function() {
    const unitRaw = window.state.data.unit;
    const unit = window.LessonAdapter.normalizeUnit(unitRaw, 'zh_tw');
    
    if (APP.elements.unitTitle) APP.elements.unitTitle.textContent = unit.displayTitle;
    if (APP.elements.unitSub) APP.elements.unitSub.textContent = `${unit.unit_id} · ${unit.level}`;
    
    if (APP.elements.unitMetaGrid) {
        APP.elements.unitMetaGrid.innerHTML = `
            <div class="meta-box"><span class="k">${window.getLabel('theme')}</span><span class="v">${unit.displayTheme}</span></div>
            <div class="meta-box"><span class="k">${window.getLabel('type')}</span><span class="v">${window.getLabel('unit_course')}</span></div>
        `;
    }
    
    if (APP.elements.canDoList) {
        APP.elements.canDoList.innerHTML = unit.displayCanDo.map(x => `<li>${window.escapeHtml(x)}</li>`).join('');
    }
    
    window.renderProgress();
    window.renderRoleSummary();
};

window.renderNodeList = function() {
    if (!APP.elements.nodeList) return;
    APP.elements.nodeList.innerHTML = window.state.data.sequence.map((n, i) => {
        const isDone = window.isDone(n.id);
        const isReview = window.isReview(n.id);
        const active = i === window.state.currentIndex;
        
        let classes = ['node-card'];
        if (active) classes.push('active');
        if (isDone) classes.push('done');
        if (isReview) classes.push('review-mark');

        return `
            <div class="${classes.join(' ')}" onclick="window.setIndex(${i})">
                <span class="num">${i + 1}</span>
                <span class="txt">
                    ${window.escapeHtml(window.nodeTitleText(n, 'zh_tw') || n.id)}
                    ${isDone ? '<span class="status-icon">✓</span>' : ''}
                    ${isReview ? '<span class="status-icon">★</span>' : ''}
                </span>
            </div>
        `;
    }).join('');
};

window.renderFooterButtons = function() {
    const node = window.state.data.sequence[window.state.currentIndex];
    if (!node) return;
    
    const isDone = window.isDone(node.id);
    const isReview = window.isReview(node.id);

    if (APP.elements.markDoneBtn) {
        if (isDone) {
            APP.elements.markDoneBtn.classList.add('success');
            APP.elements.markDoneBtn.textContent = '✓ 已完成';
        } else {
            APP.elements.markDoneBtn.classList.remove('success');
            APP.elements.markDoneBtn.textContent = '完成';
        }
    }

    if (APP.elements.markReviewBtn) {
        if (isReview) {
            APP.elements.markReviewBtn.classList.add('warn'); // style.css uses .warn for yellowish/important
            APP.elements.markReviewBtn.textContent = '★ 待回看';
            APP.elements.markReviewBtn.style.borderColor = 'var(--warn)';
        } else {
            APP.elements.markReviewBtn.classList.remove('warn');
            APP.elements.markReviewBtn.textContent = '待回看';
            APP.elements.markReviewBtn.style.borderColor = '';
        }
    }
};

window.renderProgress = function() {
    const total = window.state.data.sequence.length;
    const done = window.state.progress.completedNodeIds.length;
    if (APP.elements.progressText) APP.elements.progressText.textContent = `${done}/${total}`;
    if (APP.elements.progressFill) APP.elements.progressFill.style.width = `${(done/total)*100}%`;
};

window.renderRoleSummary = function() {
    // Basic summary for now
    if (!APP.elements.roleSummaryBox) return;
    const counts = {};
    window.state.data.sequence.forEach(n => counts[n.learning_role] = (counts[n.learning_role] || 0) + 1);
    APP.elements.roleSummaryBox.innerHTML = `<h3>${window.getLabel('content_dist')}</h3>` + Object.entries(counts).map(([k, v]) => `
        <div class="tiny-text" style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span class="muted">${k}</span>
            <span class="accent" style="font-weight:700">${v}</span>
        </div>
    `).join('');
};

window.renderCurrentNode = function() {
    const node = window.state.data.sequence[window.state.currentIndex];
    const normalized = window.LessonAdapter.normalizeNode(node, 'zh_tw');
    window.state.currentNode = normalized;
    
    window.renderNodeList();
    window.renderProgress();
    window.renderFooterButtons();

    if (window.renderDetailHeader) window.renderDetailHeader(normalized);
    if (window.renderDetailSummary) window.renderDetailSummary(normalized);

    const { contentHtml, interactionHtml } = window.RendererRegistry.dispatch(normalized);
    if (APP.elements.detailBody) {
        APP.elements.detailBody.innerHTML = contentHtml;
        const area = document.getElementById('interactionArea');
        if (area && interactionHtml) {
            area.innerHTML = interactionHtml;
        } else if (interactionHtml) {
            APP.elements.detailBody.innerHTML += interactionHtml;
        }
    }
    
    if (APP.elements.prevBtn) APP.elements.prevBtn.disabled = window.state.currentIndex === 0;
    if (APP.elements.nextBtn) APP.elements.nextBtn.disabled = window.state.currentIndex === window.state.data.sequence.length - 1;
};

window.setIndex = function(i) {
    window.state.currentIndex = i;
    window.renderCurrentNode();
};

document.addEventListener('DOMContentLoaded', () => APP.init());
window.APP = APP;

/**
 * Support Detail Renderer (Slice D)
 * Renders linguistic analysis for a selected atom.
 */
window.renderSupportDetail = function(atom) {
    const container = document.getElementById('supportDetail');
    if (!container) return;

    if (!atom) {
        container.classList.remove('active');
        return;
    }

    // 1. Decompose composite IDs and lookup parts
    const idParts = (atom.id || '').split('+');
    const results = [];
    
    idParts.forEach(part => {
        // Strip legacy prefixes and extract tag
        // e.g. "ko:pron:저" -> tag: "pron", cleanPart: "저"
        const tagMatch = part.match(/^ko:([a-z]+):/i);
        const tag = tagMatch ? tagMatch[1].toLowerCase() : null;
        const cleanPart = part.replace(/^ko:[a-z]+:/i, '').replace(/[.,?!~]/g, '');
        const surfaceText = atom.text?.includes(cleanPart) ? cleanPart : (atom.text || cleanPart);
        
        // POS Mapping: Legacy Tag -> Knowledge Lab Category/Tag
        const posMap = {
            'p': ['particle', 'postposition'],
            'pron': ['pronoun', 'noun'],
            'n': ['noun', 'vocabulary'],
            'v': ['verb', 'ending'],
            'adj': ['adjective', 'ending'],
            'adv': ['adverb'],
            'det': ['determiner', 'adnominal'],
            'e': ['ending', 'suffix'],
            'count': ['count', 'unit'],
            'vx': ['ending', 'aux_verb', 'verb']
        };

        // 1. Parallel Lookup: Dictionary (Vocab) and Knowledge (Grammar)
        const dictEntry = APP.libDictionaryRuntime.find(it => {
            const source = it.source || {};
            const i18n = it.i18n || {};
            
            // Strict Tag Check with Verb Flexibility
            if (tag) {
                const dictPos = (source.pos || i18n.pos || '').toLowerCase();
                const isVerbClass = (tag === 'v' || tag === 'vx' || tag === 'adj');
                const dictIsVerbClass = (dictPos === 'v' || dictPos === 'vx' || dictPos === 'adj');
                
                if (isVerbClass && dictIsVerbClass) {
                    // Allow cross-linking between V and VX in dictionary
                } else if (dictPos !== tag) {
                    return false;
                }
            }

            const surfaceMatch = (source.lemma_id === cleanPart || 
                                 source.surface === cleanPart || 
                                 i18n.headword === cleanPart || 
                                 (source.surface_forms || []).includes(cleanPart));
            if (surfaceMatch) return true;
            
            // Also check if the atom_id ends with the cleanPart
            const atomId = source.atom_id || it.id || '';
            return atomId.endsWith(':' + cleanPart);
        });

        const knowledgeEntry = APP.libKnowledgeRuntime.find(it => {
            const surface = it.source?.surface || '';
            const title = it.i18n?.title || '';
            const subcategory = (it.source?.subcategory || '').toLowerCase();
            const itemTags = (it.source?.tags || []).map(t => t.toLowerCase());
            
            const textMatched = (surface === cleanPart || surface.split('/').includes(cleanPart) || title === cleanPart);
            if (!textMatched) return false;

            if (tag && posMap[tag]) {
                const isCompatible = posMap[tag].some(cat => subcategory === cat || itemTags.includes(cat));
                if (tag === 'pron' && subcategory === 'determiner') return false;
                if (!isCompatible) return false;
            }
            return true;
        });

        if (dictEntry) {
            const defs = dictEntry.i18n?.definitions || [];
            let summary = defs.map(d => `${d.gloss}${d.usage_notes ? ' (' + d.usage_notes + ')' : ''}`).join('\n');
            
            // Content Quality Check: If the 'Chinese' gloss still contains Hangul, treat as untranslated
            const hasHangul = /[가-힣]/.test(summary);
            if (hasHangul) {
                // Case 1: Entry exists but translation is missing (Korean placeholder)
                summary = `<span class="muted-text">(尚無詳細釋義) - 內容建置中</span>`;
            }

            results.push({
                title: dictEntry.i18n?.headword || dictEntry.source?.headword || cleanPart,
                definition: summary || window.getLabel('no_definition'),
                id: dictEntry.id,
                type: 'dictionary',
                // Link knowledge entry if it exists for the same part
                linkedKnowledge: knowledgeEntry ? {
                    id: knowledgeEntry.id,
                    title: window.i18nText(knowledgeEntry.i18n?.title_i18n, window.currentLocale(), knowledgeEntry.i18n?.title),
                    summary: knowledgeEntry.i18n?.summary || knowledgeEntry.i18n?.description || ''
                } : null
            });
        } else if (knowledgeEntry) {
            // Only if No dictionary match, show knowledge directly
            results.push({
                title: window.i18nText(knowledgeEntry.i18n?.title_i18n, window.currentLocale(), knowledgeEntry.i18n?.title),
                definition: knowledgeEntry.i18n?.summary || knowledgeEntry.i18n?.description || '',
                id: knowledgeEntry.id,
                type: 'knowledge'
            });
        } else {
            // Case 2: Entry is missing from the dictionary entirely
            results.push({
                title: cleanPart,
                definition: `<span class="muted-text">(詞條尚未建立) - 內容建置中</span>`,
                id: 'unknown:' + cleanPart,
                type: 'unknown'
            });
        }
    });

    const bodyHtml = results.map((res, idx) => `
        <div class="support-item animate-in" id="supportItem_${idx}" style="margin-bottom:20px; border-bottom:1px solid var(--line); padding-bottom:15px;">
            <div class="support-header">
                <div>
                    <div class="support-title">${window.escapeHtml(res.title)}</div>
                    ${res.type !== 'unknown' ? `<div class="support-meta">${window.escapeHtml(res.id)}</div>` : ''}
                </div>
            </div>
            <div class="support-definition" id="def_${idx}">
                ${window.escapeHtml(res.definition).replace(/\n/g, '<br>')}
            </div>
            ${res.linkedKnowledge ? `
                <div class="support-detail-action" style="margin-top:10px;">
                    <button class="btn tiny-text secondary" style="background:var(--accent3-soft); color:var(--accent3); border:1px solid var(--accent3);"
                        onclick="APP.toggleGrammarDetail(${idx}, '${window.escapeJsSingle(res.linkedKnowledge.id)}')">
                        <i class="fas fa-book-open"></i> 詳解: ${window.escapeHtml(res.linkedKnowledge.title)}
                    </button>
                    <div id="grammar_${idx}" class="grammar-detail-box" style="display:none; margin-top:10px; padding:12px; background:var(--bg2); border-left:3px solid var(--accent3); border-radius:4px; font-size:0.9em;">
                        <strong>文法解析：</strong><br>
                        ${window.escapeHtml(res.linkedKnowledge.summary)}
                        <div style="margin-top:8px; text-align:right;">
                            <a href="#" class="tiny-text" style="color:var(--accent3);" onclick="APP.loadLibRule('${res.linkedKnowledge.id}'); return false;">查看完整文法卡片 →</a>
                        </div>
                    </div>
                </div>
            ` : ''}
        </div>
    `).join('');

    container.innerHTML = `
        <button class="close-support" onclick="document.getElementById('supportDetail').classList.remove('active')">✕</button>
        <div class="support-content" style="padding-top:20px;">
            ${bodyHtml}
        </div>
        <div style="margin-top: 20px; display: flex; gap: 10px;">
            <button class="btn tiny-text audio-btn" style="flex:1" data-text="${window.escapeJsSingle(atom.text)}">🔊 ${window.getLabel('play')}</button>
            <button class="btn tiny-text" style="flex:1" onclick="window.showToast(window.getLabel('added_to_vocab'))">⭐ ${window.getLabel('save')}</button>
        </div>
    `;
    container.classList.add('active');
};

// Global Event Delegation for Atom Selection (LLLO Style)
document.addEventListener('click', (e) => {
    const atomEl = e.target.closest('.atom-seg');
    if (atomEl && window.APP) {
        e.stopPropagation();
        const id = atomEl.dataset.atomId;
        window.APP.selectAtom(id);
    }
});
