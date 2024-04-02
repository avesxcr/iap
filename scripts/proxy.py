import logging
import os
import zipfile

from inst_poster.models import ProxyCredentials

logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
log_file_path = os.path.join(os.path.dirname(__file__), 'proxy_log.txt')
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class ProxyZipper:

    def __init__(self):

        self.path = os.path.dirname(os.path.realpath(__file__))
        self.proxy_data = ProxyCredentials.objects.first()

    def main(self):
        """
        Main
        """

        self.remove_old_archive_with_proxy()
        self.change_proxy_data()
        self.create_zip_with_proxy()
        return


    def change_proxy_data(self):
        """
        Change proxy data
        """
        try:
            with open(f"{self.path}/proxy/background.js", 'r') as file:
                lines = file.readlines()

            proxy_ip_port = self.proxy_data.proxy_ip.split(':')
            lines[5] = f"host: '{proxy_ip_port[0]}',\n"
            lines[6] = f"port: parseInt({proxy_ip_port[1]})\n"
            lines[17] = f"username: '{self.proxy_data.proxy_login}',\n"
            lines[18] = f"password: '{self.proxy_data.proxy_pass}'\n"

            with open(f"{self.path}/proxy/background.js", 'w') as file:
                file.writelines(lines)

            logger.info(f"Данные от прокси успешно изменены. IP:{self.proxy_data.proxy_ip}. Login: {self.proxy_data.proxy_login}. Password: {self.proxy_data.proxy_pass}")
            return
        except:
            logger.error(f"Произошла ошибка! Не удалось изменить данные от прокси.")

    def remove_old_archive_with_proxy(self):
        """
        Removing old archive with proxy, if exists
        """

        file_path = os.path.join(self.path + '/proxy.zip')
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Старый архив с прокси {file_path} успешно удален.")
            return
        else:
            logger.error(f"Произошла ошибка! Невозможно удалить {file_path}.")

    def create_zip_with_proxy(self):
        """
        Creating zip with (new?) proxy data
        """

        directory = f"{self.path}/proxy"
        zip_file = f"{self.path}/proxy.zip"

        try:
            with zipfile.ZipFile(zip_file, 'w') as zipf:
                for foldername, _, filenames in os.walk(directory):
                    for filename in filenames:
                        filepath = os.path.join(foldername, filename)
                        zipf.write(filepath, os.path.relpath(filepath, directory))
            logger.info(f"Новый архив с прокси успешно создан.")
            return
        except:
            logger.error(f"Произошла ошибка! Невозможно создать архив с прокси.")

