// MusicCreator Web App JavaScript

let currentMusicXML = null;

document.addEventListener('DOMContentLoaded', function() {
    // Load composers
    loadComposers();
    
    // Toggle advanced options
    document.getElementById('toggle-advanced').addEventListener('click', function() {
        const advancedDiv = document.getElementById('advanced-options');
        const isVisible = advancedDiv.style.display !== 'none';
        advancedDiv.style.display = isVisible ? 'none' : 'block';
        this.textContent = isVisible ? 'Show' : 'Hide';
    });
    
    // Generate button
    document.getElementById('generate-btn').addEventListener('click', generateMusic);
});

async function loadComposers() {
    try {
        const response = await fetch('/api/composers');
        const composers = await response.json();
        
        const select = document.getElementById('composer');
        select.innerHTML = '<option value="">Select a composer...</option>';
        
        composers.forEach(composer => {
            const option = document.createElement('option');
            option.value = composer.name;
            option.textContent = `${composer.name} (${composer.era}, ${composer.years})`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading composers:', error);
        const select = document.getElementById('composer');
        select.innerHTML = '<option value="">Error loading composers</option>';
    }
}

async function generateMusic() {
    const statusDiv = document.getElementById('status-message');
    const progressDiv = document.getElementById('progress-message');
    const generateBtn = document.getElementById('generate-btn');
    const btnText = document.getElementById('btn-text');
    const btnSpinner = document.getElementById('btn-spinner');
    
    // Get form values
    const composerSelect = document.getElementById('composer').value;
    const customComposer = document.getElementById('custom-composer').value;
    const composer = customComposer || composerSelect;
    
    if (!composer) {
        showStatus('Please select or enter a composer name', 'error');
        return;
    }
    
    const instruments = Array.from(document.querySelectorAll('input[name="instrument"]:checked'))
        .map(cb => cb.value);
    
    if (instruments.length === 0) {
        showStatus('Please select at least one instrument', 'error');
        return;
    }
    
    const difficulty = document.querySelector('input[name="difficulty"]:checked').value;
    const mood = document.getElementById('mood').value;
    const timeSignature = document.getElementById('time-signature').value;
    const keySignature = document.getElementById('key-signature').value;
    const tempo = document.getElementById('tempo').value;
    const numCompositions = parseInt(document.getElementById('num-compositions').value);
    
    // Disable button and show progress
    generateBtn.disabled = true;
    btnText.style.display = 'none';
    btnSpinner.style.display = 'inline-block';
    progressDiv.style.display = 'block';
    document.getElementById('results-section').style.display = 'none';
    
    try {
        // Show progress
        updateProgress(10, 'Researching composer...');
        
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                composer,
                instruments,
                difficulty,
                mood,
                timeSignature,
                keySignature,
                tempo: tempo ? parseInt(tempo) : null,
                numCompositions
            })
        });
        
        if (!response.ok) {
            throw new Error('Generation failed');
        }
        
        updateProgress(50, 'Analyzing musical style...');
        
        const result = await response.json();
        
        updateProgress(80, 'Generating compositions...');
        
        if (result.status === 'success') {
            updateProgress(100, 'Complete!');
            
            showStatus(`✨ Successfully generated ${result.files.length} compositions!`, 'success');
            displayResults(result);
            
            setTimeout(() => {
                progressDiv.style.display = 'none';
            }, 2000);
        } else {
            throw new Error(result.error || 'Unknown error');
        }
        
    } catch (error) {
        console.error('Error generating music:', error);
        showStatus(`❌ Error: ${error.message}`, 'error');
        progressDiv.style.display = 'none';
    } finally {
        // Re-enable button
        generateBtn.disabled = false;
        btnText.style.display = 'inline';
        btnSpinner.style.display = 'none';
    }
}

function updateProgress(percent, text) {
    document.getElementById('progress-fill').style.width = percent + '%';
    document.getElementById('progress-text').textContent = text;
}

function displayResults(result) {
    const resultsSection = document.getElementById('results-section');
    const resultsList = document.getElementById('results-list');
    
    resultsSection.style.display = 'block';
    resultsList.innerHTML = '';
    
    result.files.forEach((file, index) => {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.innerHTML = `
            <h3>🎼 ${file.title}</h3>
            <div class="card-actions">
                <button onclick="viewSheetMusic('${file.sheetMusic}', '${file.title}')" class="btn btn-secondary">
                    📄 View Sheet Music
                </button>
                <button onclick="playAudio('${file.audio}', '${file.title}')" class="btn btn-secondary">
                    ▶️ Play Audio
                </button>
                <a href="${file.sheetMusic}" download class="btn btn-link">Download XML</a>
                <a href="${file.audio}" download class="btn btn-link">Download MIDI</a>
            </div>
        `;
        resultsList.appendChild(card);
    });
    
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function viewSheetMusic(url, title) {
    window.open(`/viewer?file=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}`, '_blank');
}

function playAudio(url, title) {
    window.open(`/viewer?audio=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}`, '_blank');
}

function showStatus(message, type) {
    const statusDiv = document.getElementById('status-message');
    statusDiv.innerHTML = message;
    statusDiv.className = `status-message ${type}`;
    statusDiv.style.display = 'block';
    
    if (type === 'success') {
        setTimeout(() => {
            statusDiv.style.display = 'none';
        }, 5000);
    }
}
