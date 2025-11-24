// MusicCreator Viewer JavaScript

let osmd = null;
let currentSheetMusicUrl = null;
let audioPlayer = null;
let currentAudioUrl = null;

document.addEventListener('DOMContentLoaded', function() {
    loadCompositions();
});

async function loadCompositions() {
    const listDiv = document.getElementById('compositions-list');
    
    try {
        const response = await fetch('/api/compositions');
        const compositions = await response.json();
        
        if (compositions.length === 0) {
            listDiv.innerHTML = '<p class="no-compositions">No compositions yet. Go to <a href="/">Generate</a> to create some!</p>';
            return;
        }
        
        listDiv.innerHTML = '';
        
        compositions.forEach(comp => {
            const card = document.createElement('div');
            card.className = 'composition-card';
            card.innerHTML = `
                <h3>${comp.name}</h3>
                <p class="composer-info">Composer style: ${comp.composer}</p>
                <div class="card-actions">
                    ${comp.sheetMusic ? `<button onclick="openSheetMusic('${comp.sheetMusic}', '${comp.name}')" class="btn btn-secondary">📄 View Sheet Music</button>` : ''}
                    <button onclick="openAudioPlayer('${comp.audio}', '${comp.name}')" class="btn btn-secondary">▶️ Play Audio</button>
                    ${comp.sheetMusic ? `<a href="${comp.sheetMusic}" download class="btn btn-link">Download XML</a>` : ''}
                    <a href="${comp.audio}" download class="btn btn-link">Download MIDI</a>
                </div>
            `;
            listDiv.appendChild(card);
        });
        
    } catch (error) {
        console.error('Error loading compositions:', error);
        listDiv.innerHTML = '<p class="error">Error loading compositions</p>';
    }
}

async function openSheetMusic(url, title) {
    currentSheetMusicUrl = url;
    document.getElementById('modal-title').textContent = title;
    document.getElementById('viewer-modal').style.display = 'flex';
    
    const container = document.getElementById('sheet-music-container');
    container.innerHTML = '<p class="loading">Loading sheet music...</p>';
    
    try {
        // Initialize OpenSheetMusicDisplay
        osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay(container, {
            autoResize: true,
            backend: "svg",
            drawTitle: true,
            drawComposer: true,
            drawCredits: false,
            drawPartNames: true,
            drawFingerings: true,
        });
        
        // Load and render the MusicXML file
        await osmd.load(url);
        await osmd.render();
        
        container.querySelector('p')?.remove();
    } catch (error) {
        console.error('Error loading sheet music:', error);
        container.innerHTML = `
            <p class="error">Unable to display sheet music in browser.</p>
            <p>Download the MusicXML file and open it in MuseScore, Finale, or Sibelius.</p>
        `;
    }
}

function closeViewer() {
    document.getElementById('viewer-modal').style.display = 'none';
    document.getElementById('sheet-music-container').innerHTML = '';
    osmd = null;
}

function downloadCurrentSheet() {
    if (currentSheetMusicUrl) {
        window.location.href = currentSheetMusicUrl;
    }
}

function openAudioPlayer(url, title) {
    currentAudioUrl = url;
    document.getElementById('player-title').textContent = title;
    document.getElementById('player-modal').style.display = 'flex';
    
    audioPlayer = document.getElementById('audio-player');
    audioPlayer.src = url;
    audioPlayer.load();
    
    document.getElementById('download-audio-btn').href = url;
    
    // Set up audio player events
    audioPlayer.addEventListener('loadedmetadata', function() {
        document.getElementById('total-time').textContent = formatTime(audioPlayer.duration);
    });
    
    audioPlayer.addEventListener('timeupdate', function() {
        const progress = (audioPlayer.currentTime / audioPlayer.duration) * 100;
        document.getElementById('progress-slider').value = progress;
        document.getElementById('current-time').textContent = formatTime(audioPlayer.currentTime);
    });
    
    audioPlayer.addEventListener('ended', function() {
        document.getElementById('play-icon').textContent = '▶️';
    });
    
    // Volume control
    const volumeSlider = document.getElementById('volume-slider');
    volumeSlider.addEventListener('input', function() {
        audioPlayer.volume = this.value / 100;
    });
    
    // Progress slider
    const progressSlider = document.getElementById('progress-slider');
    progressSlider.addEventListener('input', function() {
        const time = (this.value / 100) * audioPlayer.duration;
        audioPlayer.currentTime = time;
    });
}

function closePlayer() {
    document.getElementById('player-modal').style.display = 'none';
    if (audioPlayer) {
        audioPlayer.pause();
        audioPlayer.src = '';
    }
}

function togglePlay() {
    if (!audioPlayer) return;
    
    const playIcon = document.getElementById('play-icon');
    
    if (audioPlayer.paused) {
        audioPlayer.play();
        playIcon.textContent = '⏸️';
    } else {
        audioPlayer.pause();
        playIcon.textContent = '▶️';
    }
}

function stopAudio() {
    if (!audioPlayer) return;
    
    audioPlayer.pause();
    audioPlayer.currentTime = 0;
    document.getElementById('play-icon').textContent = '▶️';
}

function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}
