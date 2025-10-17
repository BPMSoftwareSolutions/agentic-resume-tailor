/**
 * AI Agent Chat Interface
 * 
 * JavaScript application for interacting with the AI agent
 * Related to GitHub Issue #12
 */

// Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Global state
let messageHistory = [];
let availableAgents = {};
let selectedProvider = 'openai';
let selectedModel = 'gpt-4';

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

async function initializeApp() {
    try {
        // Load available agents
        await loadAvailableAgents();

        // Load existing memory
        await loadMemory();

        // Setup event listeners
        setupEventListeners();

        showAlert('Agent interface loaded successfully!', 'success', 3000);
    } catch (error) {
        console.error('Failed to initialize agent interface:', error);
        showAlert('Failed to load agent interface. Please check if the API server is running.', 'danger');
    }
}

function setupEventListeners() {
    // Send button
    document.getElementById('sendBtn').addEventListener('click', sendMessage);

    // Enter key in input
    document.getElementById('chatInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Clear memory button
    document.getElementById('clearMemoryBtn').addEventListener('click', clearMemory);

    // View memory button
    document.getElementById('viewMemoryBtn').addEventListener('click', viewMemory);

    // Agent provider selection
    document.getElementById('agentProvider').addEventListener('change', onProviderChange);

    // Agent model selection
    document.getElementById('agentModel').addEventListener('change', onModelChange);
}

/**
 * Load available agents from API
 */
async function loadAvailableAgents() {
    try {
        const response = await fetch(`${API_BASE_URL}/agents`);
        const data = await response.json();

        if (response.ok && data.success) {
            availableAgents = data.agents;
            populateProviderDropdown();
        } else {
            console.error('Failed to load agents:', data.error);
            showAlert('Failed to load available agents', 'warning');
        }
    } catch (error) {
        console.error('Failed to load agents:', error);
        showAlert('Failed to load available agents. Check if API server is running.', 'warning');
    }
}

/**
 * Populate provider dropdown with available providers
 */
function populateProviderDropdown() {
    const providerSelect = document.getElementById('agentProvider');
    providerSelect.innerHTML = '';

    for (const provider in availableAgents) {
        const option = document.createElement('option');
        option.value = provider;
        option.textContent = availableAgents[provider].name;
        providerSelect.appendChild(option);
    }

    // Set default provider
    providerSelect.value = selectedProvider;
    populateModelDropdown();
}

/**
 * Populate model dropdown based on selected provider
 */
function populateModelDropdown() {
    const providerSelect = document.getElementById('agentProvider');
    const modelSelect = document.getElementById('agentModel');
    const provider = providerSelect.value;

    modelSelect.innerHTML = '';

    if (availableAgents[provider]) {
        const models = availableAgents[provider].models;
        for (const modelId in models) {
            const model = models[modelId];
            const option = document.createElement('option');
            option.value = modelId;
            option.textContent = `${model.name} (${model.context_window.toLocaleString()} tokens)`;
            option.title = model.description;
            modelSelect.appendChild(option);
        }
    }

    // Set default model for provider
    if (selectedProvider === provider && selectedModel) {
        modelSelect.value = selectedModel;
    } else {
        // Select first model as default
        if (modelSelect.options.length > 0) {
            modelSelect.value = modelSelect.options[0].value;
            selectedModel = modelSelect.value;
        }
    }
}

/**
 * Handle provider change
 */
function onProviderChange() {
    const providerSelect = document.getElementById('agentProvider');
    selectedProvider = providerSelect.value;
    populateModelDropdown();
    showAlert(`Switched to ${availableAgents[selectedProvider].name}`, 'info', 2000);
}

/**
 * Handle model change
 */
function onModelChange() {
    const modelSelect = document.getElementById('agentModel');
    selectedModel = modelSelect.value;
    const provider = document.getElementById('agentProvider').value;
    const modelInfo = availableAgents[provider].models[selectedModel];
    showAlert(`Selected ${modelInfo.name}`, 'info', 2000);
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message) {
        return;
    }

    // Clear input
    input.value = '';

    // Add user message to chat
    addMessageToChat('user', message);

    // Show typing indicator
    showTypingIndicator(true);

    try {
        // Send to API with selected provider and model
        const response = await fetch(`${API_BASE_URL}/agent/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message,
                provider: selectedProvider,
                model: selectedModel
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            // Add assistant response to chat
            addMessageToChat('assistant', data.response);

            // Check if response contains a command to execute
            const commandMatch = extractCommand(data.response);
            if (commandMatch) {
                // Auto-execute the command
                await autoExecuteCommand(commandMatch);
            }
        } else {
            // Show error
            addMessageToChat('error', data.error || 'Failed to get response from agent');
        }

        // Update memory count
        await loadMemory();

    } catch (error) {
        console.error('Failed to send message:', error);
        addMessageToChat('error', 'Failed to communicate with agent. Please check if the API server is running.');
    } finally {
        showTypingIndicator(false);
    }
}

/**
 * Extract command from agent response
 * Looks for patterns like "run: <command>" in the response
 */
function extractCommand(response) {
    // Match "run: <command>" pattern
    const runPattern = /run:\s*(.+?)(?:\n|$)/i;
    const match = response.match(runPattern);

    if (match && match[1]) {
        return match[1].trim();
    }

    return null;
}

/**
 * Auto-execute a command suggested by the agent
 */
async function autoExecuteCommand(command) {
    try {
        addMessageToChat('system', `🔧 Executing command: ${command}`);
        showTypingIndicator(true);

        // Send command with "run:" prefix to agent
        const response = await fetch(`${API_BASE_URL}/agent/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: `run: ${command}`,
                provider: selectedProvider,
                model: selectedModel
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            // Add command result to chat
            addMessageToChat('system', data.response);
        } else {
            // Show error
            addMessageToChat('error', data.error || 'Failed to execute command');
        }

        // Update memory
        await loadMemory();

    } catch (error) {
        console.error('Failed to execute command:', error);
        addMessageToChat('error', `Failed to execute command: ${error.message}`);
    } finally {
        showTypingIndicator(false);
    }
}

