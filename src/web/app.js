/**
 * Resume Editor Application
 *
 * Main JavaScript application for managing master_resume.json
 * Related to GitHub Issues #2 and #6
 */

// Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Global state
let resumeData = null;
let currentResumeId = null;
let currentSection = 'basic-info';
let hasUnsavedChanges = false;

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

async function initializeApp() {
    try {
        // Check if a specific resume ID is provided in URL
        const urlParams = new URLSearchParams(window.location.search);
        currentResumeId = urlParams.get('resume');

        // Load resume data
        await loadResumeData();

        // Setup event listeners
        setupEventListeners();
        document.getElementById('generateDocxBtn').addEventListener('click', async () => {
            try {
                showAlert('Generating DOCX, please wait...', 'info');

                // Prepare request based on whether we're editing a specific resume
                let fetchOptions = {};
                if (currentResumeId) {
                    // Send POST request with resume ID
                    fetchOptions = {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ resume_id: currentResumeId })
                    };
                }

                const response = await fetch(`${API_BASE_URL}/resume/docx`, fetchOptions);
                if (!response.ok) {
                    let errorMsg = 'Failed to generate DOCX';
                    try {
                        const errorData = await response.json();
                        errorMsg = errorData.error || errorMsg;
                    } catch {}
                    throw new Error(errorMsg);
                }
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'resume.docx';
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                showAlert('DOCX generated and downloaded!', 'success', 3000);
            } catch (err) {
                showAlert('Failed to generate DOCX: ' + err.message, 'danger');
            }
        });

        // Render initial view
        renderAllSections();

        // Hide loading spinner
        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('contentArea').style.display = 'block';

        showAlert('Resume loaded successfully!', 'success', 3000);
    } catch (error) {
        console.error('Failed to initialize app:', error);
        showAlert('Failed to load resume data. Please check if the API server is running.', 'danger');
    }
}

// API Functions
async function loadResumeData() {
    let endpoint = `${API_BASE_URL}/resume`;

    // If a specific resume ID is provided, load that resume
    if (currentResumeId) {
        endpoint = `${API_BASE_URL}/resumes/${currentResumeId}`;
    }

    const response = await fetch(endpoint);
    if (!response.ok) {
        throw new Error('Failed to load resume data');
    }
    const result = await response.json();
    resumeData = result.data;
}

async function saveResumeData() {
    try {
        // Collect data from form
        collectFormData();

        // Validate before saving
        const validationResult = await validateResumeData(resumeData);
        if (!validationResult.valid) {
            showAlert(`Validation failed: ${validationResult.errors.join(', ')}`, 'danger');
            return;
        }

        // Determine endpoint based on whether we're editing a specific resume
        let endpoint = `${API_BASE_URL}/resume`;
        let method = 'PUT';
        let body = JSON.stringify(resumeData);

        if (currentResumeId) {
            endpoint = `${API_BASE_URL}/resumes/${currentResumeId}`;
            body = JSON.stringify({ data: resumeData });
        }

        // Save to API
        const response = await fetch(endpoint, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: body
        });

        if (!response.ok) {
            throw new Error('Failed to save resume data');
        }

        const result = await response.json();
        hasUnsavedChanges = false;

        const message = result.backup
            ? `Resume saved successfully! Backup created: ${result.backup}`
            : 'Resume saved successfully!';
        showAlert(message, 'success', 5000);
    } catch (error) {
        console.error('Failed to save resume:', error);
        showAlert('Failed to save resume data. Please try again.', 'danger');
    }
}

