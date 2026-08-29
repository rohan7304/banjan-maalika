/**
 * Bhajan Maalika (भजन मालिका) - Main Application Controller
 * Handles SPA navigation, views, lyrics editor with auto-save, theme switching,
 * Marathi typography helpers, and interactive modals.
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- Application State ---
    const AppState = {
        currentView: 'splash', // 'splash', 'home', 'collection', 'note'
        activeCollectionId: null,
        activeBhajanId: null,
        isReadingMode: false,
        autoSaveTimeout: null,
        searchQuery: ''
    };

    // --- DOM Elements ---
    const DOM = {
        // Views
        views: {
            splash: document.getElementById('splash-view'),
            home: document.getElementById('home-view'),
            collection: document.getElementById('collection-view'),
            note: document.getElementById('note-view')
        },
        // Navigation & Layout
        navbar: document.getElementById('main-navbar'),
        navBrandBtn: document.getElementById('nav-brand-btn'),
        themeToggleBtn: document.getElementById('theme-toggle-btn'),
        themeSunIcon: document.querySelector('.theme-icon-sun'),
        themeMoonIcon: document.querySelector('.theme-icon-moon'),
        globalSearchInput: document.getElementById('global-search-input'),
        searchClearBtn: document.getElementById('search-clear-btn'),
        fabContainer: document.getElementById('fab-container'),
        fabAddBtn: document.getElementById('fab-add-btn'),
        navAddBtn: document.getElementById('nav-add-btn'),

        // Home View Elements
        collectionsGrid: document.getElementById('collections-grid'),
        collectionsEmptyState: document.getElementById('collections-empty-state'),
        statsText: document.getElementById('stats-text'),
        homeCreateColBtn: document.getElementById('home-create-col-btn'),
        emptyCreateColBtn: document.getElementById('empty-create-col-btn'),

        // Collection View Elements
        colBackBtn: document.getElementById('col-back-btn'),
        colDetailIcon: document.getElementById('col-detail-icon'),
        colDetailImg: document.getElementById('col-detail-img'),
        colDetailName: document.getElementById('col-detail-name'),
        colDetailCount: document.getElementById('col-detail-count'),
        colDetailDate: document.getElementById('col-detail-date'),
        colAddBhajanBtn: document.getElementById('col-add-bhajan-btn'),
        colEditBtn: document.getElementById('col-edit-btn'),
        colDeleteBtn: document.getElementById('col-delete-btn'),
        bhajansListContainer: document.getElementById('bhajans-list-container'),
        bhajansEmptyState: document.getElementById('bhajans-empty-state'),
        emptyAddBhajanBtn: document.getElementById('empty-add-bhajan-btn'),

        // Note View Elements
        noteBackBtn: document.getElementById('note-back-btn'),
        noteBackColTitle: document.getElementById('note-back-col-title'),
        saveStatusIndicator: document.getElementById('save-status-indicator'),
        saveStatusText: document.getElementById('save-status-text'),
        noteCopyBtn: document.getElementById('note-copy-btn'),
        noteDeleteBtn: document.getElementById('note-delete-btn'),
        btnModeEdit: document.getElementById('btn-mode-edit'),
        btnModeRead: document.getElementById('btn-mode-read'),
        fontDecreaseBtn: document.getElementById('font-decrease-btn'),
        fontIncreaseBtn: document.getElementById('font-increase-btn'),
        fontSizeDisplay: document.getElementById('font-size-display'),
        marathiHelperBar: document.getElementById('marathi-helper-bar'),
        noteTitleInput: document.getElementById('note-title-input'),
        noteLyricsEditor: document.getElementById('note-lyrics-editor'),
        noteLyricsReader: document.getElementById('note-lyrics-reader'),

        // Modals
        modalCollection: document.getElementById('modal-collection'),
        modalColHeading: document.getElementById('modal-col-heading'),
        modalColId: document.getElementById('modal-col-id'),
        inputColName: document.getElementById('input-col-name'),
        inputColSubtitle: document.getElementById('input-col-subtitle'),
        colImgPreview: document.getElementById('col-img-preview'),
        inputColFile: document.getElementById('input-col-file'),
        deityPresetsPicker: document.getElementById('deity-presets-picker'),
        modalColClose: document.getElementById('modal-col-close'),
        modalColCancel: document.getElementById('modal-col-cancel'),
        modalColSave: document.getElementById('modal-col-save'),

        modalBhajan: document.getElementById('modal-bhajan'),
        modalBhajanHeading: document.getElementById('modal-bhajan-heading'),
        modalBhajanId: document.getElementById('modal-bhajan-id'),
        inputBhajanTitle: document.getElementById('input-bhajan-title'),
        modalBhajanClose: document.getElementById('modal-bhajan-close'),
        modalBhajanCancel: document.getElementById('modal-bhajan-cancel'),
        modalBhajanSave: document.getElementById('modal-bhajan-save'),

        modalConfirm: document.getElementById('modal-confirm'),
        modalConfirmTitle: document.getElementById('modal-confirm-title'),
        modalConfirmMessage: document.getElementById('modal-confirm-message'),
        modalConfirmClose: document.getElementById('modal-confirm-close'),
        modalConfirmCancel: document.getElementById('modal-confirm-cancel'),
        modalConfirmAction: document.getElementById('modal-confirm-action'),

        // Backend Status
        backendStatusBadge: document.getElementById('backend-status-badge'),
        backendStatusDot: document.getElementById('backend-status-dot'),
        backendStatusText: document.getElementById('backend-status-text'),

        // Toast
        toast: document.getElementById('app-toast'),
        toastIcon: document.getElementById('toast-icon'),
        toastMessage: document.getElementById('toast-message')
    };

    // Selected deity image in collection modal
    let selectedCollectionImage = 'assets/images/ganesha.svg';
    let selectedCollectionIcon = '🌸';
    let onConfirmCallback = null;

    // =========================================================================
    // 1. INITIALIZATION & THEME
    // =========================================================================
    function initializeApp() {
        applyTheme(window.bhajanStorage.getTheme());
        applyFontSize(window.bhajanStorage.getFontSize());
        setupEventListeners();
        handleSplashScreen();

        // Backend Status Sync
        window.bhajanStorage.onBackendStatusChange = updateBackendStatusUI;
        updateBackendStatusUI(window.bhajanStorage.backendAvailable);

        window.addEventListener('bhajan_data_synced', () => {
            if (AppState.currentView === 'home') {
                renderHomeView(DOM.globalSearchInput.value);
            } else if (AppState.currentView === 'collection' && AppState.activeCollectionId) {
                renderCollectionView(AppState.activeCollectionId);
            }
        });
    }

    function updateBackendStatusUI(isAvailable) {
        if (!DOM.backendStatusBadge) return;
        if (isAvailable) {
            DOM.backendStatusBadge.style.borderColor = 'rgba(16, 185, 129, 0.4)';
            DOM.backendStatusDot.textContent = '🟢';
            DOM.backendStatusText.textContent = 'बॅकएंड: सक्रिय (SQLite)';
        } else {
            DOM.backendStatusBadge.style.borderColor = 'rgba(245, 158, 11, 0.4)';
            DOM.backendStatusDot.textContent = '🟡';
            DOM.backendStatusText.textContent = 'ऑफलाईन (लोकल स्टोरेज)';
        }
    }

    function applyTheme(theme) {
        window.bhajanStorage.setTheme(theme);
        if (theme === 'dark') {
            DOM.themeSunIcon.style.display = 'none';
            DOM.themeMoonIcon.style.display = 'block';
        } else {
            DOM.themeSunIcon.style.display = 'block';
            DOM.themeMoonIcon.style.display = 'none';
        }
    }

    function applyFontSize(size) {
        const validatedSize = window.bhajanStorage.setFontSize(size);
        document.documentElement.style.setProperty('--editor-font-size', `${validatedSize}px`);
        if (DOM.fontSizeDisplay) {
            DOM.fontSizeDisplay.textContent = `${validatedSize}px`;
        }
    }

    // =========================================================================
    // 2. SPLASH SCREEN CONTROLLER
    // =========================================================================
    function handleSplashScreen() {
        let hasDismissed = false;

        const dismissSplash = () => {
            if (hasDismissed) return;
            hasDismissed = true;

            DOM.views.splash.classList.add('fade-out');
            setTimeout(() => {
                DOM.views.splash.style.display = 'none';
                navigateTo('home');
            }, 550);
        };

        // Transition automatically after 2.5 seconds
        const splashTimer = setTimeout(dismissSplash, 2500);

        // Or transition instantly on user tap / click / keypress anywhere
        DOM.views.splash.addEventListener('click', () => {
            clearTimeout(splashTimer);
            dismissSplash();
        });

        document.addEventListener('keydown', function keyHandler(e) {
            if (AppState.currentView === 'splash') {
                clearTimeout(splashTimer);
                dismissSplash();
                document.removeEventListener('keydown', keyHandler);
            }
        });
    }

    // =========================================================================
    // 3. SPA ROUTER & NAVIGATION
    // =========================================================================
    function navigateTo(viewName, params = {}) {
        AppState.currentView = viewName;

        // Hide all views
        Object.values(DOM.views).forEach(view => {
            if (view) {
                view.classList.remove('active');
                if (view !== DOM.views.splash) {
                    view.style.display = 'none';
                }
            }
        });

        // Configure Layout & Navbar visibility
        if (viewName === 'splash') {
            DOM.navbar.style.display = 'none';
            DOM.fabContainer.style.display = 'none';
        } else if (viewName === 'home') {
            DOM.navbar.style.display = 'block';
            DOM.fabContainer.style.display = 'block';
            renderHomeView();
        } else if (viewName === 'collection') {
            DOM.navbar.style.display = 'block';
            DOM.fabContainer.style.display = 'none';
            AppState.activeCollectionId = params.collectionId;
            renderCollectionView(params.collectionId);
        } else if (viewName === 'note') {
            DOM.navbar.style.display = 'none'; // Note view has its own customized action navbar
            DOM.fabContainer.style.display = 'none';
            AppState.activeCollectionId = params.collectionId;
            AppState.activeBhajanId = params.bhajanId;
            renderNoteView(params.collectionId, params.bhajanId);
        }

        // Show active view with smooth animation
        const activeView = DOM.views[viewName];
        if (activeView) {
            activeView.style.display = 'block';
            // Force browser reflow to trigger transition
            void activeView.offsetWidth;
            activeView.classList.add('active');
        }

        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // =========================================================================
    // 4. HOME VIEW CONTROLLER
    // =========================================================================
    function renderHomeView(filterQuery = '') {
        const { collections, matchingBhajans } = window.bhajanStorage.search(filterQuery);

        // Update Stats Badge
        const totalCols = collections.length;
        const totalBhajans = collections.reduce((acc, c) => acc + (c.bhajans ? c.bhajans.length : 0), 0);
        DOM.statsText.innerHTML = `<strong>${totalCols}</strong> संकलने • <strong>${totalBhajans}</strong> भजने`;

        DOM.collectionsGrid.innerHTML = '';

        if (collections.length === 0) {
            DOM.collectionsGrid.style.display = 'none';
            DOM.collectionsEmptyState.style.display = 'block';
            return;
        }

        DOM.collectionsGrid.style.display = 'grid';
        DOM.collectionsEmptyState.style.display = 'none';

        collections.forEach(col => {
            const bhajanCount = col.bhajans ? col.bhajans.length : 0;
            const card = document.createElement('article');
            card.className = 'collection-card';
            card.style.setProperty('--card-accent-color', col.color || '#FF7A00');

            card.innerHTML = `
                <div class="card-top">
                    <button type="button" class="card-menu-btn" title="पर्याय (Options)" data-action="menu" data-id="${col.id}">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="1"></circle>
                            <circle cx="12" cy="5" r="1"></circle>
                            <circle cx="12" cy="19" r="1"></circle>
                        </svg>
                    </button>
                </div>
                <div class="card-content">
                    <h3 class="collection-name">${escapeHtml(col.name)}</h3>
                    ${col.subtitle ? `<p class="collection-subtitle">${escapeHtml(col.subtitle)}</p>` : ''}
                </div>
                <div class="card-bottom">
                    <span class="card-count-badge">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                        </svg>
                        ${bhajanCount} ${bhajanCount === 1 ? 'भजन' : 'भजने'}
                    </span>
                    <span>उघडा →</span>
                </div>
            `;

            // Card click navigates to Collection View
            card.addEventListener('click', (e) => {
                const menuBtn = e.target.closest('[data-action="menu"]');
                if (menuBtn) {
                    e.stopPropagation();
                    openEditCollectionModal(col.id);
                } else {
                    navigateTo('collection', { collectionId: col.id });
                }
            });

            DOM.collectionsGrid.appendChild(card);
        });
    }

    // =========================================================================
    // 5. COLLECTION VIEW CONTROLLER
    // =========================================================================
    function renderCollectionView(collectionId) {
        const collection = window.bhajanStorage.getCollection(collectionId);
        if (!collection) {
            showToast('संकलन सापडले नाही', '⚠️');
            navigateTo('home');
            return;
        }

        DOM.colDetailName.textContent = collection.name;
        const count = collection.bhajans ? collection.bhajans.length : 0;
        DOM.colDetailCount.textContent = `${count} ${count === 1 ? 'भजन' : 'भजने'}`;
        DOM.colDetailDate.textContent = collection.subtitle || 'दैनिक उपासना संकलन';

        DOM.bhajansListContainer.innerHTML = '';

        if (!collection.bhajans || collection.bhajans.length === 0) {
            DOM.bhajansListContainer.style.display = 'none';
            DOM.bhajansEmptyState.style.display = 'block';
            return;
        }

        DOM.bhajansListContainer.style.display = 'flex';
        DOM.bhajansEmptyState.style.display = 'none';

        collection.bhajans.forEach((bhajan, index) => {
            const card = document.createElement('div');
            card.className = 'bhajan-card';

            // First line of lyrics preview
            const firstLine = bhajan.content ? bhajan.content.trim().split('\n')[0] : 'कोणतेही बोल लिहिलेले नाहीत...';

            card.innerHTML = `
                <div class="bhajan-card-left">
                    <div class="bhajan-number-pill">${index + 1}</div>
                    <div class="bhajan-info">
                        <h4 class="bhajan-title">${escapeHtml(bhajan.title)}</h4>
                        <p class="bhajan-snippet">${escapeHtml(firstLine)}</p>
                    </div>
                </div>
                <div class="bhajan-card-actions">
                    <svg class="btn-arrow-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                </div>
            `;

            card.addEventListener('click', () => {
                navigateTo('note', { collectionId: collection.id, bhajanId: bhajan.id });
            });

            DOM.bhajansListContainer.appendChild(card);
        });
    }

    // =========================================================================
    // 6. NOTE / LYRICS EDITOR CONTROLLER
    // =========================================================================
    function renderNoteView(collectionId, bhajanId) {
        const collection = window.bhajanStorage.getCollection(collectionId);
        const bhajan = window.bhajanStorage.getBhajan(collectionId, bhajanId);

        if (!collection || !bhajan) {
            showToast('भजन सापडले नाही', '⚠️');
            navigateTo('home');
            return;
        }

        // Setup Header
        DOM.noteBackColTitle.textContent = collection.name;
        DOM.noteTitleInput.value = bhajan.title;
        DOM.noteLyricsEditor.value = bhajan.content || '';

        // Default to edit mode initially
        setNoteMode(false);
        setSaveStatus('saved');

        // Auto-focus editor if newly created and empty
        if (!bhajan.content) {
            setTimeout(() => DOM.noteLyricsEditor.focus(), 150);
        }
    }

    function setNoteMode(isReading) {
        AppState.isReadingMode = isReading;

        if (isReading) {
            DOM.btnModeRead.classList.add('active');
            DOM.btnModeEdit.classList.remove('active');
            DOM.noteLyricsEditor.classList.add('hidden');
            DOM.noteLyricsReader.classList.add('active');
            DOM.marathiHelperBar.style.display = 'none';

            // Format lyrics for recitation/reading (preserve paragraphs and stanza spacing)
            const rawContent = DOM.noteLyricsEditor.value.trim();
            if (!rawContent) {
                DOM.noteLyricsReader.innerHTML = '<p style="color: var(--text-tertiary); font-style: italic;">कोणतेही बोल उपलब्ध नाहीत. बोल जोडण्यासाठी "संपादक" वर क्लिक करा.</p>';
            } else {
                DOM.noteLyricsReader.textContent = rawContent;
            }
        } else {
            DOM.btnModeEdit.classList.add('active');
            DOM.btnModeRead.classList.remove('active');
            DOM.noteLyricsEditor.classList.remove('hidden');
            DOM.noteLyricsReader.classList.remove('active');
            DOM.marathiHelperBar.style.display = 'flex';
        }
    }

    function triggerAutoSave() {
        if (!AppState.activeCollectionId || !AppState.activeBhajanId) return;

        setSaveStatus('saving');

        if (AppState.autoSaveTimeout) {
            clearTimeout(AppState.autoSaveTimeout);
        }

        AppState.autoSaveTimeout = setTimeout(async () => {
            const title = DOM.noteTitleInput.value.trim() || 'नवीन भजन (Untitled Bhajan)';
            const content = DOM.noteLyricsEditor.value;

            const res = await window.bhajanStorage.updateBhajan(AppState.activeCollectionId, AppState.activeBhajanId, {
                title: title,
                content: content
            });

            if (res !== false) {
                setSaveStatus('saved');
            } else {
                setSaveStatus('saved'); // local storage saved
            }
        }, 300);
    }

    function setSaveStatus(status) {
        if (status === 'saving') {
            DOM.saveStatusIndicator.className = 'save-status-pill saving';
            DOM.saveStatusText.textContent = 'जतन करत आहे...';
        } else if (status === 'saved') {
            DOM.saveStatusIndicator.className = 'save-status-pill saved';
            DOM.saveStatusText.textContent = 'जतन झाले ✓';
        }
    }

    function insertAtCursor(textarea, text) {
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const before = textarea.value.substring(0, start);
        const after = textarea.value.substring(end);

        textarea.value = before + text + after;
        textarea.selectionStart = textarea.selectionEnd = start + text.length;
        textarea.focus();
        triggerAutoSave();
    }

    // =========================================================================
    // 7. MODALS & FORMS HANDLING
    // =========================================================================
    function openCreateCollectionModal() {
        DOM.modalColHeading.textContent = 'नवीन संकलन तयार करा';
        DOM.modalColId.value = '';
        DOM.inputColName.value = '';
        DOM.inputColSubtitle.value = '';
        openModal(DOM.modalCollection);
        setTimeout(() => DOM.inputColName.focus(), 100);
    }

    function openEditCollectionModal(colId) {
        const col = window.bhajanStorage.getCollection(colId);
        if (!col) return;

        DOM.modalColHeading.textContent = 'संकलन संपादित करा';
        DOM.modalColId.value = col.id;
        DOM.inputColName.value = col.name;
        DOM.inputColSubtitle.value = col.subtitle || '';
        openModal(DOM.modalCollection);
        setTimeout(() => DOM.inputColName.focus(), 100);
    }

    function openCreateBhajanModal() {
        DOM.modalBhajanHeading.textContent = 'नवीन भजन जोडा';
        DOM.modalBhajanId.value = '';
        DOM.inputBhajanTitle.value = '';
        openModal(DOM.modalBhajan);
        setTimeout(() => DOM.inputBhajanTitle.focus(), 100);
    }

    function openModal(modalEl) {
        modalEl.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeModal(modalEl) {
        modalEl.classList.remove('active');
        document.body.style.overflow = '';
    }

    function showConfirmModal(title, message, onConfirm) {
        DOM.modalConfirmTitle.textContent = title;
        DOM.modalConfirmMessage.textContent = message;
        onConfirmCallback = onConfirm;
        openModal(DOM.modalConfirm);
    }

    function showToast(message, icon = '✨') {
        DOM.toastIcon.textContent = icon;
        DOM.toastMessage.textContent = message;
        DOM.toast.classList.add('show');
        setTimeout(() => {
            DOM.toast.classList.remove('show');
        }, 2600);
    }

    // =========================================================================
    // 8. EVENT LISTENERS
    // =========================================================================
    function setupEventListeners() {
        // --- Theme Toggle ---
        DOM.themeToggleBtn.addEventListener('click', () => {
            const newTheme = window.bhajanStorage.toggleTheme();
            applyTheme(newTheme);
            showToast(newTheme === 'dark' ? 'डार्क थीम लागू केली' : 'लाईट थीम लागू केली', newTheme === 'dark' ? '🌙' : '☀️');
        });

        // --- Brand click -> Home ---
        DOM.navBrandBtn.addEventListener('click', () => navigateTo('home'));

        // --- Back Buttons ---
        DOM.colBackBtn.addEventListener('click', () => navigateTo('home'));
        DOM.noteBackBtn.addEventListener('click', () => {
            // Ensure any pending save is flushed immediately
            if (AppState.activeCollectionId && AppState.activeBhajanId) {
                window.bhajanStorage.updateBhajan(AppState.activeCollectionId, AppState.activeBhajanId, {
                    title: DOM.noteTitleInput.value.trim() || 'नवीन भजन',
                    content: DOM.noteLyricsEditor.value
                });
            }
            navigateTo('collection', { collectionId: AppState.activeCollectionId });
        });

        // --- Search Events ---
        DOM.globalSearchInput.addEventListener('input', (e) => {
            const query = e.target.value;
            if (AppState.currentView !== 'home') {
                navigateTo('home');
            }
            renderHomeView(query);
        });

        DOM.searchClearBtn.addEventListener('click', () => {
            DOM.globalSearchInput.value = '';
            renderHomeView('');
            DOM.globalSearchInput.focus();
        });

        // --- Add Collection Buttons ---
        DOM.navAddBtn.addEventListener('click', () => {
            if (AppState.currentView === 'collection') {
                openCreateBhajanModal();
            } else {
                openCreateCollectionModal();
            }
        });
        DOM.homeCreateColBtn.addEventListener('click', openCreateCollectionModal);
        DOM.emptyCreateColBtn.addEventListener('click', openCreateCollectionModal);
        DOM.fabAddBtn.addEventListener('click', () => {
            if (AppState.currentView === 'collection') {
                openCreateBhajanModal();
            } else {
                openCreateCollectionModal();
            }
        });

        // --- Collection Modal Events ---
        DOM.modalColClose.addEventListener('click', () => closeModal(DOM.modalCollection));
        DOM.modalColCancel.addEventListener('click', () => closeModal(DOM.modalCollection));

        // Marathi Suggestion chips for collection
        DOM.modalCollection.addEventListener('click', (e) => {
            const chip = e.target.closest('.preset-chip');
            if (!chip) return;
            DOM.inputColName.value = chip.getAttribute('data-name');
        });

        const handleSaveCollection = async (e) => {
            if (e) e.preventDefault();
            const name = DOM.inputColName.value.trim();
            if (!name) {
                DOM.inputColName.focus();
                return;
            }
            const subtitle = DOM.inputColSubtitle.value.trim();
            const colId = DOM.modalColId.value;

            if (colId) {
                // Update
                await window.bhajanStorage.updateCollection(colId, {
                    name: name,
                    subtitle: subtitle
                });
                showToast('संकलन अद्यतनित केले!', '🌸');
                closeModal(DOM.modalCollection);
                if (AppState.currentView === 'collection') {
                    renderCollectionView(colId);
                } else {
                    renderHomeView(DOM.globalSearchInput.value);
                }
            } else {
                // Create
                const newCol = await window.bhajanStorage.createCollection({
                    name: name,
                    subtitle: subtitle
                });
                showToast('नवीन संकलन तयार झाले!', '🌸');
                closeModal(DOM.modalCollection);
                // Open the new collection immediately so user can add bhajans!
                navigateTo('collection', { collectionId: newCol.id });
            }
        };

        const formCol = document.getElementById('form-collection');
        if (formCol) formCol.addEventListener('submit', handleSaveCollection);
        DOM.modalColSave.addEventListener('click', handleSaveCollection);

        // --- Collection View Action Buttons ---
        DOM.colAddBhajanBtn.addEventListener('click', openCreateBhajanModal);
        DOM.emptyAddBhajanBtn.addEventListener('click', openCreateBhajanModal);
        DOM.colEditBtn.addEventListener('click', () => {
            if (AppState.activeCollectionId) {
                openEditCollectionModal(AppState.activeCollectionId);
            }
        });
        DOM.colDeleteBtn.addEventListener('click', () => {
            if (!AppState.activeCollectionId) return;
            showConfirmModal(
                'संकलन हटवा?',
                'तुम्हाला खरोखर हे संकलन आणि त्यामधील सर्व भजने हटवायची आहेत का?',
                async () => {
                    await window.bhajanStorage.deleteCollection(AppState.activeCollectionId);
                    showToast('संकलन हटवले गेले', '🗑️');
                    navigateTo('home');
                }
            );
        });

        // --- Bhajan Modal Events ---
        DOM.modalBhajanClose.addEventListener('click', () => closeModal(DOM.modalBhajan));
        DOM.modalBhajanCancel.addEventListener('click', () => closeModal(DOM.modalBhajan));

        // Bhajan preset suggestions
        DOM.modalBhajan.addEventListener('click', (e) => {
            const chip = e.target.closest('.preset-chip');
            if (!chip) return;
            DOM.inputBhajanTitle.value = chip.getAttribute('data-title');
        });

        const handleSaveBhajan = async (e) => {
            if (e) e.preventDefault();
            const title = DOM.inputBhajanTitle.value.trim();
            if (!title) {
                DOM.inputBhajanTitle.focus();
                return;
            }

            if (!AppState.activeCollectionId) return;

            const newBhajan = await window.bhajanStorage.createBhajan(AppState.activeCollectionId, {
                title: title,
                content: ''
            });

            closeModal(DOM.modalBhajan);
            showToast('नवीन भजन जोडले!', '🪕');

            // Open the Note Editor directly for the new bhajan
            navigateTo('note', {
                collectionId: AppState.activeCollectionId,
                bhajanId: newBhajan.id
            });
        };

        const formBhajan = document.getElementById('form-bhajan');
        if (formBhajan) formBhajan.addEventListener('submit', handleSaveBhajan);
        DOM.modalBhajanSave.addEventListener('click', handleSaveBhajan);

        // --- Note Editor Auto-Save & Controls ---
        DOM.noteTitleInput.addEventListener('input', triggerAutoSave);
        DOM.noteLyricsEditor.addEventListener('input', triggerAutoSave);

        // Mode Switching
        DOM.btnModeEdit.addEventListener('click', () => setNoteMode(false));
        DOM.btnModeRead.addEventListener('click', () => setNoteMode(true));

        // Font Resizing (A- / A+)
        DOM.fontDecreaseBtn.addEventListener('click', () => {
            const current = window.bhajanStorage.getFontSize();
            applyFontSize(current - 2);
        });
        DOM.fontIncreaseBtn.addEventListener('click', () => {
            const current = window.bhajanStorage.getFontSize();
            applyFontSize(current + 2);
        });

        // Marathi Punctuation Helpers
        DOM.marathiHelperBar.addEventListener('click', (e) => {
            const chip = e.target.closest('.char-chip');
            if (!chip) return;
            const char = chip.getAttribute('data-char');
            insertAtCursor(DOM.noteLyricsEditor, char + ' ');
        });

        // Copy Lyrics to Clipboard
        DOM.noteCopyBtn.addEventListener('click', async () => {
            const title = DOM.noteTitleInput.value.trim();
            const lyrics = DOM.noteLyricsEditor.value.trim();
            const fullText = `${title}\n\n${lyrics}\n\n— भजन मालिका द्वारे सामायिक`;

            try {
                await navigator.clipboard.writeText(fullText);
                showToast('भजनाचे बोल कॉपी झाले!', '📋');
            } catch (err) {
                // Fallback for clipboard
                const textarea = document.createElement('textarea');
                textarea.value = fullText;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                showToast('भजनाचे बोल कॉपी झाले!', '📋');
            }
        });

        // Delete Bhajan
        DOM.noteDeleteBtn.addEventListener('click', () => {
            if (!AppState.activeCollectionId || !AppState.activeBhajanId) return;
            showConfirmModal(
                'भजन हटवा?',
                'तुम्हाला खरोखर हे भजन कायमचे हटवायचे आहे का?',
                () => {
                    window.bhajanStorage.deleteBhajan(AppState.activeCollectionId, AppState.activeBhajanId);
                    showToast('भजन हटवले गेले', '🗑️');
                    navigateTo('collection', { collectionId: AppState.activeCollectionId });
                }
            );
        });

        // --- Confirmation Modal Handlers ---
        DOM.modalConfirmClose.addEventListener('click', () => closeModal(DOM.modalConfirm));
        DOM.modalConfirmCancel.addEventListener('click', () => closeModal(DOM.modalConfirm));
        DOM.modalConfirmAction.addEventListener('click', () => {
            if (typeof onConfirmCallback === 'function') {
                onConfirmCallback();
            }
            closeModal(DOM.modalConfirm);
        });

        // Backdrop click to close modals
        [DOM.modalCollection, DOM.modalBhajan, DOM.modalConfirm].forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    closeModal(modal);
                }
            });
        });

        // Keyboard ESC support
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                [DOM.modalCollection, DOM.modalBhajan, DOM.modalConfirm].forEach(closeModal);
            }
        });
    }

    // Helper: Escape HTML
    function escapeHtml(str) {
        if (!str) return '';
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Initialize the app on load
    initializeApp();
});
