// This function fetches current weather data from the server
function fetchCurrentWeather(location) {
    fetch(`/weather/current?location=${location}`)
        .then(response => response.json())
        .then(data => {
            console.log('Current Weather:', data);
            displayWeatherData(data);
        })
        .catch(error => {
            console.error('Error fetching current weather:', error);
        });
}

// Display the weather data in the UI
function displayWeatherData(data) {
    const resultsDiv = document.getElementById('weather-results');
    resultsDiv.innerHTML = `
        <h3>Weather in ${data.location.name}, ${data.location.country}:</h3>
        <p>Temperature: ${data.current.temp_c}°C</p>
        <p>Condition: ${data.current.condition.text}</p>
        <img src="${data.current.condition.icon}" alt="Weather icon">
    `;
}

// Handle button click to fetch weather data
document.getElementById('weather-button').addEventListener('click', function() {
    const location = document.getElementById('location-input').value;
    fetchCurrentWeather(location);
});