window.addEventListener('load', ()=> {
    let long;
    let lat;
    let temperatureDescription = document.querySelector('.temperature-description');
    let temperatureDegree = document.querySelector('.temperature-degree');
    let locationTimezone = document.querySelector('.location-timezone');
    let degreeSection = document.querySelector('.degree-section');
    const temperatureSpan = document.querySelector('.temperature-section span');

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            long = position.coords.longitude;
            lat = position.coords.latitude;

            const proxy = 'https://cors-anywhere.herokuapp.com/';
            const api = `${proxy}https://api.darksky.net/forecast/0454759bd21ca16394c804e8889f325e/${lat},${long}`;

            fetch(api)
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    console.log(data);
                    const {temperature, summary, icon} = data.currently;
                    //Formula for celsius
                    let celsius = (temperature - 32) * (5 / 9);
                    //Set DOM Elements from the API
                    temperatureDegree.textContent = Math.floor(celsius);
                    // temperatureDescription.textContent = summary;
                    locationTimezone.textContent = data.timezone
                    //Change temperature to Celsius/Farenheit
                    degreeSection.addEventListener('click', () => {
                        if (temperatureSpan.textContent === "C") {
                            temperatureSpan.textContent = "F";
                            temperatureDegree.textContent = Math.floor(temperature);
                        } else {
                            temperatureSpan.textContent = "C";
                            temperatureDegree.textContent = Math.floor(celsius);
                        }
                    });

                    //Set Icon
                    // const skycons = new Skycons({ "color": "pink" });
                    var skycons = new Skycons({ "color": "black" });
                    const currentIcon = icon.replace(/-/g, "_").toUpperCase();
                    skycons.add("icon", Skycons[currentIcon]);
                    skycons.play();
                    // skycons.add(document.querySelector('.icon'), Skycons[currentIcon]);
                });
        });
    } 
});


// www.darksky.net/dev
// skycons