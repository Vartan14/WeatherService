import "./current-weather.css"

const CurrentWeather = ({data}) => {
    return (
        <div className="weather">
            <div className="top">
                <div>
                    <p className="city">{data.city}</p>
                    <p className="weather-description">{data.weather.condition}</p>
                </div>
                <img alt="weather" className="weather-icon" src={`icons/white-${data.weather.icon}.png`}/>
            </div>

            <div className="bottom">
                <p className="temperature">{`${Math.round(data.weather.temp)}°C`}</p> 
                <div className="details">
                   
                    <div className="parameter-row">
                        <span className="parameter-label">Feels like</span>
                        <span className="parameter-value">{`${Math.round(data.weather.feels_like)}°C`}</span>
                    </div>
                    <div className="parameter-row">
                        <span className="parameter-label">Wind</span>
                        <span className="parameter-value">{`${data.weather.wind_speed} m/s`}</span>
                    </div>
                    <div className="parameter-row">
                        <span className="parameter-label">Humidity</span>
                        <span className="parameter-value">{`${data.weather.humidity} %`}</span>
                    </div>
                    <div className="parameter-row">
                        <span className="parameter-label">Pressure</span>
                        <span className="parameter-value">{`${data.weather.pressure} mm`}</span>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default CurrentWeather