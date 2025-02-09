import requests
import json

BASE_URLS = "https://catalog.onliner.by/sdapi/catalog.api/search/{}"

def get_products(section="products"):
    url = BASE_URLS.format(section)
    response = requests.get(url, params={"query": "edon", "page": "1", "limit": "50"})
    if response.status_code == 200:
            return response.json()
    raise RuntimeError(f"Was status code: {response.status_code}")


if __name__ == "__main__":
    try:
        data = get_products()
    except RuntimeError as err:
        print(err)
    else:
        result = []
        for el in data["products"]:
             result.append(
                  {
                       "name": el.get("name"),
                       "prices": el["prices"],
                       "link": el.get("url")
                  }
             )
        with open("result.json", "w") as file:
             json.dump(result, file, indent=4, ensure_ascii=False)
            