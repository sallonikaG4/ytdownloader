// YouTube to MP3 Downloader - Frontend JavaScript

const API_BASE = '';

let statusCheckInterval = null;

// DOM Elements
const urlInput = document.getElementById('urlInput');
const infoBtn = document.getElementById('infoBtn');
const downloadBtn = document.getElementById('downloadBtn');
const refreshBtn = document.getElementById('refreshBtn');
const videoInfo = document.getElementById('videoInfo');
const progressContainer = document.getElementById('progressContainer');
const progressStatus = document.getElementById('progressStatus');
const progressPercent = document.getElementById('progressPercent');
const progressFill = document.getElementById('progressFill');
const progressSpeed = document.getElementById('progressSpeed');
const progressETA = document.getElementById('progressETA');
const errorMessage = document.getElementById('errorMessage');
const successMessage = document.getElementById('successMessage');
const filesList = document.getElementById('filesList');
const bitrateSelect = document.getElementById('bitrateSelect');
const outputDir = document.getElementById('outputDir');

// Set default output directory to user's Documents folder
// This will be handled server-side, but we can show a friendly path
if (outputDir && outputDir.value === 'downloads') {
    // The server will use Documents/YouTube Downloads by default
    // We'll update the display after getting info from server
}
const playlistSelection = document.getElementById('playlistSelection');
const playlistItems = document.getElementById('playlistItems');
const selectAllBtn = document.getElementById('selectAllBtn');
const deselectAllBtn = document.getElementById('deselectAllBtn');
const selectedCount = document.getElementById('selectedCount');

let currentPlaylistInfo = null;
let selectedIndices = new Set();

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadFiles();
    checkStatus();
    
    // Auto-refresh status if download is active
    statusCheckInterval = setInterval(checkStatus, 1000);
    
    // Exit button removed - use window close button instead
});

// Get video info
infoBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();
    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }
    
    infoBtn.disabled = true;
    infoBtn.textContent = 'Loading...';
    videoInfo.classList.add('hidden');
    
    try {
        const response = await fetch(`${API_BASE}/api/info`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            const error = data.error || 'Failed to get video info';
            if (data.ffmpeg_error) {
                showError(`${error}\n\nPlease install FFmpeg. See FFMPEG_SETUP.md for instructions.`);
            } else {
                throw new Error(error);
            }
            return;
        }
        
        // Update output directory display if default path is provided
        if (data.default_downloads_path && outputDir) {
            // Show the actual path but keep it editable
            outputDir.placeholder = data.default_downloads_path;
            if (outputDir.value === 'downloads') {
                // Don't change the value, just show placeholder
            }
        }
        
        displayVideoInfo(data.info);
        
    } catch (error) {
        showError(error.message);
    } finally {
        infoBtn.disabled = false;
        infoBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 16v-4M12 8h.01"></path>
            </svg>
            Get Info
        `;
    }
});

// Download
downloadBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();
    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }
    
    // Check if playlist and has selections
    let selectedIndicesArray = null;
    if (currentPlaylistInfo && currentPlaylistInfo.type === 'playlist') {
        // Filter to only available videos
        const availableIndices = Array.from(selectedIndices).filter(idx => {
            const video = currentPlaylistInfo.videos.find(v => v.index === idx);
            return video && video.available !== false;
        });
        
        if (availableIndices.length === 0) {
            showError('Please select at least one available video from the playlist');
            return;
        }
        selectedIndicesArray = availableIndices.sort((a, b) => a - b);
    }
    
    downloadCompleted = false;
    downloadBtn.disabled = true;
    downloadBtn.textContent = 'Starting...';
    hideMessages();
    progressContainer.classList.remove('hidden');
    
    // Restart status checking if it was stopped
    if (!statusCheckInterval) {
        statusCheckInterval = setInterval(checkStatus, 1000);
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url,
                bitrate: bitrateSelect.value,
                output_dir: outputDir.value,
                selected_indices: selectedIndicesArray
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to start download');
        }
        
        // Status will be updated by checkStatus interval
        
    } catch (error) {
        showError(error.message);
        progressContainer.classList.add('hidden');
        downloadBtn.disabled = false;
        downloadBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            Download & Convert
        `;
    }
});

// Refresh files list
refreshBtn.addEventListener('click', () => {
    loadFiles();
});

// Track if we've already handled completion
let downloadCompleted = false;

