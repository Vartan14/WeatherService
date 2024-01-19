import {
  Accordion,
  AccordionItem,
  AccordionItemButton,
  AccordionItemHeading,
  AccordionItemPanel,
} from "react-accessible-accordion"

import "./forecast.css"

const WEEK_DAYS = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
]

const Forecast = ({ data }) => {
  const dayInAWeek = new Date().getDay()
  const forecastDays = WEEK_DAYS.slice(dayInAWeek, WEEK_DAYS.length).concat(
    WEEK_DAYS.slice(0, dayInAWeek)
  )


  return (
    <>
      <span className="title">Daily Forecast</span>
      <Accordion allowZeroExpanded>
        {data.weather_list.slice(1, 7).map((item, index) => (
          <AccordionItem key={index}>
            <AccordionItemHeading>
              <AccordionItemButton>
                <div className="daily-item">
                  <img
                    alt="weather"
                    className="daily-icon"
                    src={`icons/${item.icon}.png`}
                  />
                  <span className="day">{forecastDays[index]}</span>
                  <span className="description">{item.condition.split("/")[1]}</span>
                  <span className="min-max-temp">
                    {Math.round(item.temp.min)}°C /{" "}
                    {Math.round(item.temp.max)}°C
                  </span>
                </div>
              </AccordionItemButton>
            </AccordionItemHeading>

            <AccordionItemPanel>
                <div className="daily-details-grid">
                    <div className="daily-details-grid-item">
                        <span>Pressure</span>
                        <span>{item.pressure} mm</span>
                    </div>
                    <div className="daily-details-grid-item">
                        <span>Humidity</span>
                        <span>{item.humidity}%</span>
                    </div>
                    <div className="daily-details-grid-item">
                        <span>Clouds</span>
                        <span>{item.clouds}%</span>
                    </div>
                    <div className="daily-details-grid-item">
                        <span>Wind speed</span>
                        <span>{item.wind_speed} m/s</span>
                    </div>
                    <div className="daily-details-grid-item">
                        <span>Precipitation</span>
                        <span>{Math.round(item.precip_prob)}%</span>
                    </div>
                    <div className="daily-details-grid-item">
                        <span>Feels like</span>
                        <span>{Math.round(item.feels_like.day)}°C</span>
                    </div>
                </div>
            </AccordionItemPanel>
          </AccordionItem>
        ))}

      </Accordion>
    </>
  )
}

export default Forecast
