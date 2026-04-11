/**
 * Lingourmet Stable App V2 - Full Feature Set
 */
const FIXTURES_INDEX = 'data/fixtures.json';

const APP = {
    elements: {},
    init() {
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
        this.wireEvents();
        this.bootstrap();
        this.initLibrary();
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
    },

    async bootstrap() {
        try {
            const fResp = await fetch(FIXTURES_INDEX);
            let fixtures = { units: [] };
            if (fResp.ok) fixtures = await fResp.json();
            this.renderCourseMap(fixtures);

            const lastPath = localStorage.getItem('agg_gen_last_unit_path') || (fixtures.units[0]?.path);
            if (lastPath) this.loadUnit(lastPath, false);
        } catch (e) { console.error("Bootstrap error", e); }
        this.switchView('courseMapView');
    },

    async loadUnit(path, autoSwitch = true) {
        try {
            const resp = await fetch(path);
            if (!resp.ok) throw new Error('Load failed');
            window.state.data = await resp.json();
            window.state.currentIndex = 0;
            localStorage.setItem('agg_gen_last_unit_path', path);

            window.loadProgress();
            window.renderSidebar();
            window.renderCurrentNode();
            this.renderLibraryBook();
            if (autoSwitch) this.switchView('lessonView');
            if (window.showToast) window.showToast(`已載入: ${window.state.data.unit.unit_id}`);
        } catch (e) { console.error(e); }
    },

    renderLibraryBook() {
        // Legacy shim for unit-scoped library update
        console.log("Library refactored. Book is global.");
    },

    switchView(viewId) {
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
        this.elements.courseMapGrid.innerHTML = fixtures.units.map(u => {
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
            // Load Manifest
            const manifestResp = await fetch('data/library_manifest.json');
            if (manifestResp.ok) {
                this.libManifest = await manifestResp.json();
                this.renderLibToc();
                this.renderLibFeatured();
            }
            
            // Load Global Sentences (Example Bank)
            const sentenceResp = await fetch('data/global_sentences.json');
            if (sentenceResp.ok) {
                this.libSentences = await sentenceResp.json();
                console.log("Global Sentence Bank loaded.");
            }
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
            <div class="unit-card" style="text-align:left; cursor:pointer; margin-bottom:12px; display:flex; align-items:center; gap:12px;" onclick="APP.loadLibRule('${f.path}', '${f.title}')">
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
                    <button class="btn tiny-text" onclick="APP.showLibTOC()" style="padding:4px 8px; border-radius:8px; opacity:0.8;">全部主題</button>
                </div>
                <div class="list-grid">
                    ${listHtml}
                </div>
            </div>
        `;
        
        if (this.elements.libCurrentTitle) this.elements.libCurrentTitle.textContent = displaySub;
        this.toggleLibSidebar(false);
    },

    async loadLibRule(path, title) {
        try {
            const resp = await fetch(path);
            if (!resp.ok) throw new Error('Rule load failed');
            const data = await resp.json();
            
            const meta = (this.libManifest.items || []).find(it => it.path === path) || {};
            
            if (!data.example_bank) data.example_bank = [];
            const refs = meta.example_sentence_refs || data.example_sentence_refs || [];
            if (refs.length > 0 && this.libSentences) {
                refs.forEach(sid => {
                    const s = this.libSentences[sid];
                    if (s) {
                        data.example_bank.push({
                            id: sid, ko: s.ko, zh_tw: s.zh_tw || "(尚無翻譯)"
                        });
                    }
                });
            }
            
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
        
        const examplesHtml = (data.example_bank || []).map((ex, idx) => {
            const audioPath = `data/audio/${ex.id}.mp3`;
            const fallbackKo = window.escapeJsSingle(ex.ko);
            return `
                <div class="example-card animate-in">
                    <div class="example-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <div class="example-ko" style="font-weight:700; color:var(--text);">${window.escapeHtml(ex.ko)}</div>
                        <button class="audio-btn" onclick="APP.playOriginalOrTTS('${fallbackKo}', '${audioPath}')" title="播放音檔">
                            <span class="icon">🔊</span>
                        </button>
                    </div>
                    <div class="example-zh" style="color:var(--muted); font-size:14px;">${window.escapeHtml(ex.zh_tw)}</div>
                </div>
            `;
        }).join('');

        const levelClass = (meta.level || 'A1').toLowerCase();

        this.elements.libReader.innerHTML = `
            <article class="animate-in" style="padding-bottom: 60px;">
                <header class="rule-header" style="margin-bottom:32px;">
                    <div class="meta-strip" style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                        <span class="level-badge ${levelClass}">${meta.level || 'A1'}</span>
                        <span class="tiny-text muted" style="letter-spacing:0.05em;">${data.id || ''}</span>
                    </div>
                    <h1 style="font-size:32px; color:var(--text); margin:0 0 16px 0; line-height:1.2;">${window.escapeHtml(data.title_zh_tw)}</h1>
                    <div style="height:4px; width:60px; background:var(--accent); border-radius:2px; margin-bottom:24px;"></div>
                    <p class="lead" style="font-size:18px; font-weight:500; color:var(--muted); line-height:1.6; margin:0;">${window.escapeHtml(data.summary_zh_tw)}</p>
                </header>
                
                <div class="rule-body">
                    ${window.markdownToHtmlLite(data.explanation_md_zh_tw || data.explanation || '')}
                </div>

                <h2 style="margin-top:48px;">📌 變化與用法範例</h2>
                <div class="usage-tips" style="margin-bottom:32px; display:flex; flex-wrap:wrap; gap:8px;">
                    ${(data.usage_notes_zh_tw || []).map(note => `<div class="tag">${window.escapeHtml(note)}</div>`).join('')}
                </div>

                <div class="example-section">
                    <div class="section-subtitle">🔊 精選例句 (Examples)</div>
                    <div class="example-grid" style="display:grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap:16px;">
                        ${examplesHtml}
                    </div>
                </div>
            </article>
        `;
    },

    async playOriginalOrTTS(text, audioPath) {
        if (!text) return;

        // On Mac/Browsers, we must trigger speech immediately if we know the audio will fail 
        // to avoid being blocked by the "non-user-gesture" check in async callbacks.
        const isPlaceholder = audioPath.includes('unknown') || audioPath.includes('ex.ko');

        if (!isPlaceholder) {
            try {
                const audio = new Audio(audioPath);
                await audio.play();
                return;
            } catch (e) {
                console.warn("Audio file play failed, falling back to TTS:", e);
                // Fall through to TTS
            }
        }

        // TTS Fallback
        if (window.speakKo) {
            window.speakKo(text);
        } else {
            console.error("TTS engine (window.speakKo) not found.");
        }
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
            <div class="unit-card" style="text-align:left; cursor:pointer;" onclick="APP.loadLibRule('${f.path}', '${f.title}')">
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
            <span class="txt">${window.escapeHtml(n.title_zh_tw || n.id)}</span>
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
