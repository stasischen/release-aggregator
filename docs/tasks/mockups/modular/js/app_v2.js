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
            const resp = await fetch('data/library_manifest.json');
            if (resp.ok) {
                this.libManifest = await resp.json();
                this.renderLibToc();
                this.renderLibFeatured();
            }
        } catch (e) { console.error("Library init error", e); }
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
        
        /*
        .lib-sidebar {
            position: fixed !important;
            top: var(--nav-height) !important;
            bottom: 0 !important;
            left: 0 !important;
            width: 280px !important;
            transform: translateX(-105%) !important;
            box-shadow: 10px 0 30px rgba(0,0,0,0.2) !important;
            visibility: hidden !important;
            display: flex !important;
        }
        
        .lib-sidebar.open {
            transform: translateX(0) !important;
            visibility: visible !important;
        }
        */
        
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

    async selectLibCategory(catId, subId) {
        // In a real app, this would query a real metadata DB. 
        // For mockup, we show the featured item if it matches "particle", or show a list.
        if (subId === 'particle') {
            const item = this.libManifest.featured.find(f => f.sub === 'particle');
            if (item) this.loadLibRule(item.path, item.title);
        } else {
            this.elements.libReader.innerHTML = `
                <div class="empty-state">
                    <h3>${subId} 內容準備中</h3>
                    <p>此章節的編寫正在進行中，敬請期待。</p>
                </div>
            `;
            if (this.elements.libCurrentTitle) this.elements.libCurrentTitle.textContent = subId;
            this.toggleLibSidebar(false);
        }
    },

    async loadLibRule(path, title) {
        try {
            const resp = await fetch(path);
            if (!resp.ok) throw new Error('Rule load failed');
            const data = await resp.json();
            
            this.renderLibReader(data);
            if (this.elements.libCurrentTitle) this.elements.libCurrentTitle.textContent = title;
            this.toggleLibSidebar(false);
            if (this.elements.libReader) this.elements.libReader.scrollTop = 0;
        } catch (e) { console.error(e); }
    },

    renderLibReader(data) {
        if (!this.elements.libReader) return;
        
        const examplesHtml = (data.example_bank || []).slice(0, 5).map(ex => `
            <div class="example-card animate-in">
                <div class="example-ko">${window.escapeHtml(ex.ko)}</div>
                <div class="example-zh">${window.escapeHtml(ex.zh_tw)}</div>
            </div>
        `).join('');

        this.elements.libReader.innerHTML = `
            <article class="animate-in">
                <h1 style="color:var(--accent);">${window.escapeHtml(data.title_zh_tw)}</h1>
                <p class="lead" style="font-size:18px; font-weight:500;">${window.escapeHtml(data.summary_zh_tw)}</p>
                
                <div class="rule-body">
                    ${window.markdownToHtmlLite(data.explanation_md_zh_tw)}
                </div>

                <h2 style="margin-top:48px;">📌 變化與用法範例</h2>
                <div class="usage-tips" style="margin-bottom:32px;">
                    ${(data.usage_notes_zh_tw || []).map(note => `<div class="tag" style="margin-bottom:8px; display:block;">${window.escapeHtml(note)}</div>`).join('')}
                </div>

                <div class="example-section">
                    <div class="section-subtitle">🔊 精選例句 (Examples)</div>
                    ${examplesHtml}
                </div>
            </article>
        `;
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