// Check download status
async function checkStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/status`);
        const status = await response.json();
        
        if (status.active) {
            downloadCompleted = false;
            progressContainer.classList.remove('hidden');
            updateProgress(status);
            
            if (status.status === 'error') {
                showError(status.error || 'Download failed');
                resetDownloadButton();
                progressContainer.classList.add('hidden');
                downloadCompleted = true;
                // Stop polling
                if (statusCheckInterval) {
                    clearInterval(statusCheckInterval);
                    statusCheckInterval = null;
                }
            }
        } else if (!downloadCompleted && status.status === 'idle' && status.progress === 0) {
            // Download just completed (status reset to idle)
            if (progressContainer && !progressContainer.classList.contains('hidden')) {
                showSuccess('Download completed successfully!');
                loadFiles();
                resetDownloadButton();
                progressContainer.classList.add('hidden');
                downloadCompleted = true;
                // Stop polling after completion
                if (statusCheckInterval) {
                    clearInterval(statusCheckInterval);
                    statusCheckInterval = null;
                }
            }
        } else if (status.status === 'error' && !downloadCompleted) {
            showError(status.error || 'Download failed');
            resetDownloadButton();
            progressContainer.classList.add('hidden');
            downloadCompleted = true;
            // Stop polling
            if (statusCheckInterval) {
                clearInterval(statusCheckInterval);
                statusCheckInterval = null;
            }
        }
    } catch (error) {
        console.error('Error checking status:', error);
    }
}

// Update progress display
function updateProgress(status) {
    const percent = Math.round(status.progress || 0);
    progressFill.style.width = `${percent}%`;
    progressPercent.textContent = `${percent}%`;
    
    let statusText = 'Preparing...';
    if (status.status === 'downloading') {
        statusText = status.current_item || 'Downloading...';
        if (status.total_items > 1) {
            statusText += ` (${status.current_item_num || 0}/${status.total_items})`;
        }
    } else if (status.status === 'converting') {
        statusText = 'Converting to MP3...';
    } else if (status.status === 'starting') {
        statusText = 'Starting download...';
    }
    
    progressStatus.textContent = statusText;
    
    // Speed and ETA
    if (status.speed) {
        const speedKB = (status.speed / 1024).toFixed(1);
        const speedMB = (status.speed / 1024 / 1024).toFixed(2);
        progressSpeed.textContent = speedMB >= 1 
            ? `Speed: ${speedMB} MB/s`
            : `Speed: ${speedKB} KB/s`;
    } else {
        progressSpeed.textContent = 'Speed: --';
    }
    
    if (status.eta) {
        const minutes = Math.floor(status.eta / 60);
        const seconds = status.eta % 60;
        progressETA.textContent = `ETA: ${minutes}:${seconds.toString().padStart(2, '0')}`;
    } else {
        progressETA.textContent = 'ETA: --:--';
    }
}

// Display video info
function displayVideoInfo(info) {
    videoInfo.classList.remove('hidden');
    playlistSelection.classList.add('hidden');
    selectedIndices.clear();
    currentPlaylistInfo = null;
    
    if (info.type === 'playlist') {
        currentPlaylistInfo = info;
        const unavailableMsg = info.unavailable_count > 0 
            ? `<p class="warning-text">⚠️ ${info.unavailable_count} video(s) unavailable (blocked/removed) - excluded from selection</p>`
            : '';
        videoInfo.innerHTML = `
            <h3>📁 ${escapeHtml(info.title)}</h3>
            <p><strong>Type:</strong> Playlist</p>
            <p><strong>Available Videos:</strong> ${info.count}</p>
            ${unavailableMsg}
        `;
        
        // Show playlist selection
        displayPlaylistSelection(info);
    } else {
        videoInfo.innerHTML = `
            <h3>🎵 ${escapeHtml(info.title)}</h3>
            <p><strong>Type:</strong> Video</p>
            <p><strong>Duration:</strong> ${formatDuration(info.duration)}</p>
            ${info.uploader ? `<p><strong>Channel:</strong> ${escapeHtml(info.uploader)}</p>` : ''}
            ${info.view_count ? `<p><strong>Views:</strong> ${info.view_count.toLocaleString()}</p>` : ''}
        `;
    }
}

// Display playlist selection
function displayPlaylistSelection(info) {
    if (!info.videos || info.videos.length === 0) return;
    
    playlistSelection.classList.remove('hidden');
    
    // Select only available videos by default
    selectedIndices.clear();
    info.videos.forEach(video => {
        if (video.available !== false && video.index > 0) {
            selectedIndices.add(video.index);
        }
    });
    
    playlistItems.innerHTML = info.videos.map(video => {
        const isAvailable = video.available !== false && video.index > 0;
        const displayIndex = video.index > 0 ? video.index : video.original_index;
        const isSelected = isAvailable && selectedIndices.has(video.index);
        return `
        <div class="playlist-item ${isSelected ? 'selected' : ''} ${!isAvailable ? 'unavailable' : ''}" 
             data-index="${video.index > 0 ? video.index : -1}" 
             data-available="${isAvailable}">
            <input 
                type="checkbox" 
                class="playlist-item-checkbox" 
                data-index="${video.index > 0 ? video.index : -1}"
                ${isSelected ? 'checked' : ''}
                ${!isAvailable ? 'disabled' : ''}
            >
            <span class="playlist-item-index">${video.original_index}</span>
            <div class="playlist-item-info">
                <div class="playlist-item-title">
                    ${escapeHtml(video.title)}
                    ${!isAvailable ? '<span class="unavailable-badge">Unavailable</span>' : ''}
                </div>
                <div class="playlist-item-duration">
                    ${isAvailable ? formatDuration(video.duration) : 'Blocked/Removed'}
                </div>
            </div>
        </div>
    `;
    }).join('');
    
    updateSelectedCount();
    
    // Add event listeners only for available videos
    playlistItems.querySelectorAll('.playlist-item-checkbox:not(:disabled)').forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            const index = parseInt(e.target.dataset.index);
            if (index > 0) {  // Only process available videos (positive index)
                if (e.target.checked) {
                    selectedIndices.add(index);
                } else {
                    selectedIndices.delete(index);
                }
                updatePlaylistItemState(index, e.target.checked);
                updateSelectedCount();
            }
        });
    });
    
    // Add click handler to entire item (only for available videos)
    playlistItems.querySelectorAll('.playlist-item[data-available="true"]').forEach(item => {
        item.addEventListener('click', (e) => {
            if (e.target.type !== 'checkbox' && !e.target.closest('.unavailable-badge')) {
                const checkbox = item.querySelector('.playlist-item-checkbox');
                if (!checkbox.disabled) {
                    checkbox.checked = !checkbox.checked;
                    checkbox.dispatchEvent(new Event('change'));
                }
            }
        });
    });
}

// Update playlist item visual state
function updatePlaylistItemState(index, selected) {
    const item = playlistItems.querySelector(`[data-index="${index}"]`);
    if (item) {
        if (selected) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }
    }
}

// Update selected count display
function updateSelectedCount() {
    const count = selectedIndices.size;
    selectedCount.textContent = `${count} selected`;
}

// Select all
selectAllBtn.addEventListener('click', () => {
    if (!currentPlaylistInfo || !currentPlaylistInfo.videos) return;
    
    currentPlaylistInfo.videos.forEach(video => {
        // Only select available videos
        if (video.available !== false) {
            selectedIndices.add(video.index);
            const checkbox = playlistItems.querySelector(`[data-index="${video.index}"]`);
            if (checkbox && !checkbox.disabled) {
                checkbox.checked = true;
                updatePlaylistItemState(video.index, true);
            }
        }
    });
    updateSelectedCount();
});

// Deselect all
deselectAllBtn.addEventListener('click', () => {
    selectedIndices.clear();
    playlistItems.querySelectorAll('.playlist-item-checkbox').forEach(checkbox => {
        checkbox.checked = false;
        const index = parseInt(checkbox.dataset.index);
        updatePlaylistItemState(index, false);
    });
    updateSelectedCount();
});

// Load files list
async function loadFiles() {
    try {
        const dir = outputDir.value || 'downloads';
        const response = await fetch(`${API_BASE}/api/downloads?dir=${encodeURIComponent(dir)}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to load files');
        }
        
        // Update output directory display if path is provided
        if (data.path && outputDir) {
            outputDir.placeholder = data.path;
            // Update value if it's still "downloads"
            if (outputDir.value === 'downloads') {
                outputDir.value = data.path;
            }
        }
        
        displayFiles(data.files || []);
        
    } catch (error) {
        filesList.innerHTML = `<div class="error-message">Error loading files: ${error.message}</div>`;
    }
}

