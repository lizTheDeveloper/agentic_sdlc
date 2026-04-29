// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// API Functions
async function fetchStats() {
    const response = await fetch(`${API_BASE_URL}/stats`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return await response.json();
}

async function fetchVendors() {
    const response = await fetch(`${API_BASE_URL}/vendors`);
    if (!response.ok) throw new Error('Failed to fetch vendors');
    return await response.json();
}

async function fetchVendor(id) {
    const response = await fetch(`${API_BASE_URL}/vendors/${id}`);
    if (!response.ok) throw new Error('Failed to fetch vendor');
    return await response.json();
}

async function createVendor(vendorData) {
    const response = await fetch(`${API_BASE_URL}/vendors`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(vendorData)
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create vendor');
    }
    return await response.json();
}

async function updateVendor(id, vendorData) {
    const response = await fetch(`${API_BASE_URL}/vendors/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(vendorData)
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to update vendor');
    }
    return await response.json();
}

async function deleteVendor(id) {
    const response = await fetch(`${API_BASE_URL}/vendors/${id}`, {
        method: 'DELETE'
    });
    if (!response.ok) throw new Error('Failed to delete vendor');
    return await response.json();
}

// Risk Calculation (client-side for preview)
function calculateRiskScore(dataAccessLevel, oauthScopes, complianceCerts) {
    const dataAccessPoints = {
        'none': 0,
        'read-only': 15,
        'read-write': 30,
        'admin': 40
    };

    const oauthPoints = {
        'email': 5,
        'profile': 8,
        'files': 15,
        'write': 20,
        'admin': 35
    };

    const complianceReductions = {
        'SOC2': -5,
        'ISO27001': -5,
        'GDPR': -8,
        'HIPAA': -10
    };

    const dataScore = dataAccessPoints[dataAccessLevel] || 0;
    const oauthScore = oauthScopes.reduce((sum, scope) => sum + (oauthPoints[scope] || 0), 0);
    const complianceScore = complianceCerts.reduce((sum, cert) => sum + (complianceReductions[cert] || 0), 0);

    let finalScore = dataScore + oauthScore + complianceScore;
    finalScore = Math.max(0, Math.min(100, finalScore));

    return finalScore;
}

function getRating(score) {
    if (score <= 30) return 'green';
    if (score <= 60) return 'amber';
    return 'red';
}

function getRatingLabel(rating) {
    const labels = {
        'green': 'Low Risk',
        'amber': 'Medium Risk',
        'red': 'High Risk'
    };
    return labels[rating] || rating;
}