function sendQuickMessage(message) {
    document.getElementById('chatInput').value = message;
    sendMessage();
}

function addMessageToChat(role, content) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const roleDiv = document.createElement('div');
    roleDiv.className = 'message-role';
    roleDiv.textContent = role.charAt(0).toUpperCase() + role.slice(1);
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(roleDiv);
    messageDiv.appendChild(contentDiv);
    
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingIndicator(show) {
    const indicator = document.getElementById('typingIndicator');
    if (show) {
        indicator.classList.add('active');
    } else {
        indicator.classList.remove('active');
    }
}

async function loadMemory() {
    try {
        const response = await fetch(`${API_BASE_URL}/agent/memory`);
        const data = await response.json();

        if (response.ok && data.success) {
            messageHistory = data.messages;
            updateMessageCount();

            // Load token usage stats (Issue #24)
            await loadTokenStats();
        }
    } catch (error) {
        console.error('Failed to load memory:', error);
    }
}

function updateMessageCount() {
    const countElement = document.getElementById('messageCount');
    // Filter out system messages for count
    const userMessages = messageHistory.filter(m => m.role !== 'system');
    countElement.textContent = userMessages.length;
}

/**
 * Load and display token usage statistics (Issue #24)
 */
async function loadTokenStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/agent/memory/stats`);
        const data = await response.json();

        if (response.ok && data.success) {
            updateTokenDisplay(data.stats);
        }
    } catch (error) {
        console.error('Failed to load token stats:', error);
    }
}

/**
 * Update token usage display (Issue #24)
 */
function updateTokenDisplay(stats) {
    const tokenCount = document.getElementById('tokenCount');
    const tokenBarFill = document.getElementById('tokenBarFill');
    const tokenWarning = document.getElementById('tokenWarning');

    // Update token count text
    tokenCount.textContent = `${stats.total_tokens}/${stats.max_tokens} tokens (${stats.percentage}%)`;

    // Update progress bar
    tokenBarFill.style.width = `${stats.percentage}%`;

    // Update bar color based on usage
    tokenBarFill.classList.remove('warning', 'critical');
    if (stats.critical) {
        tokenBarFill.classList.add('critical');
    } else if (stats.warning) {
        tokenBarFill.classList.add('warning');
    }

    // Show/hide warning message
    if (stats.critical) {
        tokenWarning.className = 'token-warning critical show';
        tokenWarning.innerHTML = `
            <strong>🚨 CRITICAL:</strong> Memory at ${stats.percentage}% capacity (${stats.total_tokens}/${stats.max_tokens} tokens).
            You are very close to the limit! Consider clearing memory now.
        `;
    } else if (stats.warning) {
        tokenWarning.className = 'token-warning warning show';
        tokenWarning.innerHTML = `
            <strong>⚠️ WARNING:</strong> Memory at ${stats.percentage}% capacity (${stats.total_tokens}/${stats.max_tokens} tokens).
            Consider clearing memory if conversation continues.
        `;
    } else {
        tokenWarning.className = 'token-warning';
        tokenWarning.innerHTML = '';
    }
}

async function clearMemory() {
    if (!confirm('Are you sure you want to clear the conversation history? This cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/agent/memory/clear`, {
            method: 'POST'
        });

        const data = await response.json();

        if (response.ok && data.success) {
            // Clear chat display
            const messagesContainer = document.getElementById('chatMessages');
            messagesContainer.innerHTML = `
                <div class="message system">
                    <div class="message-role">System</div>
                    <div class="message-content">Memory cleared. Starting fresh conversation!</div>
                </div>
            `;

            messageHistory = [];
            updateMessageCount();

            // Refresh token stats (Issue #24)
            await loadTokenStats();

            showAlert('Memory cleared successfully!', 'success', 3000);
        } else {
            showAlert('Failed to clear memory: ' + (data.error || 'Unknown error'), 'danger');
        }
    } catch (error) {
        console.error('Failed to clear memory:', error);
        showAlert('Failed to clear memory. Please check if the API server is running.', 'danger');
    }
}

