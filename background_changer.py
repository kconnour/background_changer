# Built-in imports
from datetime import date, datetime
import glob
import os

# TODO: See if I can make this work on non-Ubuntu OS
# TODO: Add an option to change this weekly/hourly so it's not locked into
#  daily
# TODO: Add an option to change wallpapers seasonally
# TODO: It'd be nice to auto set the crontab from Python
# TODO: See if this can be less fragile. It breaks if there are less than 7
#  images in the folder and it can't set a background to a non png/jpeg file
# TODO: A GUI would be nice


class BackgroundChanger:
    """ A BackgroundChanger object can change the desktop wallpapers. """
    def __init__(self):
        self.__image_loc_file = os.path.abspath('.imageloc.txt')
        self.pictures_Folder = self.__get_image_location()

    def __get_image_location(self):
        self.__make_file_if_nonexistent()
        return self.__get_first_line_of_file()

    def __make_file_if_nonexistent(self):
        if not os.path.exists(self.__image_loc_file):
            self.__make_imageloc_file()

    def __get_first_line_of_file(self):
        with open(self.__image_loc_file, 'r') as f:
            return f.readline()

    def __make_imageloc_file(self):
        path = input('Enter the absolute path of the folder containing '
                     'images: ')
        f = open(self.__image_loc_file, 'w+')
        f.write(path)

    def change_background(self):
        """ Change the background.

        Returns:
        -------
        None
        """
        daily_picture_filename = self.__get_daily_image_filename()
        self.__set_wallpaper(daily_picture_filename)
        print(f'Successfully changed wallpaper at {datetime.now()}.')

    def __get_daily_image_filename(self):
        return self.__get_images()[self.__get_weekday_number()]

    def __get_images(self):
        search_pattern = os.path.join(self.pictures_Folder, '*')
        return sorted(glob.glob(search_pattern))

    @staticmethod
    def __get_weekday_number():
        return int(date.today().strftime('%w'))

    @staticmethod
    def __set_wallpaper(image):
        cmd = f'gsettings set org.gnome.desktop.background picture-uri {image}'
        os.system(cmd)


if __name__ == '__main__':
    # This works as long as you have at least 7 pictures in a folder
    # Then add '0 0 * * * /path/to/python3 /path/to/script.py' to cron to
    # change it at midnight every day
    b = BackgroundChanger()
    b.change_background()
