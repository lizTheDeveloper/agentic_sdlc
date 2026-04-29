// Component Rendering Functions

function renderStats(stats) {
    document.getElementById('totalVendors').textContent = stats.total_vendors;
    document.getElementById('highRiskCount').textContent = stats.high_risk_count;
    document.getElementById('mediumRiskCount').textContent = stats.medium_risk_count;
    document.getElementById('lowRiskCount').textContent = stats.low_risk_count;
    document.getElementById('avgRiskScore').textContent = stats.average_risk_score.toFixed(1);
}

function renderVendorCard(vendor) {
    const card = document.createElement('div');
    card.className = `vendor-card rating-${vendor.rating}`;
    card.dataset.vendorId = vendor.id;
    card.dataset.rating = vendor.rating;
    
    const oauthScopes = vendor.oauth_scopes ? vendor.oauth_scopes.split(',') : [];
    const complianceCerts = vendor.compliance_certs ? vendor.compliance_certs.split(',') : [];
    
    card.innerHTML = `
        <div class="vendor-card-header">
            <div>
                <div class="vendor-name">${escapeHtml(vendor.name)}</div>
                <div class="vendor-detail-item">${escapeHtml(vendor.data_access_level)}</div>
            </div>
            <span class="vendor-rating">${getRatingLabel(vendor.rating)}</span>
        </div>
        <div class="vendor-score">${vendor.risk_score}</div>
        <div class="vendor-details">
            ${oauthScopes.length > 0 ? `
                <div class="vendor-detail-item">
                    <strong>OAuth:</strong> ${oauthScopes.map(escapeHtml).join(', ')}
                </div>
            ` : ''}
            ${complianceCerts.length > 0 ? `
                <div class="vendor-detail-item">
                    <strong>Certs:</strong> ${complianceCerts.map(escapeHtml).join(', ')}
                </div>
            ` : ''}
        </div>
    `;
    
    return card;
}

function renderVendorGrid(vendors, filter = 'all', searchQuery = '') {
    const grid = document.getElementById('vendorGrid');
    grid.innerHTML = '';
    
    let filteredVendors = vendors;
    
    // Apply rating filter
    if (filter !== 'all') {
        filteredVendors = filteredVendors.filter(v => v.rating === filter);
    }
    
    // Apply search filter
    if (searchQuery) {
        const query = searchQuery.toLowerCase();
        filteredVendors = filteredVendors.filter(v => 
            v.name.toLowerCase().includes(query) ||
            v.data_access_level.toLowerCase().includes(query) ||
            (v.oauth_scopes && v.oauth_scopes.toLowerCase().includes(query)) ||
            (v.compliance_certs && v.compliance_certs.toLowerCase().includes(query))
        );
    }
    
    if (filteredVendors.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <h3>No vendors found</h3>
                <p>${vendors.length === 0 ? 'Add your first vendor to get started' : 'Try adjusting your filters'}</p>
            </div>
        `;
        return;
    }
    
    filteredVendors.forEach(vendor => {
        const card = renderVendorCard(vendor);
        grid.appendChild(card);
    });
}

function renderDetailPanel(vendor) {
    const oauthScopes = vendor.oauth_scopes ? vendor.oauth_scopes.split(',') : [];
    const complianceCerts = vendor.compliance_certs ? vendor.compliance_certs.split(',') : [];
    
    const content = document.getElementById('detailPanelContent');
    content.innerHTML = `
        <div class="detail-panel-header">
            <div class="detail-panel-name">${escapeHtml(vendor.name)}</div>
            <div class="detail-panel-score rating-${vendor.rating}">${vendor.risk_score}</div>
            <div style="margin-top: 10px;">
                <span class="tag rating-${vendor.rating}">${getRatingLabel(vendor.rating)}</span>
            </div>
        </div>
        
        <div class="detail-panel-section">
            <h3>Data Access</h3>
            <div class="detail-panel-info">
                <div class="detail-panel-row">
                    <span>Access Level</span>
                    <strong>${escapeHtml(vendor.data_access_level)}</strong>
                </div>
            </div>
        </div>
        
        <div class="detail-panel-section">
            <h3>OAuth Scopes</h3>
            <div class="detail-panel-info">
                ${oauthScopes.length > 0 ? `
                    <div class="tag-list">
                        ${oauthScopes.map(scope => `<span class="tag">${escapeHtml(scope)}</span>`).join('')}
                    </div>
                ` : '<p>No OAuth scopes configured</p>'}
            </div>
        </div>
        
        <div class="detail-panel-section">
            <h3>Compliance Certifications</h3>
            <div class="detail-panel-info">
                ${complianceCerts.length > 0 ? `
                    <div class="tag-list">
                        ${complianceCerts.map(cert => `<span class="tag compliance">${escapeHtml(cert)}</span>`).join('')}
                    </div>
                ` : '<p>No compliance certifications</p>'}
            </div>
        </div>
        
        <div class="detail-panel-section">
            <h3>Risk Breakdown</h3>
            <div class="detail-panel-info">
                <div class="risk-breakdown">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span>Overall Risk</span>
                        <strong>${vendor.risk_score}/100</strong>
                    </div>
                    <div class="risk-bar">
                        <div class="risk-bar-fill ${vendor.rating}" style="width: ${vendor.risk_score}%"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="detail-panel-section">
            <button class="btn btn-primary" onclick="app.editVendor(${vendor.id})" style="width: 100%; margin-bottom: 10px;">
                Edit Vendor
            </button>
            <button class="btn btn-secondary" onclick="app.deleteVendor(${vendor.id})" style="width: 100%;">
                Delete Vendor
            </button>
        </div>
    `;
}

function updateRiskPreview() {
    const dataAccessLevel = document.getElementById('dataAccessLevel').value;
    const oauthScopes = Array.from(document.querySelectorAll('input[name="oauthScope"]:checked'))
        .map(cb => cb.value);
    const complianceCerts = Array.from(document.querySelectorAll('input[name="complianceCert"]:checked'))
        .map(cb => cb.value);
    
    if (!dataAccessLevel) {
        document.getElementById('previewScore').textContent = '0';
        document.getElementById('previewRating').textContent = '-';
        document.getElementById('previewRating').className = 'score-rating';
        return;
    }
    
    const score = calculateRiskScore(dataAccessLevel, oauthScopes, complianceCerts);
    const rating = getRating(score);
    
    document.getElementById('previewScore').textContent = score;
    document.getElementById('previewRating').textContent = getRatingLabel(rating);
    document.getElementById('previewRating').className = `score-rating ${rating}`;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