async function viewMemory() {
    const modal = new bootstrap.Modal(document.getElementById('memoryModal'));
    const modalBody = document.getElementById('memoryModalBody');
    
    // Show loading
    modalBody.innerHTML = `
        <div class="text-center">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
    
    modal.show();
    
    try {
        await loadMemory();
        
        if (messageHistory.length === 0) {
            modalBody.innerHTML = '<p class="text-muted">No conversation history yet.</p>';
            return;
        }
        
        // Build history HTML
        let html = '<div class="list-group">';
        
        messageHistory.forEach((msg, index) => {
            const roleClass = msg.role === 'user' ? 'primary' : msg.role === 'assistant' ? 'secondary' : 'warning';
            html += `
                <div class="list-group-item">
                    <div class="d-flex w-100 justify-content-between">
                        <h6 class="mb-1">
                            <span class="badge bg-${roleClass}">${msg.role}</span>
                        </h6>
                        <small class="text-muted">#${index + 1}</small>
                    </div>
                    <p class="mb-1" style="white-space: pre-wrap;">${escapeHtml(msg.content)}</p>
                </div>
            `;
        });
        
        html += '</div>';
        modalBody.innerHTML = html;
        
    } catch (error) {
        console.error('Failed to load memory:', error);
        modalBody.innerHTML = '<p class="text-danger">Failed to load conversation history.</p>';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showAlert(message, type = 'info', timeout = 0) {
    const alertContainer = document.getElementById('alertContainer');
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alertDiv);
    
    if (timeout > 0) {
        setTimeout(() => {
            alertDiv.remove();
        }, timeout);
    }
}

