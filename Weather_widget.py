"""

    This file is to create a weather widget with the actually weather conditions

    -> you are able to change the size of it and the language

    Features:
        show: min temp, max temp, actually temp, feel temp
              status:      example: light rain
              wind:        show the actually wind speed
              humidity:    show the humidity in %
              clouds:      show the cloud rate in %
              destination: show the actually selected destination
              icon:        show a gif animated icon of the actually weather

    Easter Egg: -> The Weather Icon is a animated gif animation


"""


from lib import languages
from lib import weather
import Ctkinter as Ctk
import tkinter as tk


__date__ = '8.07.2021'
__completed__ = '16.07.2021'
__work_time__ = 'about 5 Hours'
__author__ = 'Christof Haidegger'
__version__ = '2.0'
__licence__ = 'Common Licence'
__debugging__ = 'Christof Haidegger'


def get_right_gif_path(status):
    """

    :param status: detailed status of the weather library
    :return: the path to the icon, the background color of the widget and the background color of the header
    """
    detailed_status_possibilities = ['sun', 'partly cloudy', 'scattered clouds', 'thunderstorm', 'mist',
                                     'broken clouds', 'rain', 'snow', 'overcast clouds', 'few clouds', 'clear sky',
                                     'light rain', 'drizzle', 'shower rain', 'moderate rain',
                                     'light intensity shower rain', 'haze', 'light intensity drizzle',
                                     'heavy intensity shower rain', 'light snow']

    gif_path_list = ['sun_t.gif', 'partly_cloudy_t.gif', 'scattered_clouds_t.gif',
                     'thunderstorm_t.gif', 'mist_t.gif', 'broken_clouds_t.gif', 'rain_t.gif', 'snow_t.gif',
                     'scattered_clouds_t.gif', 'partly_cloudy_t.gif', 'sun_t.gif', 'rain_t.gif', 'rain_t.gif',
                     'rain_t.gif', 'rain_t.gif', 'rain_t.gif', 'mist_t.gif', 'rain_t.gif', 'rain_t.gif', 'snow_t.gif']

    color_list = ['orange', 'yellow2', 'spring green', 'green2', 'deep sky blue', 'light sky blue', 'dodger blue',
                  'blue', 'green2', 'yellow2', 'orange', 'dodger blue', 'dodger blue', 'dodger blue', 'dodger blue',
                  'dodger blue', 'deep sky blue', 'dodger blue', 'dodger blue', 'blue']

    color_header_list = ['DarkOrange2', 'gold', 'green2', 'chartreuse2', 'cyan', 'deep sky blue', 'DodgerBlue3',
                         'medium blue', 'chartreuse2', 'gold', 'DarkOrange2', 'DodgerBlue3', 'DodgerBlue3',
                         'DodgerBlue3', 'DodgerBlue3', 'DodgerBlue3', 'cyan', 'DodgerBlue3', 'DodgerBlue3',
                         'medium blue']

    right_gif_and_color_index = detailed_status_possibilities.index(status)  # if ValueError -> no internet connection

    return 'icons/' + gif_path_list[right_gif_and_color_index], color_list[right_gif_and_color_index], \
           color_header_list[right_gif_and_color_index]


