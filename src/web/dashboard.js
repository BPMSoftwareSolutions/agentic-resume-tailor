/**
 * Resume Dashboard Application
 *
 * Main JavaScript application for managing multiple resumes and job listings
 * Related to GitHub Issue #6
 */

// Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Global state
let resumes = [];
let jobListings = [];
let currentResumeId = null;

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

async function initializeApp() {
    try {
        // Load data
        await Promise.all([
            loadResumes(),
            loadJobListings()
        ]);

        // Setup event listeners
        setupEventListeners();

        // Update statistics
        updateStatistics();

        showAlert('Dashboard loaded successfully!', 'success', 3000);
    } catch (error) {
        console.error('Failed to initialize dashboard:', error);
        showAlert('Failed to load dashboard data. Please check if the API server is running.', 'danger');
    }
}

function setupEventListeners() {
    // Create resume button
    document.getElementById('createResumeBtn').addEventListener('click', showCreateResumeModal);
    document.getElementById('saveResumeBtn').addEventListener('click', createResume);

    // Create job listing button
    document.getElementById('createJobListingBtn').addEventListener('click', showCreateJobListingModal);
    document.getElementById('saveJobListingBtn').addEventListener('click', createJobListing);

    // Tailor resume button
    document.getElementById('saveTailorBtn').addEventListener('click', tailorResume);

    // RAG options listeners
    document.getElementById('tailorUseRag').addEventListener('change', (e) => {
        const llmCheckbox = document.getElementById('tailorUseLlmRewriting');
        const ragInfo = document.getElementById('ragContextInfo');

        if (e.target.checked) {
            llmCheckbox.disabled = false;
            ragInfo.style.display = 'block';
        } else {
            llmCheckbox.disabled = true;
            llmCheckbox.checked = false;
            ragInfo.style.display = 'none';
        }
    });
}

// ============================================================================
// API Functions
// ============================================================================

async function loadResumes() {
    const response = await fetch(`${API_BASE_URL}/resumes`);
    if (!response.ok) {
        throw new Error('Failed to load resumes');
    }
    const result = await response.json();
    resumes = result.resumes;
    renderResumes();
}

async function loadJobListings() {
    const response = await fetch(`${API_BASE_URL}/job-listings`);
    if (!response.ok) {
        throw new Error('Failed to load job listings');
    }
    const result = await response.json();
    jobListings = result.job_listings;
    renderJobListings();
}

