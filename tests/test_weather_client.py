from src.weather_client import WeatherClient, DEFAULT_LONGITUDE, DEFAULT_LATITUDE

def test_latitude_longitude_defaults():
    client = WeatherClient()

    assert client.latitude == DEFAULT_LATITUDE
    assert client.longitude == DEFAULT_LONGITUDE

