import gspread
import random
import threading
import time

class Sheets:
    def __init__(self):
        self.gc = gspread.service_account(filename="creds.json")
        self.links = []
        self.reviews = []
        self.get_all_links()
        self.get_all_reviews()

        thread = threading.Thread(target=self._autoupdate_links)
        thread2 = threading.Thread(target=self._autoupdate_reviews)
        thread.start()
        thread2.start()
    def get_all_links(self):
        sheet = self.gc.open("links")
        second_sheet = sheet.get_worksheet(2)
        self.links = second_sheet.col_values(1)

    def get_all_reviews(self):
        sheet = self.gc.open("links")
        review_sheet= sheet.get_worksheet(3)
        self.reviews = review_sheet.col_values(1)

    def get_one_review(self, used_reviews=None):
        if used_reviews is None:
            used_reviews = set()
        else:
            used_reviews = set(used_reviews)

        available = list(set(self.reviews) - used_reviews)
        if not available:
            return []
        print("Беру случайный отзыв")
        return random.choice(available)


    def get_random_link(self, used_links=None):
        if used_links is None:
            used_links = set()
        else:
            used_links = set(used_links)


        available = list(set(self.links) - used_links)
        if not available:
            return []



        return random.choice(available)
    def _autoupdate_reviews(self):
        while True:
            print("Обновляю отзывы...")
            self.get_all_reviews()
            print(f"Загружено {len(self.reviews)} отзывов")
            time.sleep(3600)
    def _autoupdate_links(self):
        while True:
            print("Обновляю ссылки...")
            self.get_all_links()
            print(f"Загружено {len(self.links)} ссылок")
            time.sleep(3600)



