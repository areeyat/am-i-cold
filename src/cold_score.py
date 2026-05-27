from .pipeline import fetch_weather_data


def get_cold_score(temp):
    if temp > 72: 
        return "not cold"
    elif temp > 65:
        return "chilly"
    elif temp > 60:
        return "soo chilly"
    elif temp > 55:
        return "brr"
    elif temp > 50:
        return "brrr"
    elif temp > 45:
        return "soo brrrr"
    else:
        return "brr brr brrrrr"

if __name__ == "__main__":
    weather_data = fetch_weather_data()
    print(weather_data.columns)
    print(weather_data['forecast_time'])
    temps = weather_data['temperature_f']

    print(weather_data.apply(lambda x: get_cold_score(x.temperature_f), axis=1)[0])  

