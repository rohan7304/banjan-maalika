/**
 * Bhajan Maalika (भजन मालिका) - Storage & Data Persistence Module
 * Manages localStorage caching and automatic full synchronization with the
 * Python SQLite REST API backend.
 */

const STORAGE_KEYS = {
    THEME: 'bhajan_maalika_theme',
    COLLECTIONS: 'bhajan_maalika_collections',
    FONT_SIZE: 'bhajan_maalika_font_size',
    VIEW_MODE: 'bhajan_maalika_view_mode'
};

const API_BASE = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1')
    ? window.location.origin
    : 'http://localhost:8000';

class StorageManager {
    constructor() {
        this.backendAvailable = false;
        this.onBackendStatusChange = null;
        this.init();
    }

    async init() {
        // Initialize default theme
        if (!localStorage.getItem(STORAGE_KEYS.THEME)) {
            localStorage.setItem(STORAGE_KEYS.THEME, 'light');
        }
        // Initialize default font size
        if (!localStorage.getItem(STORAGE_KEYS.FONT_SIZE)) {
            localStorage.setItem(STORAGE_KEYS.FONT_SIZE, '18');
        }

        // Check Backend Connectivity & Sync
        await this.checkBackendAndSync();
    }

    async checkBackendAndSync() {
        try {
            const res = await fetch(`${API_BASE}/api/health`, { method: 'GET', cache: 'no-cache' });
            if (res.ok) {
                this.backendAvailable = true;
                if (this.onBackendStatusChange) this.onBackendStatusChange(true);
                await this.fetchFromBackend();
            } else {
                this.backendAvailable = false;
                if (this.onBackendStatusChange) this.onBackendStatusChange(false);
            }
        } catch (e) {
            this.backendAvailable = false;
            if (this.onBackendStatusChange) this.onBackendStatusChange(false);
        }
    }

    async fetchFromBackend() {
        try {
            const res = await fetch(`${API_BASE}/api/collections`, { method: 'GET', cache: 'no-cache' });
            if (res.ok) {
                const data = await res.json();
                if (data && Array.isArray(data.collections)) {
                    this.saveLocalCollections(data.collections);
                    window.dispatchEvent(new CustomEvent('bhajan_data_synced'));
                    return data.collections;
                }
            }
        } catch (e) {
            console.warn('Could not pull collections from backend', e);
        }
        return this.getCollections();
    }

    // --- Theme Management ---
    getTheme() {
        return localStorage.getItem(STORAGE_KEYS.THEME) || 'light';
    }