// Display files
function displayFiles(files) {
    if (files.length === 0) {
        filesList.innerHTML = `
            <div class="empty-state">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                <p>No files downloaded yet</p>
            </div>
        `;
        return;
    }
    
    filesList.innerHTML = files.map(file => `
        <div class="file-item">
            <div class="file-info">
                <div class="file-name">${escapeHtml(file.name)}</div>
                <div class="file-path">${escapeHtml(file.path)}</div>
            </div>
            <div class="file-actions">
                <button class="file-download-btn" onclick="downloadFile('${escapeHtml(file.path)}', '${escapeHtml(outputDir.value || 'downloads')}')">
                    Download
                </button>
            </div>
        </div>
    `).join('');
}

// Download file
function downloadFile(path, dir) {
    window.open(`${API_BASE}/api/download-file?path=${encodeURIComponent(path)}&dir=${encodeURIComponent(dir)}`, '_blank');
}

// Utility functions
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    successMessage.classList.add('hidden');
    setTimeout(() => {
        errorMessage.classList.add('hidden');
    }, 5000);
}

function showSuccess(message) {
    successMessage.textContent = message;
    successMessage.classList.remove('hidden');
    errorMessage.classList.add('hidden');
    setTimeout(() => {
        successMessage.classList.add('hidden');
    }, 5000);
}

function hideMessages() {
    errorMessage.classList.add('hidden');
    successMessage.classList.add('hidden');
}

function resetDownloadButton() {
    downloadBtn.disabled = false;
    downloadBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
        </svg>
        Download & Convert
    `;
}

function formatDuration(seconds) {
    if (!seconds) return 'Unknown';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Allow Enter key to trigger download
urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        downloadBtn.click();
    }
});

