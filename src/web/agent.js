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

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

async function initializeApp() {
    try {
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
        // Send to API
        const response = await fetch(`${API_BASE_URL}/agent/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
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
            body: JSON.stringify({ message: `run: ${command}` })
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

