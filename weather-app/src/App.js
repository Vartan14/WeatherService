import "./App.css"
import Search from "./components/search/search"
import CurrentWeather from "./components/current-weather/current-weather"
import { WEATHER_API_URL } from "./api"
import { WEATHER_API_KEY } from "./config"
import { useState } from "react"
import Forecast from "./components/forecast/forecast"
import axios from "axios"


function App() {
  const [currentWeather, setCurrentWeather] = useState(null)
  const [forecast, setForecast] = useState(null)

  const handleOnSearchChange = (searchData) => {
    const [lat, lon] = searchData.value.split(" ")

    axios.get(`${WEATHER_API_URL}/weather?lat=${lat}&lon=${lon}&apikey=${WEATHER_API_KEY}`).then(resp => {
      setCurrentWeather({ city: searchData.label, ...resp.data})
    }).catch((err) => console.log(err))

 
    axios.get(`${WEATHER_API_URL}/forecast?lat=${lat}&lon=${lon}&apikey=${WEATHER_API_KEY}`).then(resp => {
      setForecast({ city: searchData.label, ...resp.data})
    }).catch((err) => console.log(err))

  }


  console.log(currentWeather);
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