class Weather_widget:
    """
        To create the weather widget call the Class Weather Widget
    """
    def __init__(self, master, destination='Innsbruck', language='english', scale=('celsius', 'km/h')):
        """

        :param master: master -> Item where the weather widget should be placed
        :param destination:   -> village ore town where the weather should be collected
        :param language:      -> language on the weather widget
        :param scale:         -> is a tuple example: ('celsius', 'km/h') first is for the temp and second for the wind
        """
        self.destination = destination
        self.scale = scale
        self.change_to_language = languages.Language(file_path='languages/languages.txt', language=language)
        self.master = master

        status, temp, wind, humidity, cloud_index = self._get_actually_weather(scale)
        # status, temp, wind, humidity, cloud_index = 'sun nice', [25, 30, 23, 26], 4.1, 5, 50

        if status == 'DataCollectingError':
            print('Destination not found')
            return

        gif_path, bg, header_bg = get_right_gif_path(status)

        self.weather_widget = Ctk.CCanvas(master, bg=bg, size=(600, 300), corners='rounded', max_rad=100,
                                          outline=('', 0))
        # run function to place objects
        self.header_text = self._create_header_text(bg=header_bg, size=(300, 40), place=(28, 5))
        self.destination_lab = self._create_destination_label(bg=bg, size=(355, 60), place=(240, 60))
        self.logo = self._create_header_logo(bg=bg, size=(105, 35), place=(450, 2))

        self._create_gif_icon_temp_labels_info_labels(bg, gif_path, temp, status, wind, humidity, cloud_index)

    def _get_actually_weather(self, scale):
        """

        :param scale: scale for the temperature (could be celsius, fahrenheit or kelvin)
        :return: the items of the weather library -> to see als available items watch in the file weather.py
        """

        actually_weather = weather.Weather(self.destination)
        if actually_weather.weather_data is None:
            return 'DataCollectingError', None, None, None, None
        status = actually_weather.get_item('detailed_status')
        temp = [actually_weather.get_item('temperature', 'temp', scale[0]),
                actually_weather.get_item('temperature', 'temp_max', scale[0]),
                actually_weather.get_item('temperature', 'temp_min', scale[0]),
                actually_weather.get_item('temperature', 'feels_like', scale[0])]
        wind = actually_weather.get_item('wind', 'speed')
        humidity = actually_weather.get_item('humidity')
        cloud_index = actually_weather.get_item('clouds')

        if scale[1] == 'km/h':
            wind = wind * 1.609  # wind *1.609 for refactor mp/h -> km/h
        if temp[1] == temp[2]:
            temp[1] = temp[1] + 1

        wind = round(wind, 2)

        return status, temp, wind, humidity, cloud_index

    def _create_header_text(self, bg, size, place):
        """

        :param bg:    bg of the header
        :param size:  size of the header
        :param place: place for the header
        :return:      place the header widget on the given place
        """
        weather_widget_title = Ctk.CLabel(self.weather_widget, bg=bg, size=size,
                                          text=self.change_to_language.refactor('Weather forecast'), fg='white',
                                          font=('Constantia', 15), corner='rounded', max_rad=None, anchor='CENTRE')
        weather_widget_title.place(*place)

        return weather_widget_title

    def show_destination_error(self):
        self.destination_lab.destroy()
        self.destination_lab = self._create_destination_label(bg=self.weather_widget['background'],
                                                              size=(355, 60), place=(240, 60))

    def _new_destination(self, destination):
        """

        :param destination: the new destination
        : fill the weather widget with the new destination data
        """
        old_destination = self.destination
        self.destination = destination.get()
        status, temp, wind, humidity, cloud_index = self._get_actually_weather(self.scale)
        if status == 'DataCollectingError':
            self.destination = self.change_to_language.refactor('Destination not found')
            self._create_destination_label(bg=self.weather_widget['background'], size=(355, 60), place=(240, 60),
                                           fg='red')
            self.destination = old_destination
            self.weather_widget.after(1000, self.show_destination_error)
            return

        self.gif_icon.destroy()
        self.temp_labels.destroy()
        self.info_labels.destroy()
        self.logo.destroy()
        self.header_text.destroy()

        gif_path, bg, header_bg = get_right_gif_path(status)
        self.logo = self._create_header_logo(bg=bg, size=(105, 35), place=(450, 2))
        self.header_text = self._create_header_text(bg=header_bg, size=(300, 40), place=(28, 5))
        self.logo.get_canvas().config(bg=bg)

        self.weather_widget.config(bg=bg)

        self.destination_lab.config(bg=bg)
        self.destination_lab.get_canvas().config(bg=bg)

        self.header_text.get_canvas().config(bg=bg)
        self._create_gif_icon_temp_labels_info_labels(bg, gif_path, temp, status, wind, humidity, cloud_index)

    def _create_gif_icon_temp_labels_info_labels(self, bg, gif_path, temp, status, wind, humidity, cloud_index):
        """

        :param bg:          background for the items
        :param gif_path:    path to the gif animation
        :param temp:        actually temperature
        :param status:      actually status
        :param wind:        actually wind speed
        :param humidity:    actually humidity
        :param cloud_index: actually percent value of the clouds
        :return:            draw the items on the weather widget
        """
        self.gif_icon = self._create_weather_icon(bg=bg, size=(180, 160), place=(20, 70), gif_path=gif_path)
        self.temp_labels = self._create_temperature_labels(bg=bg, size=(345, 150), place=(250, 120), temp=temp,
                                                           scale=self.scale)
        self.info_labels = self._create_info_labels(bg=bg, size=(510, 30), place=(50, 265),
                                                    status=self.change_to_language.refactor(status), wind=wind,
                                                    humidity=humidity, cloud_index=cloud_index, scale=self.scale)

    def _create_destination_label(self, bg, size, place, fg='black'):
        """

        :param bg:    bg of the destination label
        :param size:  size of the destination label
        :param place: place for the destination label
        :return:      place the destination label on the given place
        """
        destination_label = Ctk.CLabel(self.weather_widget, bg=bg, size=size, text=self.destination, fg=fg,
                                       font=('Constantia', 20, 'bold'), corner='rounded', max_rad=None, anchor='NW',
                                       variable_text=True, enter_hit=(True, self._new_destination))
        destination_label.place(*place)

        return destination_label

    def _create_header_logo(self, bg, size, place):
        """

        :param bg:    bg of the icon logo (it is transparent)
        :param size:  size of the icon
        :param place: place for the icon
        :return:      place the icon on the given place
        """
        pixel_boy_logo = Ctk.CCanvas(self.weather_widget, bg=bg, size=size, corners='rounded', max_rad=None,
                                     outline=('', 0))
        pixel_boy_logo.create_image(corner='angular', bg=bg, width=size[0] - 13, height=size[1] - 13,
                                    pos=(int(size[0] / 2), int(size[1] / 2)), image_path='icons/logo.png',
                                    transparent=True)

        pixel_boy_logo.place(*place)

        return pixel_boy_logo

    def _create_weather_icon(self, bg, size, place, gif_path):
        """

        :param bg:       bg of the weather icon
        :param size:     size of the weather icon
        :param place:    place for the weather icon
        :param gif_path: path to the weather icon
        :return:         place the weather icon on the given place
        """
        gif_weather_icon = Ctk.CCanvas(self.weather_widget, bg=bg, size=size, corners='angular')
        gif_weather_icon.create_gif(gif_path=gif_path, corner='angular',
                                    size=(size[0] - 20, size[1] - 20),
                                    pos=(int(size[0] / 2), int(size[1] / 2)),
                                    set_half_gif_time=False, transparent=True)
        gif_weather_icon.place(*place)

        return gif_weather_icon

    def _create_info_labels(self, bg, size, place, status, wind, humidity, cloud_index, scale):
        """

        :param bg:          bg of the info label
        :param size:        size of the info label
        :param place:       place of the info label
        :param status:      status string from the _get_actually_weather function
        :param wind:        wind value from the _get_actually_weather function
        :param humidity:    humidity value from the _get_actually_weather function
        :param cloud_index: cloud_index from the _get_actually_weather function
        :param scale:       scale for the given data (it is a tuple like ('celsius', 'km/h)
        :return:            place the info labels on the given place
        """
        background_canvas = Ctk.CCanvas(self.weather_widget, bg=bg, size=size, corners='rounded', max_rad=None,
                                        outline=('', 0))
        background_canvas.place(*place)

        texts = ['Status: ' + str(status),
                 'Wind: ' + str(round(wind, 1)) + scale[1],
                 self.change_to_language.refactor('Humidity') + ': ' + str(humidity) + '%',
                 self.change_to_language.refactor('Clouds') + ': ' + str(cloud_index) + '%']
        x_po = 0
        for counter, text in enumerate(texts):
            info_label = Ctk.CLabel(background_canvas, bg=bg, size=(None, 30), text=text, fg='black',
                                    font=('Sans', 10), corner='angular', max_rad=None, outline=('', 0), anchor='NW')
            info_label.place(x=x_po, y=1)
            x_po += int(info_label.get_text_len_in_px() + 5)

        return background_canvas

    def _create_temperature_labels(self, bg, size, place, temp, scale):
        """

        :param bg:     background of the temperature labels
        :param size:   size of the temperature labels
        :param place:  place fot the temperature labels
        :param temp:   temp to place on the label
        :param scale:  scale (°C, °F, °K) are available
        :return:       the temperature labels
        """
        background_canvas = Ctk.CCanvas(self.weather_widget, bg=bg, size=size, corners='angular', max_rad=None,
                                        outline=('', 0))
        background_canvas.place(*place)
        if scale[0] == 'celsius':
            temp_scale = '°C'
        elif scale[0] == 'fahrenheit':
            temp_scale = '°F'
        else:
            temp_scale = '°K'
        actual_temp = Ctk.CLabel(background_canvas, bg=bg, size=(300, 80),
                                 text=str(int(temp[2])) + ' - ' + str(int(temp[1])) + temp_scale, fg='white',
                                 font=('Sans', 50), corner='angular', max_rad=None, outline=('', 0),
                                 anchor='NW')
        actual_temp.place(x=0, y=10)

        background_canvas.create_line(0, 93, 300, 93, fill='white', width=1)

        for x_pos, text in zip([45, 155], [self.change_to_language.refactor('Actually') + ': ' + str(temp[0]) +
                                           temp_scale,
                                           self.change_to_language.refactor('Feels like') + ': ' +
                                           str(temp[3]) + temp_scale]):
            info_label = Ctk.CLabel(background_canvas, bg=bg, size=(120, 30), text=text, fg='black',
                                    font=('Sans', 10), corner='angular', max_rad=None, outline=('', 0), anchor='NW')
            info_label.place(x=x_pos, y=94)

        return background_canvas


def main():
    """

    : To test the Weather_widget Class run this function
    """
    root = tk.Tk()
    root.config(bg='white')
    root.geometry("800x450")
    new_weather = Weather_widget(root, destination='Innsbruck', language='german', scale=('celsius', 'km/h'))
    new_weather.weather_widget.pack(pady=50)
    root.mainloop()

    return 0


if __name__ == '__main__':
    main()
