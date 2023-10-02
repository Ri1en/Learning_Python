import get_weather


def test_write_to_db_by_save_weather(save_weather_in_test_function, read_weather_in_test_function):
    settings = get_weather.PostgresSettings()
    db = get_weather.PostgresDb(settings)
    weather_object = get_weather.Weather(db, settings, get_weather.get_weather_from_api)
    data_to_save = save_weather_in_test_function(
        'Moscow', 13.5, 14.5, 12.5, [{'main': 'rain', 'description': 'heavy rain'}]
    )
    weather_object.save_weather_data(data_to_save)
    read_weather = read_weather_in_test_function()[0]
    assert read_weather[1] == data_to_save.city
    assert read_weather[2] == data_to_save.temp
    assert read_weather[3] == data_to_save.temp_max
    assert read_weather[4] == data_to_save.temp_min
    assert read_weather[5] == data_to_save.weather[0]['main']
    assert read_weather[6] == data_to_save.weather[0]['description']
