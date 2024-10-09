// List of districts
const districts = ['agra', 'aligarh', 'allahabad', 'ambedkar nagar', 'amethi', 'amroha', 'auraiya', 'azamgarh', 'baghpat', 'bahraich', 'ballia', 'balrampur', 'banda', 'barabanki', 'bareilly', 'basti', 'bijnor', 'budaun', 'bulandshahr', 'chandauli', 'chitrakoot', 'deoria', 'etah', 'etawah', 'faizabad', 'farrukhabad', 'fatehpur', 'firozabad', 'gautam buddha nagar', 'ghaziabad', 'ghazipur', 'gonda', 'gorakhpur', 'hamirpur', 'hapur', 'hardoi', 'hathras', 'jalaun', 'jaunpur', 'jhansi', 'kannauj', 'kanpur dehat', 'kanpur nagar', 'kasganj', 'kaushambi', 'kheri', 'kushi nagar', 'lalitpur', 'lucknow', 'maharajganj', 'mahoba', 'mainpuri', 'mathura', 'mau', 'meerut', 'mirzapur', 'moradabad', 'muzaffarnagar', 'pilibhit', 'pratapgarh', 'rae bareli', 'rampur', 'saharanpur', 'sambhal', 'sant kabeer nagar', 'sant ravidas nagar', 'shahjahanpur', 'shamli', 'shravasti', 'siddharth nagar', 'sitapur', 'sonbhadra', 'sultanpur', 'unnao', 'varanasi'];

// Populate district dropdown
const districtSelect = document.getElementById('district');
districts.forEach(district => {
    const option = document.createElement('option');
    option.value = district;
    option.textContent = district.charAt(0).toUpperCase() + district.slice(1);
    districtSelect.appendChild(option);
});

document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        District: document.getElementById('district').value.toLowerCase(),
        'Area (Hectare)': parseFloat(document.getElementById('area').value),
        Season: document.getElementById('season').value,
        N: parseFloat(document.getElementById('N').value),
        P2O5: parseFloat(document.getElementById('P2O5').value),
        K2O: parseFloat(document.getElementById('K2O').value),
        Start_Year: 2022,
        Humidity_Sowing: 0,
        Humidity_Full: 0,
        Rainfall_Sowing: 0,
        Rainfall_Full: 0,
        Max_Temperature_Sowing: 0,
        Max_Temperature_Full: 0,
        Min_Temperature_Sowing: 0,
        Min_Temperature_Full: 0
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const results = await response.json();
        await displayResults(results, formData.District);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('results').innerHTML = `<p>Error: ${error.message}</p>`;
    }
});

async function displayResults(results, district) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<h2>Top 3 Recommended Crops:</h2>';

    for (const [crop, details] of Object.entries(results)) {
        const cropDiv = document.createElement('div');
        cropDiv.className = 'crop-result';
        cropDiv.innerHTML = `
            <h3>${crop.charAt(0).toUpperCase() + crop.slice(1)}</h3>
            <p>Predicted Yield Difference: ${details.Yield_Difference.toFixed(2)} Tonnes/Hectare</p>
            <h4>Nutrient Recommendations:</h4>
            <ul>
                ${details.Nutrient_Recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
            <canvas id="${crop}-chart"></canvas>
        `;
        resultsDiv.appendChild(cropDiv);

        try {
            const historicalData = await fetchHistoricalYield(district, crop);
            createChart(crop, historicalData);
        } catch (error) {
            console.error(`Error fetching historical data for ${crop}:`, error);
            document.getElementById(`${crop}-chart`).innerHTML = `<p>Error loading historical data: ${error.message}</p>`;
        }
    }
}

async function fetchHistoricalYield(district, crop) {
    const response = await fetch(`/historical_yield?district=${encodeURIComponent(district)}&crop=${encodeURIComponent(crop)}`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

function createChart(crop, data) {
    const ctx = document.getElementById(`${crop}-chart`).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.years,
            datasets: [{
                label: 'Historical Yield',
                data: data.yields,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Yield (Tonnes/Hectare)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Year'
                    }
                }
            }
        }
    });
}