async function validateResumeData(data) {
    try {
        const response = await fetch(`${API_BASE_URL}/resume/validate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        return await response.json();
    } catch (error) {
        console.error('Validation error:', error);
        return { valid: false, errors: ['Validation request failed'] };
    }
}

async function createBackup() {
    try {
        const response = await fetch(`${API_BASE_URL}/resume/backup`, {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error('Failed to create backup');
        }

        const result = await response.json();
        showAlert(`Backup created successfully: ${result.backup}`, 'success', 5000);
    } catch (error) {
        console.error('Failed to create backup:', error);
        showAlert('Failed to create backup. Please try again.', 'danger');
    }
}

async function loadBackups() {
    try {
        const response = await fetch(`${API_BASE_URL}/resume/backups`);
        if (!response.ok) {
            throw new Error('Failed to load backups');
        }

        const result = await response.json();
        return result.backups;
    } catch (error) {
        console.error('Failed to load backups:', error);
        return [];
    }
}

async function restoreBackup(filename) {
    try {
        const response = await fetch(`${API_BASE_URL}/resume/restore`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename })
        });

        if (!response.ok) {
            throw new Error('Failed to restore backup');
        }

        const result = await response.json();
        showAlert(`Resume restored from ${filename}. Reloading...`, 'success', 3000);

        // Reload the page after a short delay
        setTimeout(() => {
            window.location.reload();
        }, 2000);
    } catch (error) {
        console.error('Failed to restore backup:', error);
        showAlert('Failed to restore backup. Please try again.', 'danger');
    }
}

// Event Listeners Setup
function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.list-group-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const section = item.getAttribute('data-section');
            navigateToSection(section);
        });
    });

    // Save button
    document.getElementById('saveBtn').addEventListener('click', saveResumeData);

    // Backup button
    document.getElementById('backupBtn').addEventListener('click', createBackup);

    // View backups button
    document.getElementById('viewBackupsBtn').addEventListener('click', showBackupsModal);

    // Add buttons
    document.getElementById('addExperienceBtn').addEventListener('click', () => addExperienceEntry());
    document.getElementById('addEducationBtn').addEventListener('click', () => addEducationEntry());
    document.getElementById('addCertificationBtn').addEventListener('click', () => addCertificationEntry());
    document.getElementById('addExpertiseBtn').addEventListener('click', () => addExpertiseItem());

    // Track changes
    document.addEventListener('input', () => {
        hasUnsavedChanges = true;
    });

    // Warn before leaving with unsaved changes
    window.addEventListener('beforeunload', (e) => {
        if (hasUnsavedChanges) {
            e.preventDefault();
            e.returnValue = '';
        }
    });
}

// Navigation
function navigateToSection(sectionId) {
    // Update active state in sidebar
    document.querySelectorAll('.list-group-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelector(`[data-section="${sectionId}"]`).classList.add('active');

    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });

    // Show selected section
    document.getElementById(sectionId).style.display = 'block';
    currentSection = sectionId;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Collect form data
function collectFormData() {
    // Basic info
    resumeData.name = document.getElementById('name').value;
    resumeData.title = document.getElementById('title').value;
    resumeData.location = document.getElementById('location').value;
    resumeData.contact.email = document.getElementById('email').value;
    resumeData.contact.phone = document.getElementById('phone').value;

    // Summary
    resumeData.summary = document.getElementById('summaryText').value;

    // Technical proficiencies
    collectTechnicalProficiencies();

    // Areas of expertise
    collectAreasOfExpertise();

    // Experience, Education, Certifications are collected in real-time
}

// Render functions
function renderAllSections() {
    renderBasicInfo();
    renderSummary();
    renderTechnicalProficiencies();
    renderAreasOfExpertise();
    renderExperience();
    renderEducation();
    renderCertifications();
}

function renderBasicInfo() {
    document.getElementById('name').value = resumeData.name || '';
    document.getElementById('title').value = resumeData.title || '';
    document.getElementById('location').value = resumeData.location || '';
    document.getElementById('email').value = resumeData.contact?.email || '';
    document.getElementById('phone').value = resumeData.contact?.phone || '';
}

function renderSummary() {
    document.getElementById('summaryText').value = resumeData.summary || '';
}

function renderTechnicalProficiencies() {
    const container = document.getElementById('technicalProficienciesContainer');
    container.innerHTML = '';

    if (!resumeData.technical_proficiencies) {
        resumeData.technical_proficiencies = {};
    }

    for (const [category, skills] of Object.entries(resumeData.technical_proficiencies)) {
        const categoryDiv = document.createElement('div');
        categoryDiv.className = 'tech-category mb-3';
        categoryDiv.innerHTML = `
            <label class="form-label tech-category-label">${category}</label>
            <textarea class="form-control" data-tech-category="${category}" rows="2">${skills}</textarea>
        `;
        container.appendChild(categoryDiv);
    }
}

function collectTechnicalProficiencies() {
    const textareas = document.querySelectorAll('[data-tech-category]');
    resumeData.technical_proficiencies = {};
    textareas.forEach(textarea => {
        const category = textarea.getAttribute('data-tech-category');
        resumeData.technical_proficiencies[category] = textarea.value;
    });
}

function renderAreasOfExpertise() {
    const container = document.getElementById('expertiseContainer');
    container.innerHTML = '';

    if (!resumeData.areas_of_expertise) {
        resumeData.areas_of_expertise = [];
    }

    resumeData.areas_of_expertise.forEach((expertise, index) => {
        const expertiseDiv = createExpertiseItem(expertise, index);
        container.appendChild(expertiseDiv);
    });
}

function createExpertiseItem(value, index) {
    const div = document.createElement('div');
    div.className = 'expertise-item';
    div.innerHTML = `
        <input type="text" class="form-control" value="${value}" data-expertise-index="${index}">
        <button class="btn btn-sm btn-outline-danger" onclick="removeExpertiseItem(${index})">
            <i class="bi bi-trash"></i>
        </button>
    `;
    return div;
}

function addExpertiseItem() {
    if (!resumeData.areas_of_expertise) {
        resumeData.areas_of_expertise = [];
    }
    resumeData.areas_of_expertise.push('');
    renderAreasOfExpertise();
}

function removeExpertiseItem(index) {
    resumeData.areas_of_expertise.splice(index, 1);
    renderAreasOfExpertise();
}

function collectAreasOfExpertise() {
    const inputs = document.querySelectorAll('[data-expertise-index]');
    resumeData.areas_of_expertise = Array.from(inputs).map(input => input.value).filter(v => v.trim());
}

function renderExperience() {
    const container = document.getElementById('experienceContainer');
    container.innerHTML = '';

    if (!resumeData.experience) {
        resumeData.experience = [];
    }

    // Sort by start date (descending)
    const parseStartYear = exp => {
        if (!exp.dates) return 0;
        // Expect format like "2017 – 2024" or "2016 – 2017"
        const match = exp.dates.match(/(\d{4})/);
        return match ? parseInt(match[1], 10) : 0;
    };
    const sortedExperience = resumeData.experience
        .slice()
        .sort((a, b) => parseStartYear(b) - parseStartYear(a));
    sortedExperience.forEach((exp) => {
        const index = resumeData.experience.findIndex(e => (e.employer + '_' + e.dates) === (exp.employer + '_' + exp.dates));
        const expKey = exp.employer + '_' + exp.dates;
        const expCard = createExperienceCard(exp, index, expKey);
        container.appendChild(expCard);
    });
}

function createExperienceCard(exp, index, expKey) {
    const card = document.createElement('div');
    card.className = 'card experience-card';

    const bulletsHtml = (exp.bullets || []).map((bullet, bIndex) => {
        const tagsHtml = (bullet.tags || []).map(tag =>
            `<span class="tag-badge">${tag} <span class="remove-tag" onclick="removeTag(${index}, ${bIndex}, '${tag}')">×</span></span>`
        ).join('');

        return `
            <div class="bullet-item" data-exp-index="${index}" data-bullet-index="${bIndex}">
                <textarea class="form-control bullet-text" rows="3">${bullet.text || ''}</textarea>
                <div class="bullet-tags mt-2">
                    ${tagsHtml}
                    <button class="btn btn-sm btn-outline-primary" onclick="addTag(${index}, ${bIndex})">
                        <i class="bi bi-plus"></i> Add Tag
                    </button>
                </div>
                <button class="btn btn-sm btn-outline-danger mt-2" onclick="removeBullet(${index}, ${bIndex})">
                    <i class="bi bi-trash"></i> Remove Bullet
                </button>
            </div>
        `;
    }).join('');

    card.innerHTML = `
        <div class="card-header">
            <h5 class="card-title">${exp.employer || 'New Experience'}</h5>
            <div class="btn-group">
                <button class="btn btn-sm btn-outline-danger" onclick="removeExperience('${expKey}')">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </div>
        </div>
        <div class="card-body">
            <div class="row mb-3">
                <div class="col-md-6">
                    <label class="form-label">Employer</label>
                    <input type="text" class="form-control" value="${exp.employer || ''}"
                           onchange="updateExperience(${index}, 'employer', this.value)">
                </div>
                <div class="col-md-6">
                    <label class="form-label">Location</label>
                    <input type="text" class="form-control" value="${exp.location || ''}"
                           onchange="updateExperience(${index}, 'location', this.value)">
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-md-6">
                    <label class="form-label">Role</label>
                    <input type="text" class="form-control" value="${exp.role || ''}"
                           onchange="updateExperience(${index}, 'role', this.value)">
                </div>
                <div class="col-md-6">
                    <label class="form-label">Dates</label>
                    <input type="text" class="form-control" value="${exp.dates || ''}"
                           onchange="updateExperience(${index}, 'dates', this.value)">
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label">Accomplishments</label>
                ${bulletsHtml}
                <button class="btn btn-sm btn-outline-primary mt-2" onclick="addBullet(${index})">
                    <i class="bi bi-plus-circle"></i> Add Accomplishment
                </button>
            </div>
        </div>
    `;

    return card;
}


function addExperienceEntry() {
    if (!resumeData.experience) {
        resumeData.experience = [];
    }
    resumeData.experience.push({
        employer: '',
        location: '',
        role: '',
        dates: '',
        bullets: []
    });
    renderExperience();
    // Scroll to the new entry
    setTimeout(() => {
        const cards = document.querySelectorAll('.experience-card');
        cards[cards.length - 1].scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
}

function removeExperience(index) {
    if (confirm('Are you sure you want to delete this experience entry?')) {
        const idx = resumeData.experience.findIndex(exp => (exp.employer + '_' + exp.dates) === index);
        if (idx !== -1) {
            resumeData.experience.splice(idx, 1);
            renderExperience();
        }
    }
}

function updateExperience(index, field, value) {
    resumeData.experience[index][field] = value;
}

function addBullet(expIndex) {
    if (!resumeData.experience[expIndex].bullets) {
        resumeData.experience[expIndex].bullets = [];
    }
    resumeData.experience[expIndex].bullets.push({ text: '', tags: [] });
    renderExperience();
}

function removeBullet(expIndex, bulletIndex) {
    resumeData.experience[expIndex].bullets.splice(bulletIndex, 1);
    renderExperience();
}

function addTag(expIndex, bulletIndex) {
    const tag = prompt('Enter tag name:');
    if (tag && tag.trim()) {
        if (!resumeData.experience[expIndex].bullets[bulletIndex].tags) {
            resumeData.experience[expIndex].bullets[bulletIndex].tags = [];
        }
        resumeData.experience[expIndex].bullets[bulletIndex].tags.push(tag.trim());
        renderExperience();
    }
}

function removeTag(expIndex, bulletIndex, tag) {
    const bullet = resumeData.experience[expIndex].bullets[bulletIndex];
    bullet.tags = bullet.tags.filter(t => t !== tag);
    renderExperience();
}

// Update bullet text when changed
document.addEventListener('change', (e) => {
    if (e.target.classList.contains('bullet-text')) {
        const bulletItem = e.target.closest('.bullet-item');
        const expIndex = parseInt(bulletItem.getAttribute('data-exp-index'));
        const bulletIndex = parseInt(bulletItem.getAttribute('data-bullet-index'));
        resumeData.experience[expIndex].bullets[bulletIndex].text = e.target.value;
    }
});

function renderEducation() {
    const container = document.getElementById('educationContainer');
    container.innerHTML = '';

    if (!resumeData.education) {
        resumeData.education = [];
    }

    resumeData.education.forEach((edu, index) => {
        const eduCard = createEducationCard(edu, index);
        container.appendChild(eduCard);
    });
}

function createEducationCard(edu, index) {
    const card = document.createElement('div');
    card.className = 'card education-card';

    card.innerHTML = `
        <div class="card-header">
            <h5 class="card-title">${edu.institution || 'New Education'}</h5>
            <button class="btn btn-sm btn-outline-danger" onclick="removeEducation(${index})">
                <i class="bi bi-trash"></i> Delete
            </button>
        </div>
        <div class="card-body">
            <div class="row mb-3">
                <div class="col-md-6">
              <label class="form-label">Institution</label>
              <input type="text" class="form-control" value="${edu.institution || ''}"
                  onchange="updateEducation(${index}, 'institution', this.value)">
                </div>
                <div class="col-md-6">
                    <label class="form-label">Degree</label>
                    <input type="text" class="form-control" value="${edu.degree || ''}"
                           onchange="updateEducation(${index}, 'degree', this.value)">
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-md-6">
                    <label class="form-label">Year</label>
                    <input type="text" class="form-control" value="${edu.year || ''}"
                           onchange="updateEducation(${index}, 'year', this.value)">
                </div>
                <div class="col-md-6">
                    <label class="form-label">Location (Optional)</label>
                    <input type="text" class="form-control" value="${edu.location || ''}"
                           onchange="updateEducation(${index}, 'location', this.value)">
                </div>
            </div>
        </div>
    `;

    return card;
}

function addEducationEntry() {
    if (!resumeData.education) {
        resumeData.education = [];
    }
    resumeData.education.push({
        institution: 'Institution Name',
        degree: '',
        year: ''
    });
    renderEducation();
}

function removeEducation(index) {
    if (confirm('Are you sure you want to delete this education entry?')) {
        resumeData.education.splice(index, 1);
        renderEducation();
    }
}

function updateEducation(index, field, value) {
    resumeData.education[index][field] = value;
}

function renderCertifications() {
    const container = document.getElementById('certificationsContainer');
    container.innerHTML = '';

    if (!resumeData.certifications) {
        resumeData.certifications = [];
    }

    if (resumeData.certifications.length === 0) {
        container.innerHTML = '<p class="text-muted">No certifications added yet.</p>';
        return;
    }

    resumeData.certifications.forEach((cert, index) => {
        const certCard = createCertificationCard(cert, index);
        container.appendChild(certCard);
    });
}

function createCertificationCard(cert, index) {
    const card = document.createElement('div');
    card.className = 'card certification-card';

    // Handle both string and object formats
    const certName = typeof cert === 'string' ? cert : (cert.name || '');
    const certIssuer = typeof cert === 'object' ? (cert.issuer || '') : '';
    const certYear = typeof cert === 'object' ? (cert.year || '') : '';

    card.innerHTML = `
        <div class="card-header">
            <h5 class="card-title">${certName || 'New Certification'}</h5>
            <button class="btn btn-sm btn-outline-danger" onclick="removeCertification(${index})">
                <i class="bi bi-trash"></i> Delete
            </button>
        </div>
        <div class="card-body">
            <div class="row mb-3">
                <div class="col-md-12">
                    <label class="form-label">Certification Name</label>
                    <input type="text" class="form-control" value="${certName}"
                           onchange="updateCertification(${index}, 'name', this.value)">
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-md-6">
                    <label class="form-label">Issuer (Optional)</label>
                    <input type="text" class="form-control" value="${certIssuer}"
                           onchange="updateCertification(${index}, 'issuer', this.value)">
                </div>
                <div class="col-md-6">
                    <label class="form-label">Year (Optional)</label>
                    <input type="text" class="form-control" value="${certYear}"
                           onchange="updateCertification(${index}, 'year', this.value)">
                </div>
            </div>
        </div>
    `;

    return card;
}

function addCertificationEntry() {
    if (!resumeData.certifications) {
        resumeData.certifications = [];
    }
    resumeData.certifications.push({ name: '', issuer: '', year: '' });
    renderCertifications();
}

function removeCertification(index) {
    if (confirm('Are you sure you want to delete this certification?')) {
        resumeData.certifications.splice(index, 1);
        renderCertifications();
    }
}

function updateCertification(index, field, value) {
    if (typeof resumeData.certifications[index] === 'string') {
        resumeData.certifications[index] = { name: resumeData.certifications[index] };
    }
    resumeData.certifications[index][field] = value;
}


// Utility Functions
function showAlert(message, type = 'info', duration = 0) {
    const alertContainer = document.getElementById('alertContainer');
    const alertId = 'alert-' + Date.now();

    const alert = document.createElement('div');
    alert.id = alertId;
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.role = 'alert';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    alertContainer.appendChild(alert);

    // Auto-dismiss after duration
    if (duration > 0) {
        setTimeout(() => {
            const alertElement = document.getElementById(alertId);
            if (alertElement) {
                const bsAlert = new bootstrap.Alert(alertElement);
                bsAlert.close();
            }
        }, duration);
    }

    // Scroll to alert
    alertContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function showBackupsModal() {
    const modal = new bootstrap.Modal(document.getElementById('backupModal'));
    modal.show();

    const container = document.getElementById('backupListContainer');
    container.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div></div>';

    try {
        const backups = await loadBackups();

        if (backups.length === 0) {
            container.innerHTML = '<p class="text-muted">No backups found.</p>';
            return;
        }

        container.innerHTML = '';
        backups.forEach(backup => {
            const backupItem = document.createElement('div');
            backupItem.className = 'backup-item';

            const date = new Date(backup.created);
            const formattedDate = date.toLocaleString();
            const sizeKB = (backup.size / 1024).toFixed(2);

            backupItem.innerHTML = `
                <div class="backup-info">
                    <div class="backup-filename">${backup.filename}</div>
                    <div class="backup-meta">
                        <i class="bi bi-calendar"></i> ${formattedDate} |
                        <i class="bi bi-file-earmark"></i> ${sizeKB} KB
                    </div>
                </div>
                <button class="btn btn-sm btn-primary" onclick="confirmRestore('${backup.filename}')">
                    <i class="bi bi-arrow-counterclockwise"></i> Restore
                </button>
            `;

            container.appendChild(backupItem);
        });
    } catch (error) {
        container.innerHTML = '<p class="text-danger">Failed to load backups.</p>';
    }
}

function confirmRestore(filename) {
    const modal = new bootstrap.Modal(document.getElementById('confirmModal'));
    document.getElementById('confirmModalBody').textContent =
        `Are you sure you want to restore from "${filename}"? This will replace your current resume data. A backup of the current state will be created automatically.`;

    document.getElementById('confirmModalBtn').onclick = () => {
        restoreBackup(filename);
        bootstrap.Modal.getInstance(document.getElementById('confirmModal')).hide();
        bootstrap.Modal.getInstance(document.getElementById('backupModal')).hide();
    };

    modal.show();
}

