import gspread
import random
import threading
import time

class Sheets:
    def __init__(self):
        self.gc = gspread.service_account(filename="creds.json")
        self.links = []
        self.get_all_links()

        thread = threading.Thread(target=self._autoupdate_links)
        thread.start()
    def get_all_links(self):
        sheet = self.gc.open("links")
        second_sheet = sheet.get_worksheet(2)
        self.links = second_sheet.col_values(1)
    def get_random_link(self, used_links=None):
        if used_links is None:
            used_links = set()
        else:
            used_links = set(used_links)


        available = list(set(self.links) - used_links)
        if not available:
            return []



        return random.choice(available)
    def _autoupdate_links(self):
        while True:
            print("Обновляю ссылки...")
            self.get_all_links()
            print(f"Загружено {len(self.links)} ссылок")
            time.sleep(3600)


