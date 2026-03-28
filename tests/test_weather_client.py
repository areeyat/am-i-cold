from src.weather_client import WeatherClient, DEFAULT_LONGITUDE, DEFAULT_LATITUDE

def test_latitude_longitude_defaults():
    client = WeatherClient()

    assert client.latitude == DEFAULT_LATITUDE
    assert client.longitude == DEFAULT_LONGITUDE

def test_build_params():
    return

def test_fetch():
    return

def test_get_forecast_raw():
    return

def test_get_forecast_df():
    return

def test_raise_client_error():
    return