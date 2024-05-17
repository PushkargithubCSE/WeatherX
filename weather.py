from pyowm import OWM

# Replace 'your-api-key' with your actual OpenWeatherMap API key
owm = OWM('ea10bfc176ead0ebea34970bfff36677')

def get_forecast(lat, lon):
    mgr = owm.weather_manager()
    observation = mgr.weather_at_coords(lat, lon)
    weather = observation.weather

    location = observation.location
    loc_name = location.name
    loc_lat = location.lat
    loc_lon = location.lon

    results = []

    results.append(f"Location: {loc_name}, Lat: {loc_lat}, Lon: {loc_lon}")

    status = weather.status
    detailed = weather.detailed_status
    temperature = weather.temperature('celsius')
    temp = temperature["temp"]
    temp_min = temperature["temp_min"]
    temp_max = temperature["temp_max"]

    results.append(f"Time: {weather.reference_time('iso')}")
    results.append(f"Status: {status}")
    results.append(f"Temperature: {temp}")
    results.append(f"Min Temperature: {temp_min}")
    results.append(f"Max Temperature: {temp_max}")

    return "\n".join(results)

if __name__ == "__main__":
    print(get_forecast(28.463845272479112, 77.00203055961481))

