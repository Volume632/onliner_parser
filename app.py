import requests
import csv

BASE_URLS = "https://catalog.onliner.by/sdapi/catalog.api/search/{}"

def get_all_products(section="products"):
    page = 1
    all_products = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    while True:
        url = BASE_URLS.format(section)
        params = {"query": "Edon", "page": str(page), "limit": "100"}

        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code != 200:
            raise RuntimeError(f"Ошибка! Сервер вернул код: {response.status_code}")
        
        data = response.json()
        products = data.get("products", [])

        if not products:  # Если товаров больше нет – выходим
            break

        all_products.extend(products)
        print(f"📦 Загружено товаров: {len(all_products)}")  # Отображаем прогресс

        page += 1  # Переход на следующую страницу

    return all_products

if __name__ == "__main__":
    try:
        products = get_all_products()
    except RuntimeError as err:
        print(err)
    else:
        csv_filename = "result.csv"

        with open(csv_filename, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["Название", "Цена min (BYN)", "Цена max (BYN)", "Ссылка"])

            for el in products:
                name = el.get("name", "Нет данных")

                prices = el.get("prices") or {}  # Если "prices" == None → делаем пустой словарь
                price_min = prices.get("price_min", {}).get("amount", "Нет цены")
                price_max = prices.get("price_max", {}).get("amount", "Нет цены")

                link = el.get("html_url", "Нет ссылки")

                writer.writerow([name, price_min, price_max, link])

        print(f"✅ Загружено всего {len(products)} товаров!")
        print(f"📄 Данные сохранены в {csv_filename} (Кириллица отображается корректно!)")