async function createResume() {
    try {
        const name = document.getElementById('resumeName').value.trim();
        const description = document.getElementById('resumeDescription').value.trim();
        const baseResumeId = document.getElementById('baseResume').value;

        if (!name) {
            showAlert('Please enter a resume name', 'warning');
            return;
        }

        let newResume;

        if (baseResumeId) {
            // Duplicate existing resume
            const response = await fetch(`${API_BASE_URL}/resumes/${baseResumeId}/duplicate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name })
            });

            if (!response.ok) throw new Error('Failed to duplicate resume');
            const result = await response.json();
            newResume = result.resume;
        } else {
            // Create new resume from master
            const masterResume = resumes.find(r => r.is_master);
            if (!masterResume) {
                showAlert('No master resume found. Please create one first.', 'danger');
                return;
            }

            // Get master resume data
            const dataResponse = await fetch(`${API_BASE_URL}/resumes/${masterResume.id}`);
            if (!dataResponse.ok) throw new Error('Failed to load master resume');
            const dataResult = await dataResponse.json();

            // Create new resume
            const response = await fetch(`${API_BASE_URL}/resumes`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name,
                    description,
                    data: dataResult.data
                })
            });

            if (!response.ok) throw new Error('Failed to create resume');
            const result = await response.json();
            newResume = result.resume;
        }

        // Close modal and reload
        bootstrap.Modal.getInstance(document.getElementById('createResumeModal')).hide();
        document.getElementById('createResumeForm').reset();
        
        await loadResumes();
        updateStatistics();
        showAlert('Resume created successfully!', 'success');
    } catch (error) {
        console.error('Failed to create resume:', error);
        showAlert('Failed to create resume. Please try again.', 'danger');
    }
}

async function deleteResume(resumeId, resumeName) {
    if (!confirm(`Are you sure you want to delete "${resumeName}"?`)) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/resumes/${resumeId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete resume');

        await loadResumes();
        updateStatistics();
        showAlert('Resume deleted successfully!', 'success');
    } catch (error) {
        console.error('Failed to delete resume:', error);
        showAlert('Failed to delete resume. Please try again.', 'danger');
    }
}

async function exportResumeDocx(resumeId, resumeName) {
    try {
        showAlert('Generating DOCX, please wait...', 'info');

        const response = await fetch(`${API_BASE_URL}/resume/docx`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ resume_id: resumeId })
        });

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
        a.download = `${resumeName}.docx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

        showAlert('DOCX generated and downloaded!', 'success', 3000);
    } catch (error) {
        console.error('Failed to export resume:', error);
        showAlert('Failed to export resume: ' + error.message, 'danger');
    }
}

async function createJobListing() {
    try {
        const title = document.getElementById('jobTitle').value.trim();
        const company = document.getElementById('jobCompany').value.trim();
        const location = document.getElementById('jobLocation').value.trim();
        const url = document.getElementById('jobUrl').value.trim();
        const salary_range = document.getElementById('jobSalary').value.trim();
        const description = document.getElementById('jobDescription').value.trim();

        if (!title || !company || !description) {
            showAlert('Please fill in all required fields', 'warning');
            return;
        }

        const response = await fetch(`${API_BASE_URL}/job-listings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title,
                company,
                location,
                url,
                salary_range,
                description
            })
        });

        if (!response.ok) throw new Error('Failed to create job listing');

        // Close modal and reload
        bootstrap.Modal.getInstance(document.getElementById('createJobListingModal')).hide();
        document.getElementById('createJobListingForm').reset();
        
        await loadJobListings();
        updateStatistics();
        showAlert('Job listing added successfully!', 'success');
    } catch (error) {
        console.error('Failed to create job listing:', error);
        showAlert('Failed to create job listing. Please try again.', 'danger');
    }
}

async function deleteJobListing(jobId, jobTitle) {
    if (!confirm(`Are you sure you want to delete "${jobTitle}"?`)) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/job-listings/${jobId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete job listing');

        await loadJobListings();
        updateStatistics();
        showAlert('Job listing deleted successfully!', 'success');
    } catch (error) {
        console.error('Failed to delete job listing:', error);
        showAlert('Failed to delete job listing. Please try again.', 'danger');
    }
}

async function tailorResume() {
    try {
        const sourceResumeId = document.getElementById('tailorSourceResumeId').value;
        const jobListingId = document.getElementById('tailorJobListing').value;
        const newResumeName = document.getElementById('tailorResumeName').value.trim();
        const useRag = document.getElementById('tailorUseRag').checked;
        const useLlmRewriting = document.getElementById('tailorUseLlmRewriting').checked;

        if (!jobListingId || !newResumeName) {
            showAlert('Please fill in all required fields', 'warning');
            return;
        }

        // Show loading indicator
        const tailorBtn = document.getElementById('saveTailorBtn');
        const originalText = tailorBtn.innerHTML;
        tailorBtn.disabled = true;
        tailorBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Tailoring...';

        const response = await fetch(`${API_BASE_URL}/resumes/${sourceResumeId}/tailor`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                job_listing_id: jobListingId,
                new_resume_name: newResumeName,
                use_rag: useRag,
                use_llm_rewriting: useLlmRewriting
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to tailor resume');
        }

        const result = await response.json();

        // Close modal and reload
        bootstrap.Modal.getInstance(document.getElementById('tailorResumeModal')).hide();
        document.getElementById('tailorResumeForm').reset();

        await loadResumes();
        updateStatistics();

        // Show success message with RAG info if applicable
        let message = 'Resume tailored successfully!';
        if (result.rag_enabled) {
            message += ` (RAG: ${result.rag_context?.total_documents_retrieved || 0} documents retrieved)`;
        }
        showAlert(message, 'success');
    } catch (error) {
        console.error('Failed to tailor resume:', error);
        showAlert(`Failed to tailor resume: ${error.message}`, 'danger');
    } finally {
        // Restore button state
        const tailorBtn = document.getElementById('saveTailorBtn');
        tailorBtn.disabled = false;
        tailorBtn.innerHTML = '<i class="bi bi-magic"></i> Tailor Resume';
    }
}

// ============================================================================
// Render Functions
// ============================================================================

function renderResumes() {
    const container = document.getElementById('resumesContainer');
    const loading = document.getElementById('loadingResumes');

    loading.style.display = 'none';
    container.style.display = 'flex';

    if (resumes.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="bi bi-file-earmark-text" style="font-size: 4rem; color: #ccc;"></i>
                <p class="text-muted mt-3">No resumes yet. Create your first resume to get started!</p>
            </div>
        `;
        return;
    }

    container.innerHTML = resumes.map(resume => `
        <div class="col-md-6 col-lg-4">
            <div class="card resume-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h5 class="card-title mb-0">${escapeHtml(resume.name)}</h5>
                        ${resume.is_master ? '<span class="badge master-badge">Master</span>' : ''}
                    </div>
                    ${resume.description ? `<p class="card-text text-muted small">${escapeHtml(resume.description)}</p>` : ''}
                    ${resume.job_listing_id ? '<p class="card-text"><small class="text-success"><i class="bi bi-briefcase"></i> Linked to job</small></p>' : ''}
                    <p class="card-text"><small class="text-muted">Updated: ${formatDate(resume.updated_at)}</small></p>
                    <div class="btn-group w-100 mb-2" role="group">
                        <a href="index.html?resume=${resume.id}" class="btn btn-sm btn-primary">
                            <i class="bi bi-pencil"></i> Edit
                        </a>
                        <button class="btn btn-sm btn-outline-primary" onclick="showTailorModal('${resume.id}', '${escapeHtml(resume.name)}')">
                            <i class="bi bi-magic"></i> Tailor
                        </button>
                        ${!resume.is_master ? `<button class="btn btn-sm btn-outline-danger" onclick="deleteResume('${resume.id}', '${escapeHtml(resume.name)}')">
                            <i class="bi bi-trash"></i>
                        </button>` : ''}
                    </div>
                    <button class="btn btn-sm btn-success w-100" onclick="exportResumeDocx('${resume.id}', '${escapeHtml(resume.name)}')">
                        <i class="bi bi-file-earmark-word"></i> Export DOCX
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

function renderJobListings() {
    const container = document.getElementById('jobListingsContainer');
    const loading = document.getElementById('loadingJobListings');

    loading.style.display = 'none';
    container.style.display = 'flex';

    if (jobListings.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="bi bi-briefcase" style="font-size: 4rem; color: #ccc;"></i>
                <p class="text-muted mt-3">No job listings yet. Add a job listing to start tailoring resumes!</p>
            </div>
        `;
        return;
    }

    container.innerHTML = jobListings.map(job => `
        <div class="col-md-6 col-lg-4">
            <div class="card job-listing-card">
                <div class="card-body">
                    <h5 class="card-title">${escapeHtml(job.title)}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">${escapeHtml(job.company)}</h6>
                    ${job.location ? `<p class="card-text"><small><i class="bi bi-geo-alt"></i> ${escapeHtml(job.location)}</small></p>` : ''}
                    <p class="card-text"><small class="text-muted">Added: ${formatDate(job.created_at)}</small></p>
                    <div class="btn-group w-100" role="group">
                        <button class="btn btn-sm btn-primary" onclick="viewJobListing('${job.id}')">
                            <i class="bi bi-eye"></i> View
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteJobListing('${job.id}', '${escapeHtml(job.title)}')">
                            <i class="bi bi-trash"></i> Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// ============================================================================
// Modal Functions
// ============================================================================

function showCreateResumeModal() {
    // Populate base resume dropdown
    const select = document.getElementById('baseResume');
    select.innerHTML = '<option value="">Start from scratch</option>';

    resumes.forEach(resume => {
        const option = document.createElement('option');
        option.value = resume.id;
        option.textContent = resume.name;
        select.appendChild(option);
    });

    const modal = new bootstrap.Modal(document.getElementById('createResumeModal'));
    modal.show();
}

function showCreateJobListingModal() {
    const modal = new bootstrap.Modal(document.getElementById('createJobListingModal'));
    modal.show();
}

function showTailorModal(resumeId, resumeName) {
    document.getElementById('tailorSourceResumeId').value = resumeId;
    document.getElementById('tailorResumeName').value = `${resumeName} - Tailored`;

    // Populate job listings dropdown
    const select = document.getElementById('tailorJobListing');
    select.innerHTML = '<option value="">Choose a job listing...</option>';

    jobListings.forEach(job => {
        const option = document.createElement('option');
        option.value = job.id;
        option.textContent = `${job.title} at ${job.company}`;
        select.appendChild(option);
    });

    const modal = new bootstrap.Modal(document.getElementById('tailorResumeModal'));
    modal.show();
}

function viewJobListing(jobId) {
    // For now, just show an alert. In the future, this could open a detailed view
    const job = jobListings.find(j => j.id === jobId);
    if (job) {
        alert(`Job: ${job.title}\nCompany: ${job.company}\n\nClick OK to close.`);
    }
}

// ============================================================================
// Utility Functions
// ============================================================================

function updateStatistics() {
    document.getElementById('totalResumes').textContent = resumes.length;
    document.getElementById('totalJobListings').textContent = jobListings.length;

    const tailored = resumes.filter(r => r.job_listing_id).length;
    document.getElementById('tailoredResumes').textContent = tailored;
}

function showAlert(message, type = 'info', duration = 0) {
    const container = document.getElementById('alertContainer');
    const alertId = 'alert-' + Date.now();

    const alertHtml = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', alertHtml);

    if (duration > 0) {
        setTimeout(() => {
            const alert = document.getElementById(alertId);
            if (alert) {
                const bsAlert = bootstrap.Alert.getInstance(alert);
                if (bsAlert) {
                    bsAlert.close();
                } else {
                    alert.remove();
                }
            }
        }, duration);
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