    setTheme(theme) {
        localStorage.setItem(STORAGE_KEYS.THEME, theme);
        document.documentElement.setAttribute('data-theme', theme);
        if (this.backendAvailable) {
            fetch(`${API_BASE}/api/theme`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ theme: theme })
            }).catch(() => {});
        }
    }

    toggleTheme() {
        const nextTheme = this.getTheme() === 'dark' ? 'light' : 'dark';
        this.setTheme(nextTheme);
        return nextTheme;
    }

    // --- Font Size Management ---
    getFontSize() {
        return parseInt(localStorage.getItem(STORAGE_KEYS.FONT_SIZE) || '18', 10);
    }

    setFontSize(size) {
        const clamped = Math.max(14, Math.min(34, size));
        localStorage.setItem(STORAGE_KEYS.FONT_SIZE, clamped.toString());
        return clamped;
    }

    // --- Local Storage Helpers ---
    getCollections() {
        try {
            const data = localStorage.getItem(STORAGE_KEYS.COLLECTIONS);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            return [];
        }
    }

    saveLocalCollections(collections) {
        try {
            localStorage.setItem(STORAGE_KEYS.COLLECTIONS, JSON.stringify(collections));
            return true;
        } catch (e) {
            return false;
        }
    }

    getCollection(id) {
        const collections = this.getCollections();
        return collections.find(col => col.id === id) || null;
    }

    // --- Create Collection (Local + Backend API) ---
    async createCollection({ name, subtitle = '', color = '#FF7A00' }) {
        const collections = this.getCollections();
        const now = Date.now();
        const newCollection = {
            id: 'col_' + now + '_' + Math.random().toString(36).substr(2, 5),
            name: name.trim(),
            subtitle: subtitle.trim(),
            color: color || '#FF7A00',
            createdAt: now,
            updatedAt: now,
            bhajans: []
        };
        collections.unshift(newCollection);
        this.saveLocalCollections(collections);

        // Sync with Backend using the EXACT id
        if (this.backendAvailable) {
            try {
                await fetch(`${API_BASE}/api/collections`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        id: newCollection.id,
                        name: newCollection.name,
                        subtitle: newCollection.subtitle,
                        color: newCollection.color
                    })
                });
            } catch (e) {
                console.warn('Backend sync failed on createCollection', e);
            }
        }

        return newCollection;
    }

    // --- Update Collection ---
    async updateCollection(id, updates) {
        const collections = this.getCollections();
        const index = collections.findIndex(c => c.id === id);
        if (index === -1) return null;

        collections[index] = {
            ...collections[index],
            ...updates,
            updatedAt: Date.now()
        };
        this.saveLocalCollections(collections);

        // Sync with Backend
        if (this.backendAvailable) {
            try {
                await fetch(`${API_BASE}/api/collections/${encodeURIComponent(id)}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updates)
                });
            } catch (e) {
                console.warn('Backend sync failed on updateCollection', e);
            }
        }

        return collections[index];
    }

    // --- Delete Collection ---
    async deleteCollection(id) {
        let collections = this.getCollections();
        const originalLength = collections.length;
        collections = collections.filter(c => c.id !== id);
        if (collections.length !== originalLength) {
            this.saveLocalCollections(collections);

            // Sync with Backend
            if (this.backendAvailable) {
                try {
                    await fetch(`${API_BASE}/api/collections/${encodeURIComponent(id)}`, {
                        method: 'DELETE'
                    });
                } catch (e) {
                    console.warn('Backend sync failed on deleteCollection', e);
                }
            }
            return true;
        }
        return false;
    }

    // --- Bhajans CRUD ---
    getBhajan(collectionId, bhajanId) {
        const collection = this.getCollection(collectionId);
        if (!collection || !collection.bhajans) return null;
        return collection.bhajans.find(b => b.id === bhajanId) || null;
    }

    async createBhajan(collectionId, { title, content = '' }) {
        const collections = this.getCollections();
        let collection = collections.find(c => c.id === collectionId);
        if (!collection) {
            collection = { id: collectionId, name: 'भजन संकलन', bhajans: [] };
            collections.unshift(collection);
        }

        if (!collection.bhajans) collection.bhajans = [];

        const now = Date.now();
        const newBhajan = {
            id: 'bhajan_' + now + '_' + Math.random().toString(36).substr(2, 5),
            title: title.trim() || 'नवीन भजन',
            content: content,
            createdAt: now,
            updatedAt: now
        };

        collection.bhajans.unshift(newBhajan);
        this.saveLocalCollections(collections);

        // Sync with Backend using the EXACT id
        if (this.backendAvailable) {
            try {
                await fetch(`${API_BASE}/api/collections/${encodeURIComponent(collectionId)}/bhajans`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        id: newBhajan.id,
                        title: newBhajan.title,
                        content: newBhajan.content
                    })
                });
            } catch (e) {
                console.warn('Backend sync failed on createBhajan', e);
            }
        }

        return newBhajan;
    }

    async updateBhajan(collectionId, bhajanId, updates) {
        const collections = this.getCollections();
        let collection = collections.find(c => c.id === collectionId);
        if (!collection) {
            collection = { id: collectionId, name: 'भजन संकलन', bhajans: [] };
            collections.push(collection);
        }
        if (!collection.bhajans) collection.bhajans = [];

        let bhajanIndex = collection.bhajans.findIndex(b => b.id === bhajanId);
        if (bhajanIndex === -1) {
            collection.bhajans.unshift({
                id: bhajanId,
                title: updates.title || 'नवीन भजन',
                content: updates.content || '',
                updatedAt: Date.now()
            });
            bhajanIndex = 0;
        } else {
            collection.bhajans[bhajanIndex] = {
                ...collection.bhajans[bhajanIndex],
                ...updates,
                updatedAt: Date.now()
            };
        }

        this.saveLocalCollections(collections);

        // Sync with Backend (Auto-save)
        if (this.backendAvailable) {
            try {
                const res = await fetch(`${API_BASE}/api/collections/${encodeURIComponent(collectionId)}/bhajans/${encodeURIComponent(bhajanId)}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updates)
                });
                return res.ok;
            } catch (e) {
                console.warn('Backend sync failed on updateBhajan', e);
                return false;
            }
        }

        return true;
    }

    async deleteBhajan(collectionId, bhajanId) {
        const collections = this.getCollections();
        const collection = collections.find(c => c.id === collectionId);
        if (!collection || !collection.bhajans) return false;

        const originalLength = collection.bhajans.length;
        collection.bhajans = collection.bhajans.filter(b => b.id !== bhajanId);
        if (collection.bhajans.length !== originalLength) {
            this.saveLocalCollections(collections);

            // Sync with Backend
            if (this.backendAvailable) {
                try {
                    await fetch(`${API_BASE}/api/collections/${encodeURIComponent(collectionId)}/bhajans/${encodeURIComponent(bhajanId)}`, {
                        method: 'DELETE'
                    });
                } catch (e) {
                    console.warn('Backend sync failed on deleteBhajan', e);
                }
            }
            return true;
        }
        return false;
    }

    // --- Search ---
    search(query) {
        if (!query || !query.trim()) {
            return { collections: this.getCollections(), matchingBhajans: [] };
        }

        const q = query.trim().toLowerCase();
        const allCollections = this.getCollections();

        const filteredCollections = [];
        const matchingBhajans = [];

        allCollections.forEach(col => {
            const colNameMatch = col.name.toLowerCase().includes(q) || 
                                (col.subtitle && col.subtitle.toLowerCase().includes(q));

            const matchedBhajansInCol = (col.bhajans || []).filter(b => 
                b.title.toLowerCase().includes(q) || 
                (b.content && b.content.toLowerCase().includes(q))
            );

            if (colNameMatch || matchedBhajansInCol.length > 0) {
                filteredCollections.push(col);
            }

            matchedBhajansInCol.forEach(b => {
                matchingBhajans.push({
                    ...b,
                    collectionId: col.id,
                    collectionName: col.name,
                    collectionIcon: col.icon
                });
            });
        });

        return {
            collections: filteredCollections,
            matchingBhajans: matchingBhajans
        };
    }
}

// Global instance
window.bhajanStorage = new StorageManager();
