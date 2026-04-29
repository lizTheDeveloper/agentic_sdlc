// Main Application Logic
const app = {
    vendors: [],
    currentFilter: 'all',
    searchQuery: '',
    editingVendorId: null,

    async init() {
        this.bindEvents();
        await this.loadVendors();
        await this.loadStats();
    },

    bindEvents() {
        // Add vendor button
        document.getElementById('addVendorBtn').addEventListener('click', () => this.openModal());

        // Modal close buttons
        document.getElementById('modalClose').addEventListener('click', () => this.closeModal());
        document.getElementById('cancelBtn').addEventListener('click', () => this.closeModal());
        document.getElementById('modalOverlay').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) this.closeModal();
        });

        // Detail panel close
        document.getElementById('detailPanelClose').addEventListener('click', () => this.closeDetailPanel());
        document.getElementById('detailPanelOverlay').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) this.closeDetailPanel();
        });

        // Form submit
        document.getElementById('vendorForm').addEventListener('submit', (e) => this.handleFormSubmit(e));

        // Live risk preview updates
        document.getElementById('dataAccessLevel').addEventListener('change', updateRiskPreview);
        document.querySelectorAll('input[name="oauthScope"]').forEach(cb => {
            cb.addEventListener('change', updateRiskPreview);
        });
        document.querySelectorAll('input[name="complianceCert"]').forEach(cb => {
            cb.addEventListener('change', updateRiskPreview);
        });

        // Search input
        document.getElementById('searchInput').addEventListener('input', (e) => {
            this.searchQuery = e.target.value;
            this.renderVendors();
        });

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentFilter = e.target.dataset.filter;
                this.renderVendors();
            });
        });

        // Vendor card clicks (event delegation)
        document.getElementById('vendorGrid').addEventListener('click', (e) => {
            const card = e.target.closest('.vendor-card');
            if (card) {
                this.showVendorDetail(parseInt(card.dataset.vendorId));
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
                this.closeDetailPanel();
            }
        });
    },

    async loadVendors() {
        try {
            this.vendors = await fetchVendors();
            this.renderVendors();
        } catch (error) {
            console.error('Failed to load vendors:', error);
            alert('Failed to load vendors. Make sure the backend is running.');
        }
    },

    async loadStats() {
        try {
            const stats = await fetchStats();
            renderStats(stats);
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    },

    renderVendors() {
        renderVendorGrid(this.vendors, this.currentFilter, this.searchQuery);
    },

    openModal(vendor = null) {
        const modal = document.getElementById('modalOverlay');
        const title = document.getElementById('modalTitle');
        const form = document.getElementById('vendorForm');

        form.reset();
        this.editingVendorId = null;

        if (vendor) {
            // Edit mode
            title.textContent = 'Edit Vendor';
            this.editingVendorId = vendor.id;

            document.getElementById('vendorId').value = vendor.id;
            document.getElementById('vendorName').value = vendor.name;
            document.getElementById('dataAccessLevel').value = vendor.data_access_level;

            // Set OAuth scopes
            const oauthScopes = vendor.oauth_scopes ? vendor.oauth_scopes.split(',') : [];
            document.querySelectorAll('input[name="oauthScope"]').forEach(cb => {
                cb.checked = oauthScopes.includes(cb.value);
            });

            // Set compliance certs
            const complianceCerts = vendor.compliance_certs ? vendor.compliance_certs.split(',') : [];
            document.querySelectorAll('input[name="complianceCert"]').forEach(cb => {
                cb.checked = complianceCerts.includes(cb.value);
            });
        } else {
            // Add mode
            title.textContent = 'Add New Vendor';
        }

        updateRiskPreview();
        modal.classList.add('active');
    },

    closeModal() {
        document.getElementById('modalOverlay').classList.remove('active');
    },

    async handleFormSubmit(e) {
        e.preventDefault();

        const name = document.getElementById('vendorName').value.trim();
        const dataAccessLevel = document.getElementById('dataAccessLevel').value;
        const oauthScopes = Array.from(document.querySelectorAll('input[name="oauthScope"]:checked'))
            .map(cb => cb.value);
        const complianceCerts = Array.from(document.querySelectorAll('input[name="complianceCert"]:checked'))
            .map(cb => cb.value);

        const vendorData = {
            name,
            data_access_level: dataAccessLevel,
            oauth_scopes: oauthScopes,
            compliance_certs: complianceCerts
        };

        try {
            if (this.editingVendorId) {
                await updateVendor(this.editingVendorId, vendorData);
            } else {
                await createVendor(vendorData);
            }

            this.closeModal();
            await this.loadVendors();
            await this.loadStats();
        } catch (error) {
            console.error('Failed to save vendor:', error);
            alert(`Failed to save vendor: ${error.message}`);
        }
    },

    async showVendorDetail(id) {
        try {
            const vendor = await fetchVendor(id);
            renderDetailPanel(vendor);
            document.getElementById('detailPanelOverlay').classList.add('active');
        } catch (error) {
            console.error('Failed to load vendor details:', error);
            alert('Failed to load vendor details.');
        }
    },

    closeDetailPanel() {
        document.getElementById('detailPanelOverlay').classList.remove('active');
    },

    editVendor(id) {
        const vendor = this.vendors.find(v => v.id === id);
        if (vendor) {
            this.closeDetailPanel();
            setTimeout(() => this.openModal(vendor), 300);
        }
    },

    async deleteVendor(id) {
        if (!confirm('Are you sure you want to delete this vendor? This action cannot be undone.')) {
            return;
        }

        try {
            await deleteVendor(id);
            this.closeDetailPanel();
            await this.loadVendors();
            await this.loadStats();
        } catch (error) {
            console.error('Failed to delete vendor:', error);
            alert('Failed to delete vendor.');
        }
    }
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => app.init());
