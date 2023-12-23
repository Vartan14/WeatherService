import "./App.css"
import Search from "./components/search/search"
import CurrentWeather from "./components/current-weather/current-weather"
import { WEATHER_API_URL } from "./api"
import { WEATHER_API_KEY } from "./config"
import { useState } from "react"
import Forecast from "./components/forecast/forecast"

function App() {
  const [currentWeather, setCurrentWeather] = useState(null)
  const [forecast, setForecast] = useState(null)

  const handleOnSearchChange = (searchData) => {
    const [lat, lon] = searchData.value.split(" ")

    const currentWeatherFetch = fetch(
      `${WEATHER_API_URL}/weather?lat=${lat}&lon=${lon}&appid=${WEATHER_API_KEY}&units=metric`
    )

    const forecastWeatherFetch = fetch(
      `${WEATHER_API_URL}/forecast/daily?lat=${lat}&lon=${lon}&appid=${WEATHER_API_KEY}&units=metric`
    )

    Promise.all([currentWeatherFetch, forecastWeatherFetch])
      .then(async (response) => {
        const weatherResponse = await response[0].json()
        const forecastResponse = await response[1].json()

        setCurrentWeather({ city: searchData.label, ...weatherResponse })
        setForecast({ city: searchData.label, ...forecastResponse })
      })
      .catch((err) => console.log(err))
  }


  console.log(forecast);

  return (
    <div className="container">
      <Search onSearchChange={handleOnSearchChange} />
      {currentWeather && <CurrentWeather data={currentWeather} />}
      {forecast && <Forecast data={forecast}/>}
    </div>
  )
}

export default App
