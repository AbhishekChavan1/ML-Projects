// API Base URL
const API_BASE = '';

// Tab Management
function openTab(evt, tabName) {
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }

    const tabButtons = document.getElementsByClassName('tab-button');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }

    document.getElementById(tabName).classList.add('active');
    evt.currentTarget.classList.add('active');

    // Load data when tab is opened
    if (tabName === 'model-info') {
        loadModelInfo();
    } else if (tabName === 'features') {
        loadFeatureImportance();
    }
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Fill random data
function fillRandomData() {
    document.getElementById('medInc').value = (Math.random() * 10 + 1).toFixed(2);
    document.getElementById('houseAge').value = Math.floor(Math.random() * 50 + 5);
    document.getElementById('aveRooms').value = (Math.random() * 5 + 3).toFixed(1);
    document.getElementById('aveBedrms').value = (Math.random() * 2 + 0.5).toFixed(1);
    document.getElementById('population').value = Math.floor(Math.random() * 3000 + 500);
    document.getElementById('aveOccup').value = (Math.random() * 3 + 2).toFixed(1);
    document.getElementById('latitude').value = (Math.random() * 5 + 33).toFixed(2);
    document.getElementById('longitude').value = (Math.random() * 5 - 123).toFixed(2);
}

// Prediction Form Handler
document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const features = {
        MedInc: parseFloat(document.getElementById('medInc').value),
        HouseAge: parseFloat(document.getElementById('houseAge').value),
        AveRooms: parseFloat(document.getElementById('aveRooms').value),
        AveBedrms: parseFloat(document.getElementById('aveBedrms').value),
        Population: parseFloat(document.getElementById('population').value),
        AveOccup: parseFloat(document.getElementById('aveOccup').value),
        Latitude: parseFloat(document.getElementById('latitude').value),
        Longitude: parseFloat(document.getElementById('longitude').value)
    };

    try {
        const response = await fetch(`${API_BASE}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(features)
        });

        if (!response.ok) {
            throw new Error('Prediction failed');
        }

        const data = await response.json();
        displayPrediction(data);
        showNotification('Prediction successful!', 'success');
    } catch (error) {
        showNotification('Error making prediction: ' + error.message, 'error');
    }
});

// Display prediction result
function displayPrediction(data) {
    const resultBox = document.getElementById('predictionResult');
    const priceValue = document.getElementById('priceValue');

    priceValue.textContent = `$${data.price_in_thousands.toFixed(2)}k`;
    resultBox.style.display = 'block';

    // Smooth scroll to result
    resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Load Model Info
async function loadModelInfo() {
    const content = document.getElementById('modelInfoContent');
    content.innerHTML = '<p class="loading">Loading model information...</p>';

    try {
        const response = await fetch(`${API_BASE}/model-info`);
        const data = await response.json();

        const html = `
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Model Type</div>
                    <div class="info-value">${data.model_type}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Estimators</div>
                    <div class="info-value">${data.n_estimators}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Max Depth</div>
                    <div class="info-value">${data.max_depth}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Training Samples</div>
                    <div class="info-value">${data.training_samples.toLocaleString()}</div>
                </div>
            </div>

            <h3 style="margin-top: 30px; margin-bottom: 15px;">Model Performance</h3>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Train R² Score</div>
                    <div class="info-value">${data.metrics.train_r2.toFixed(4)}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Test R² Score</div>
                    <div class="info-value">${data.metrics.test_r2.toFixed(4)}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Train RMSE</div>
                    <div class="info-value">${data.metrics.train_rmse.toFixed(4)}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Test RMSE</div>
                    <div class="info-value">${data.metrics.test_rmse.toFixed(4)}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Train MAE</div>
                    <div class="info-value">${data.metrics.train_mae.toFixed(4)}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Test MAE</div>
                    <div class="info-value">${data.metrics.test_mae.toFixed(4)}</div>
                </div>
            </div>

            <h3 style="margin-top: 30px; margin-bottom: 15px;">Features Used</h3>
            <div class="feature-grid">
                ${data.features.map(feature => `
                    <div class="feature-item">
                        <span class="feature-name">${feature}</span>
                    </div>
                `).join('')}
            </div>
        `;

        content.innerHTML = html;
    } catch (error) {
        content.innerHTML = '<p class="loading">Error loading model information</p>';
        showNotification('Error loading model info: ' + error.message, 'error');
    }
}

// Load Sample Data
async function loadSampleData() {
    const content = document.getElementById('sampleDataContent');
    content.innerHTML = '<p class="loading">Loading sample data...</p>';

    try {
        const response = await fetch(`${API_BASE}/sample-data`);
        const samples = await response.json();

        const html = samples.map((sample, index) => `
            <div class="sample-card">
                <div class="sample-header">
                    <h3>Sample ${index + 1}</h3>
                    <div>
                        <div style="font-size: 0.9rem; color: var(--text-secondary);">Actual Price</div>
                        <div class="sample-price">$${sample.actual_price_thousands.toFixed(2)}k</div>
                    </div>
                    <div>
                        <div style="font-size: 0.9rem; color: var(--text-secondary);">Predicted Price</div>
                        <div class="sample-price">$${sample.predicted_price_thousands.toFixed(2)}k</div>
                    </div>
                </div>
                <div class="feature-grid">
                    ${Object.entries(sample.features).map(([key, value]) => `
                        <div class="feature-item">
                            <span class="feature-name">${key}:</span>
                            <span class="feature-value">${value.toFixed(2)}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `).join('');

        content.innerHTML = html;
        showNotification('Sample data loaded successfully!', 'success');
    } catch (error) {
        content.innerHTML = '<p class="loading">Error loading sample data</p>';
        showNotification('Error loading sample data: ' + error.message, 'error');
    }
}

// Load Feature Importance
async function loadFeatureImportance() {
    const content = document.getElementById('featureImportanceContent');
    content.innerHTML = '<p class="loading">Loading feature importance...</p>';

    try {
        const response = await fetch(`${API_BASE}/feature-importance`);
        const features = await response.json();

        const maxImportance = Math.max(...features.map(f => f.importance));

        const html = features.map(feature => `
            <div class="importance-bar">
                <div class="importance-label">${feature.feature}</div>
                <div class="importance-progress">
                    <div class="importance-fill" style="width: ${(feature.importance / maxImportance * 100).toFixed(1)}%">
                        ${(feature.importance * 100).toFixed(1)}%
                    </div>
                </div>
                <div class="importance-value">${feature.importance.toFixed(4)}</div>
            </div>
        `).join('');

        content.innerHTML = html;
    } catch (error) {
        content.innerHTML = '<p class="loading">Error loading feature importance</p>';
        showNotification('Error loading feature importance: ' + error.message, 'error');
    }
}

// Retrain Model
async function retrainModel() {
    if (!confirm('Are you sure you want to retrain the model? This may take a few moments.')) {
        return;
    }

    showNotification('Retraining model... Please wait.', 'success');

    try {
        const response = await fetch(`${API_BASE}/retrain`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.status === 'success') {
            showNotification('Model retrained successfully!', 'success');
            loadModelInfo();
        } else {
            throw new Error('Retraining failed');
        }
    } catch (error) {
        showNotification('Error retraining model: ' + error.message, 'error');
    }
}

// Load initial data
window.addEventListener('load', () => {
    // Load a random example on page load
    fillRandomData();
});
