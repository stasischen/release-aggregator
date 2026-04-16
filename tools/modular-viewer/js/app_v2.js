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
                this.elements.darkModeToggle.textContent = isDark ? '☀️ 淺色' : '🌓 深色';
            };
            if (localStorage.getItem('lingo_mock_dark_mode') === 'true') {
                document.body.classList.add('dark');
                this.elements.darkModeToggle.textContent = '☀️ 淺色';
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
            console.log("[Audio Engine] Priming for Safari/macOS...");

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
            console.log(`[LOADER] Loading path: ${path}`);
            // Force state clearing to prevent leftovers
            window.state.data = null;
            window.state.currentNode = null;
            window.state.currentIndex = 0;

            const resp = await fetch(path + '?v=' + Date.now());
            if (!resp.ok) throw new Error('Load failed');
            let data = await resp.json();
            
            // Auto-Wrap raw V5 content from content-ko/core into a valid unit structure
            if (data.nodes && !data.sequence) {
                console.log("Wrapping raw V5 content for rendering...");
                data = {
                    unit: { 
                        unit_id: data.id || 'REAL-DATA', 
                        title_i18n: { zh_tw: (data.id && data.id.includes('vlog')) ? '實體影片測試' : '實體對話測試' },
                        level: 'A1',
                        theme_i18n: { zh_tw: '生產環境資料鏈路' }
                    },
                    sequence: [
                        {
                            id: data.id || 'node-0',
                            title_i18n: { zh_tw: '內容預覽 (Real Content)' },
                            summary_i18n: { zh_tw: '正在直接從 content-ko 加載實體 JSON 檔案。' },
                            content_form: (data.content_form) || (data.nodes?.Start?.turns ? 'video' : 'dialogue'),
                            payload: data
                        }
                    ]
                };
            }

            window.state.data = data;
            window.state.currentIndex = 0;
            localStorage.setItem('agg_gen_last_unit_path', path);

            // Enrichment Step (Atoms) - Pass unit ID explicitly if available
            const unitId = data.unit?.unit_id || data.id;
            await this.enrichAtoms(window.state.data, unitId);

            window.loadProgress();
            window.renderSidebar();
            window.renderCurrentNode();
            this.renderLibraryBook();
            if (autoSwitch) this.switchView('lessonView');
            if (window.showToast) window.showToast(`已載入: ${window.state.data.unit?.unit_id || '實體內容'}`);
        } catch (e) { 
            console.error("LoadUnit Error:", e);
            if (window.showToast) window.showToast("載入失敗: " + e.message, "error");
        }
    },

    async enrichAtoms(data, providedId) {
        if (!data) return;
        
        // FIND THE REAL CONTENT ID (e.g. BWINkN8QbkU or goPwS4aL4Lk)
        const rawPayload = data.sequence?.[0]?.payload || data;
        const cid = rawPayload.id || data.id || data.unit?.unit_id || providedId;
        
        if (!cid || cid === 'REAL-DATA') { 
            console.warn('enrichAtoms: no valid content ID found, skips.'); 
            return; 
        }
        
        console.log(`[ENRICH] Loading assets for Content ID: ${cid}`);

        try {
            let atomsData = null;
            let i18nData = null;
            const locale = window.state.progress.prefs.locale || 'zh_tw';
            const isVideo = rawPayload.nodes?.Start?.turns || rawPayload.turns;
            const isDialogueLesson = rawPayload.dialogue_scenes || rawPayload.dialogue_turns || rawPayload.content;

            // 1. Load Assets with explicit cid
            if (isVideo) {
                const i18nPath = `data/real_content/i18n/${locale}/video/${cid}.json`;
                const iResp = await fetch(`${i18nPath}?v=${Date.now()}`);
                if (iResp.ok) i18nData = await iResp.json();

                // Atom discovery: try _atoms.json pattern first as confirmed in list_dir
                const atomPaths = [`data/real_content/atoms/${cid}_atoms.json`, `data/real_content/atoms/${cid}.json` ];
                for (const p of atomPaths) {
                    const r = await fetch(`${p}?v=${Date.now()}`);
                    if (r.ok) { atomsData = await r.json(); break; }
                }
            } else if (isDialogueLesson) {
                // Dialogue
                const i18nPath = `data/real_content/i18n/${locale}/dialogue/${cid}.json`;
                const iResp = await fetch(`${i18nPath}?v=${Date.now()}`);
                if (iResp.ok) i18nData = await iResp.json();
                
                const aResp = await fetch(`data/real_content/atoms/dialogue_atoms.json?v=${Date.now()}`);
                if (aResp.ok) atomsData = await aResp.json();
            }
            console.log(`[ENRICH] Assets Loaded? Atoms: ${!!atomsData}, I18N: ${!!i18nData}`);

            // 2. Apply enrichment – handle auto-wrapped structure
            const sequence = data.sequence?.length ? data.sequence : [{ payload: rawPayload }];
            
            sequence.forEach(node => {
                // IMPORTANT: The actual content lives in node.payload for wrapped units
                const payload = node.payload || data;
                
                // Collect all possible turn sources
                const turnSources = [
                    payload.dialogue_turns,
                    payload.content,
                    payload.nodes?.Start?.turns,
                    payload.turns
                ];
                if (payload.dialogue_scenes) {
                    payload.dialogue_scenes.forEach(s => turnSources.push(s.turns));
                }

                turnSources.filter(Array.isArray).forEach(turns => {
                    turns.forEach(turn => {
                        try {
                            const tid = turn.id || turn.line_id;
                            if (!tid) return;

                            // Normalized IDs for matching
                            const nid = tid.replace('-', '_');
                            const locale = window.state.progress.prefs.locale || 'zh_tw';

                            const rawTrans = i18nData?.translations?.[tid] || i18nData?.translations?.[nid];
                            if (rawTrans) {
                                turn.translations_i18n = turn.translations_i18n || {};
                                turn.translations_i18n[locale] = rawTrans;
                                turn.translations_i18n.translation = rawTrans; 
                                turn.translation = rawTrans; 
                            }

                            // Map Atoms
                            if (Array.isArray(atomsData)) {
                                const entry = atomsData.find(a => 
                                    (a.turn_id === tid || a.turn_id === nid || a.line_id === tid || a.line_id === nid)
                                );
                                
                                if (entry && entry.atoms) {
                                    // DEEP SANITY CHECK: Compare the actual text content
                                    const atomsText = entry.atoms.map(a => a.text).join('').replace(/\s/g, '').replace(/[.,?!~]/g, '');
                                    const sourceText = (turn.text?.ko || turn.ko || '').replace(/\s/g, '').replace(/[.,?!~]/g, '');
                                    
                                    // If text is significantly different, the assets are misaligned
                                    if (atomsText !== sourceText && sourceText.length > 0) {
                                        console.warn(`[ENRICH] Content Mismatch for ${tid}: Atoms text ("${atomsText}") != Source text ("${sourceText}"). Discarding atoms for alignment.`);
                                        turn.atoms = []; 
                                        turn.alignment_failed = true; // MARK AS BAD
                                    } else {
                                        turn.atoms = entry.atoms;
                                    }
                                } else if (atomsData[0]?.lesson_id) {
                                    const turnAtoms = atomsData.filter(a => a.line_id === tid || a.line_id === nid);
                                    if (turnAtoms.length > 0) {
                                        turn.atoms = turnAtoms.map(a => ({
                                            id: a.gold_final_atom_id,
                                            text: a.surface,
                                            pos: a.gsd_action
                                        }));
                                    }
                                }
                            }
                        } catch (err) {
                            console.warn(`Error enriching turn:`, err);
                        }
                    });
                });
            });
            console.log("Enrichment complete. Re-rendering...");
            if (window.renderCurrentNode) window.renderCurrentNode();
        } catch (e) {
            console.warn("Enrichment failed", e);
        }
    },

    selectSegment(id) {
        console.log(`Segment selected: ${id}`);
        window.state.activeSegmentId = id;
        document.querySelectorAll('.subtitle-row, .dialogue-turn').forEach(el => el.classList.toggle('active', el.dataset.segmentId === id));
        // Deep integration: when a segment is selected, the first atom could be pre-selected?
    },

    selectAtom(id, event) {
        if (event) event.stopPropagation();
        console.log(`Atom selected: ${id}`);
        // Highlight in UI
        document.querySelectorAll('.atom-seg').forEach(el => el.classList.toggle('active', el.dataset.atomId === id));
        
        // Find atom data in current state
        const atomData = this.getAtomData(id);
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

    renderKoreanSegmentation(seg) {
        if (!seg.atoms || seg.atoms.length === 0) {
            const raw = window.escapeHtml(seg.ko || '');
            if (seg.alignment_failed) {
                return `<span class="alignment-warning" title="資料對齊異常：單字分割已停用">${raw} <i class="fas fa-info-circle" style="font-size:0.7em;"></i></span>`;
            }
            return raw;
        }

        return seg.atoms.map(a => {
            if (a.pos === 'space' || a.id?.includes(':space:')) {
                return ' ';
            }
            const cleanId = a.id || `${a.text}-${a.pos}`;
            return `<span class="atom-seg" data-atom-id="${cleanId}">${window.escapeHtml(a.text)}</span>`;
        }).join('');
    },

    renderLibraryBook() {
        // Legacy shim for unit-scoped library update
        console.log("Library refactored. Book is global.");
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
                this.elements.unitIndicator.textContent = `導覽中: ${window.state.data.unit.unit_id}`;
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
                    <h3>暫無課程資料</h3>
                    <p class="muted-text">目前只保留知識文庫的單一重建條目。</p>
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
            const [manifestResp, knowledgeResp, sentenceResp] = await Promise.all([
                fetch(`data/library_manifest.json?v=${Date.now()}`),
                fetch(`data/runtime/zh_tw/knowledge.json?v=${Date.now()}`),
                fetch(`data/runtime/zh_tw/example_sentence.json?v=${Date.now()}`)
            ]);
            if (manifestResp.ok) {
                this.libManifest = await manifestResp.json();
            }
            if (knowledgeResp.ok) {
                this.libKnowledgeRuntime = await knowledgeResp.json();
            }
            if (sentenceResp.ok) {
                const runtimeSentences = await sentenceResp.json();
                this.libSentences = runtimeSentences.reduce((acc, item) => {
                    if (item && item.id) acc[item.id] = item;
                    return acc;
                }, {});
            }
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
            "grammar": "韓文法",
            "pattern": "必修句型",
            "connector": "連接詞",
            "expression": "慣用語",
            "vocab": "主題單字"
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
                    <h3>${subId} 內容準備中</h3>
                    <p>此章節的編寫正在進行中，敬請期待。</p>
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
                        <button class="btn tiny-text" onclick="window.resetAudioEngine()" style="padding:4px 8px; border-radius:8px; opacity:0.8; color:var(--warn); border-color:var(--warn-soft);">🔊 重設語音</button>
                        <button class="btn tiny-text" onclick="APP.showLibTOC()" style="padding:4px 8px; border-radius:8px; opacity:0.8;">全部主題</button>
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
                        <button type="button" class="audio-btn" onclick="event.stopPropagation(); APP.playOriginalOrTTS('${fallbackKo}'); return false;" title="播放 TTS">
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
                    <h1 style="font-size:32px; color:var(--text); margin:0 0 16px 0; line-height:1.2;">${window.escapeHtml(window.i18nText(data.title_i18n, window.currentLocale(), data.id || ''))}</h1>
                    <div style="height:4px; width:60px; background:var(--accent); border-radius:2px; margin-bottom:24px;"></div>
                    <p class="lead" style="font-size:18px; font-weight:500; color:var(--muted); line-height:1.6; margin:0;">${window.escapeHtml(window.i18nText(data.summary_i18n, window.currentLocale(), ''))}</p>
                </header>

                <section class="content-block" style="margin-top:0; padding:22px; border:1px solid var(--line); border-radius:20px; background:var(--card);">
                    <div class="rule-body">
                        ${explanationHtml || '<p class="md-paragraph muted">目前沒有內容。</p>'}
                    </div>
                </section>

                ${(window.i18nText(data.usage_notes_i18n, window.currentLocale(), []) || []).length > 0 ? `
                    <h2 style="margin-top:48px;">📌 重點提示</h2>
                    <div class="usage-tips" style="margin-bottom:32px; display:flex; flex-wrap:wrap; gap:8px;">
                        ${(window.i18nText(data.usage_notes_i18n, window.currentLocale(), []) || []).map(note => `<div class="tag">${window.escapeHtml(note)}</div>`).join('')}
                    </div>
                ` : ''}

                <div class="example-section" style="margin-top:28px;">
                    <div class="section-subtitle">例句</div>
                    ${hasExamples ? `<div class="example-grid" style="display:grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap:16px;">${examplesHtml}</div>` : '<p class="muted-text">目前沒有對應例句。</p>'}
                </div>
            </article>
        `;
    },

    playOriginalOrTTS(text) {
        if (!text) return;
        console.log("TTS-only test mode: speaking via Web Speech API.");
        if (window.speakKo) window.speakKo(text);
    },

    showLibTOC() {
        this.elements.libReader.innerHTML = `
            <div class="empty-state" style="margin-top:100px;">
                <div class="icon" style="font-size:48px;">📖</div>
                <h3>歡迎來到 Lingourmet 韓語知識文庫</h3>
                <p class="muted-text">請從左側目錄選擇一個主題開始學習。</p>
                <div class="featured-list" id="libFeaturedList" style="margin-top:32px;"></div>
            </div>
        `;
        this.renderLibFeatured();
        if (this.elements.libCurrentTitle) this.elements.libCurrentTitle.textContent = '請選擇主題';
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
                <p class="tiny-text muted">快速查看此語法條目</p>
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
        if (idx > -1) {
            window.state.currentIndex = idx;
            this.switchView('lessonView');
            window.renderCurrentNode();
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
            <div class="meta-box"><span class="k">主題</span><span class="v">${unit.displayTheme}</span></div>
            <div class="meta-box"><span class="k">類型</span><span class="v">單元課程</span></div>
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
    APP.elements.nodeList.innerHTML = window.state.data.sequence.map((n, i) => `
        <div class="node-card ${i === window.state.currentIndex ? 'active' : ''}" onclick="window.setIndex(${i})">
            <span class="num">${i + 1}</span>
            <span class="txt">${window.escapeHtml(window.nodeTitleText(n, 'zh_tw') || n.id)}</span>
        </div>
    `).join('');
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
    APP.elements.roleSummaryBox.innerHTML = '<h3>內容分佈</h3>' + Object.entries(counts).map(([k, v]) => `
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

    if (window.renderDetailHeader) window.renderDetailHeader(normalized);
    if (window.renderDetailSummary) window.renderDetailSummary(normalized);

    const { contentHtml, interactionHtml } = window.RendererRegistry.dispatch(normalized);
    if (APP.elements.detailBody) {
        APP.elements.detailBody.innerHTML = contentHtml + interactionHtml;
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

    // Mock definitions if missing (Heuristic)
    let definition = atom.definition || "(尚無詳細釋義)";
    if (atom.id && atom.id.includes('안녕하세요')) definition = "【釋義】安寧，平安。用於打招呼，相當於『您好』。";
    if (atom.id && atom.id.includes('여러분')) definition = "【釋義】各位，大家。";

    container.innerHTML = `
        <button class="close-support" onclick="document.getElementById('supportDetail').classList.remove('active')">✕</button>
        <div class="support-header">
            <div>
                <div class="support-title">${window.escapeHtml(atom.text)}</div>
                <div class="support-meta">${window.escapeHtml(atom.lemma || atom.text)} · ${window.escapeHtml(atom.id)}</div>
            </div>
            <span class="pos-badge">${window.escapeHtml(atom.pos || 'unknown')}</span>
        </div>
        <div class="support-definition">
            ${window.escapeHtml(definition)}
        </div>
        <div style="margin-top: 20px; display: flex; gap: 10px;">
            <button class="btn tiny-text audio-btn" style="flex:1" data-text="${window.escapeJsSingle(atom.text)}">🔊 播放</button>
            <button class="btn tiny-text" style="flex:1" onclick="window.showToast('已加入生字本')">⭐ 收藏</button>
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
