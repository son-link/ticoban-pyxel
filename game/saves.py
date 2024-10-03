import sys
import json
from os import path, remove, mkdir

__dir = ''
if getattr(sys, 'frozen', False):
    __dir = path.dirname(sys.executable)
elif __file__:
    __dir = path.dirname(__file__)

SAVES_DIR = path.join(__dir, 'saves')


class Saves:
    @staticmethod
    def open(filename: str):
        """Opens a save file and returns its contents.

        Args:
            filename (str): The name, without extension, of the saving file

        Returns:
            dict: A dictionary with the contents of the file, or None if the contents cannot be read or parsed
        """
        savefile = path.join(SAVES_DIR, f'{filename}.json')
        if (path.isfile(savefile)):
            with open(savefile, 'r', encoding='utf8') as fp:
                try:
                    content = json.load(fp)
                    fp.close()
                    return content
                except json.JSONDecodeError:
                    return None
        else:
            return None

    @staticmethod
    def save(data: any, filename: str):
        """Save the dictionary passed by the data parameter in the file with the name passed by filename, without extension, in JSON format.

        Args:
            data (dict): The data to be saved
            filename (str):  The name, without extension, of the saving file

        Returns:
            bool: Whether or not the file was saved correctly
        """
        savefile = path.join(SAVES_DIR, f'{filename}.json')

        # First we check if the directory where the files are stored does not exist, if not, we create it.
        if not path.isdir(SAVES_DIR):
            mkdir(SAVES_DIR, 777)

        with open(savefile, 'w', encoding='utf8') as fp:
            try:
                json.dump(data, fp)
                fp.close()
                return True
            except TypeError:
                return False

        return False

    @staticmethod
    def delete(filename: str):
        """Delete a save file

        Args:
            filename (str): The name, without extension, of the saving file

        Returns:
            bool: Whether or not the file was removed correctly
        """
        savefile = path.join(SAVES_DIR, f'{filename}.json')
        if (path.isfile(savefile)):
            try:
                remove(savefile)
                return True
            except OSError:
                return False
