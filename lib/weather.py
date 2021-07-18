"""
    This program is to get the actually weather data of the given destination

    -> following arguments in the dict (you can get them by running the function get_item in class Weather)

        1. 'reference_time':             give you the seconds to this point since 1970: 00:00 back
        2. 'sunset_time':                give you the seconds to this point since 1970: 00:00 back
        3. 'sunrise_time':               give you the seconds to this point since 1970: 00:00 back
        4. 'clouds':                     give you a percent number of the clouds cover
        5. 'rain':                       is a dict with: duration of the rain and m3 per hour
        6. 'snow':                       is a dict with: is a dict but not tested jet what it contain!
        7. 'wind':                       is a dict with: speed, deg, gust
        8. 'humidity':                   is a percent value of the humidity
        9. 'pressure':                   is a dict with: press. sea_level
        10. 'temperature':               is a dict with: temp, temp_kf, temp_max, temp_min, feels_like -> test in main()
        11. 'status':                    is a string: example: Rain
        12. 'detailed_status':           is the detailed status: example: light rain
        13. 'weather_code':              is a value of the actually weather
        14. 'weather_icon_name':         is the id of the actually weather
        15. 'visibility_distance':       is a value -> in german: Sichtweite
        16. 'dewpoint':                  is a value -> in german: Taupunkt
        17. 'humidex':                   is a value -> in german: Humidex
        18. 'heat_index':                is a value -> in german: Hitzeindex
        19. 'utc_offset':                is a value -> in german: utc_offset
        20. 'uvi':                       is a value -> in german: UV-Index
        21. 'precipitation_probability': is a percent value: -> in german Niederschlagswarscheinlichkeit

"""

__date__ = '08.07.2021'
__completed__ = '10.07.2021'
__work_time__ = 'about 8 Hours'
__author__ = 'Christof Haidegger'
__version__ = '1.2'
__licence__ = 'Common Licence'
__debugging__ = 'Christof Haidegger'

from inspect import currentframe
from termcolor import colored
import pyowm
import sys


def get_line_number():
    """

        :return: the current line number
        """
    cf = currentframe()
    return cf.f_back.f_lineno


class Weather:
    """
        Class to get the actually weather data of the given destination
    """
    # to count warnings:
    warning_counter = 0

    def __init__(self, destination):
        """

        :param destination: place for the weather check
        """
        self.weather_data = None
        self.destination = destination
        self.__ApiKey__ = 'acf332399352867a4d3b1d80b0bed26f'

        self._fill_weather_data()

    def _fill_weather_data(self):
        """

        :return: create a dict of the weather data
        :raises: [Error] Message, when there is no Internet connection -> return None
        """
        open_wm_map = pyowm.OWM(self.__ApiKey__)
        mgr = open_wm_map.weather_manager()
        try:
            try:
                weather = mgr.weather_at_place(self.destination)
            except (pyowm.commons.exceptions.NotFoundError, pyowm.commons.exceptions.TimeoutError,
                    pyowm.commons.exceptions.APIRequestError) as e:
                print('[Weather: Error: ' + str(type(self).warning_counter) + ' in Line: ' + str(get_line_number())
                      + '] ', e, '-> return None', file=sys.stderr)
                return None
            self.weather_data = weather.weather.to_dict()
        except pyowm.commons.exceptions.InvalidSSLCertificateError:
            print('[Weather: Error in Line: ' + str(get_line_number()) + '] No internet connection!', file=sys.stderr)
            return None

    def calc_kelvin_2_celsius(self, temp, comma=2):
        """

        :param temp:  temp in °k
        :param comma: comma values -> default is 2
        :return:      the temp in celsius format with the given float point

        :raise:       [Warning] when there is actually no weather data collected
        """
        if self.weather_data is None:
            print(colored('[Weather: Warning: ' + str(type(self).warning_counter)
                  + ' in Line: ' + str(get_line_number())
                  + '] No weather data is collected! Do not only try random values!', 'yellow'))
            type(self).warning_counter += 1
        return round(temp - 273.15, comma)

    def calc_kelvin_2_fahrenheit(self, temp, comma=2):
        """

        :param temp:   temp in °k
        :param comma: comma values -> default is 2
        :return:      the temp in fahrenheit format with the given float point

        :raise:       [Warning] when there is actually no weather data collected
        """
        if self.weather_data is None:
            print(colored('[Weather: Warning: ' + str(type(self).warning_counter) + ' in Line: ' + str(get_line_number()) +
                  '] No weather data is collected! Do not only try random values!', 'yellow'))
            type(self).warning_counter += 1
        return round((temp - 273.15) * 9/5 + 32, comma)

    def get_item(self, *args):
        """

        :param args: args -> tuple with the items
        :return:     the values of the wished item

        :raise:     Error when to many or to less arguments
        """

        if self.weather_data is None:
            print('[Weather: Error in Line: ' + str(get_line_number()) +
                  '] No weather information collected', file=sys.stderr)
            return None
        if args[0] == 'temperature':
            if len(args) == 3:
                if args[2] == 'kelvin':
                    return self._get_dict(args[0])[args[1]]
                elif args[2] == 'celsius':
                    return self.calc_kelvin_2_celsius(self._get_dict(args[0])[args[1]])
                elif args[2] == 'fahrenheit':
                    return self.calc_kelvin_2_fahrenheit(self._get_dict(args[0])[args[1]])
                else:
                    print('[Weather: Error in Line: ' + str(get_line_number()) +
                          '] temperature scale [args[2]] had to be kelvin, celsius or fahrenheit',
                          file=sys.stderr)
                    return None
            else:
                print('[Weather: Error in Line: ' + str(get_line_number()) +
                      '], param temperature had to contain three arguments to unpack '
                      'like: ("temperature", "temp_max", "celsius")', file=sys.stderr)
                return None
        elif len(args) == 2:
            return self._get_dict(args[0])[args[1]]
        elif len(args) == 1:
            return self._get_dict(args[0])
        else:
            print('[Weather: Error in Line: ' + str(get_line_number()) + '] bad arguments: ' +
                  str(args), file=sys.stderr)

    def _get_dict(self, item='temperature'):
        """

        :param item: item of the dict to take
        :return:     the contained items in the dict

        ':raises:    KeyError when a unknown argument is given and stop the program
        """
        try:
            return self.weather_data[item]
        except KeyError:
            print('[ Weather: Key Error in Line: ' + str(get_line_number()) + '] bad argument: ' + str(item),
                  file=sys.stderr)
            sys.exit(-1)


def main():
    """

    It is to test the program
    """
    w = Weather('Madrid')
    item = w.get_item('temperature', 'feels_like', 'celsius')
    print(item)


if __name__ == '__main__':
    main()
