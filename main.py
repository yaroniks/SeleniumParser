from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec


class SeleniumParser:
    def __init__(self):
        self._driver: WebDriver
        self._chrome_options = webdriver.ChromeOptions()
        self._chrome_options.page_load_strategy = 'eager'
        self._chrome_options.add_argument('--headless=new')
        self._chrome_options.add_argument('--incognito')
        self._chrome_options.add_argument('--no-sandbox')
        self._chrome_options.add_argument('--disable-gpu')
        self._chrome_options.add_argument('--disable-dev-shm-usage')
        self._chrome_options.add_argument("--disable-extensions")
        self._chrome_options.add_argument("--disable-plugins")
        self._chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self._chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36")

    def __enter__(self):
        # без докера
        service = Service(executable_path=ChromeDriverManager().install())
        self._driver = webdriver.Chrome(service=service, options=self._chrome_options)
        # с докером
        # self._driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub', options=self._chrome_options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._driver.quit()
        except:
            pass

    def parse_wildberries(self, product_name: str) -> list[dict]:
        """
        :return {
            'name': str,
            'cost' int,
            'star': float,
            'image': str,
        }
        """
        wait = WebDriverWait(self._driver, 5, poll_frequency=1)
        self._driver.get(f'https://www.wildberries.ru/catalog/0/search.aspx?search={product_name}')
        wait.until(ec.visibility_of_element_located((By.XPATH, "//div[@class='product-card-list']")))

        element = self._driver.find_element(By.XPATH, "//div[@class='product-card-list']")
        text = element.get_attribute("outerHTML")
        soup = BeautifulSoup(text, 'html.parser')
        items = soup.find_all('article')

        products = []
        for i in items:
            name = i.find('h2').text
            cost = i.find('ins').text
            try:
                star = i.find('span', class_='address-rate-mini').text
                star = float(star.replace(',', '.'))
            except:
                star = None
            image = i.find('img').get('src')
            products.append(
                {'name': name, 'cost': int(''.join(filter(str.isdigit, cost))), 'star': star, 'image': image}
            )

        return products

    def parse_yandex_market(self, product_name: str) -> list[dict]:
        """
        :return {
            'name': str,
            'cost' int,
            'star': float,
            'image': str,
        }
        """
        self._driver.implicitly_wait(1)
        self._driver.get(f'https://market.yandex.ru/search?text={product_name}')

        element = self._driver.find_element(By.XPATH, "//div[@class='_33Ftr']")
        text = element.get_attribute("outerHTML")
        soup = BeautifulSoup(text, 'html.parser')
        items = soup.find_all('article')

        products = []
        for i in items:
            try:
                name = i.find('span', role='link').get('title')
                cost_div = i.find('div', class_='tRz2a')
                cost = cost_div.find('span', class_='ds-text').text
                star = i.find('span', class_='ds-rating').text[:3]
                image = i.find('img').get('src')
                products.append(
                    {'name': name, 'cost': int(''.join(filter(str.isdigit, cost))), 'star': float(star.replace(',', '.')), 'image': image}
                )
            except:
                pass

        return products

    def parse_ozon(self, product_name: str) -> list[dict]:
        """
        :return {
            'name': str,
            'cost' int,
            'star': float,
            'image': str,
        }
        """
        self._driver.implicitly_wait(1)
        self._driver.get(f'https://www.ozon.ru/search/?text={product_name}')

        element = self._driver.find_element(By.XPATH, "//div[@id='contentScrollPaginator']")
        text = element.get_attribute("outerHTML")
        soup = BeautifulSoup(text, 'html.parser')
        items = soup.find_all('div', class_='tile-root')

        products = []
        for i in items:
            name = i.find('span', class_='tsBody500Medium').text
            cost = i.find('span', class_='c35_3_11-a1').text
            try:
                star = i.find('span', style='color:var(--textPremium);').text
                star = float(star.replace(',', '.'))
            except:
                star = None
            image = i.find('img').get('src')
            products.append(
                {'name': name, 'cost': int(''.join(filter(str.isdigit, cost))), 'star': star, 'image': image}
            )

        return products

    def parse_aliexpress(self, product_name: str) -> list[dict]:
        """
        :return {
            'name': str,
            'cost' int,
            'star': float,
            'image': str,
        }
        """
        self._driver.implicitly_wait(1)
        self._driver.get(f'https://aliexpress.ru/wholesale?SearchText={product_name}')

        element = self._driver.find_element(By.XPATH, "//div[@data-spm-protocol='i']")
        text = element.get_attribute("outerHTML")
        soup = BeautifulSoup(text, 'html.parser')
        items = soup.find_all('div', class_='red-snippet_RedSnippet__container__q0mlsu')

        products = []
        for i in items:
            name = i.find('div', class_='red-snippet_RedSnippet__title__q0mlsu').text
            cost = i.find('div', class_='red-snippet_RedSnippet__priceNew__q0mlsu').text
            star_div = i.find('div', class_='red-snippet_RedSnippet__trust__q0mlsu')
            star = star_div.find('span', class_='snippet-element_Element__item__1nwok2').text
            try:
                star = float(star.replace(',', '.'))
            except:
                continue
            image = i.find('img').get('src')
            products.append(
                {'name': name, 'cost': int(''.join(filter(str.isdigit, cost))), 'star': star, 'image': image}
            )

        return products

    def parse_yandex_images(self, search_text: str) -> str:
        self._driver.implicitly_wait(2)
        self._driver.get(f'https://yandex.ru/images/search?text={search_text}')

        try:
            element = self._driver.find_element(By.XPATH, "//div[@class='gdpr-popup-v3-button gdpr-popup-v3-button_id_all']")
            element.click()
        except:
            pass
        try:
            element = self._driver.find_element(By.XPATH, "//div[@class='SerpList']")
            element.click()
        except:
            return self.parse_yandex_images(search_text)

        search_text = element.get_attribute("outerHTML")
        soup = BeautifulSoup(search_text, 'html.parser')
        item = soup.find('div', class_='JustifierRowLayout-Item')
        return 'https:' + item.find('img').get('src')


# with SeleniumParser() as parser:
#     name = input('Введите название: ')
#     print(parser.parse_wildberries(name))
#     print(parser.parse_yandex_market(name))
#     print(parser.parse_ozon(name))
#     print(parser.parse_aliexpress(name))
#     print(parser.parse_yandex_images(name))
