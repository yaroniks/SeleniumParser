# Парсер маркетплейсов на Selenium

Example usage:
```python
from SeleniumParser import SeleniumParser

with SeleniumParser() as parser:
    products = parser.parse_wildberries('куртка')

for product in products:
    print(product["name"], product["cost"])

```

| Сайт          | Статус работы парсера |
|:--------------|:---------------------:|
| Wildberries   |           ✅           |
| Яндекс Маркет |           ✅           |
| OZON          |           ✅           |
| AliExpress    |           ❌           |
| Yandex Images |           ✅           |
| Пятёрочка     |           ⌛           |
| Магнит        |           ⌛           |

Последняя проверка: 02.12.2025
