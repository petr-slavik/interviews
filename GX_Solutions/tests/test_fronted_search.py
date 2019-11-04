import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

# Nastaveni ktere bude pouzito ve vsech testech
# Urci URL, implicitni cekani, maximalizaci browseru a zavrreni browseru nakonci
@pytest.fixture
def browser():
    global driver
    driver = Chrome()
    driver.get(r"https://hdart.cz/")
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.close()


################################ TESTOVACI CAST ###############################

def test_main_page_load(browser):
    # Verify if login page for administration is loaded
    assert driver.current_url == r"https://www.hdart.cz/"
    # Overuje zda odpovida URL
    assert driver.title == "HD Art - Obrazy pro Váš interiér"
    # Overuje zda sedi title


@pytest.mark.parametrize("hledany_autor, expected_dilo, position_of_link", [
    ("Picasso", "Guernica", 2),
    ("Monet", "Il giardino di Monet", 3),
    ("Flower", "Dove with flowers", 28)
    ])
    # Parametry pro testovani Search pole
    # Samotny test overi, zda pri hledani danneho autora vyhledavani vrati
    # dilo na konkretni pozici (Monet par. 3 je nastaven pro FAIL)
def test_search_field(browser, hledany_autor, expected_dilo, position_of_link):
    search_input = driver.find_element_by_name('q')
    # Priradi promene vyhledavaci pole
    search_button = driver.find_element_by_id('searchButton')
    # Priradi promene Vyhledavaci tlacitko
    search_input.send_keys(hledany_autor)
    # VLozi do vyhledavaciho pole jmeno hledaneho autora - napr. Picasso
    search_button.click()
    # Klikne na Search button
    assert expected_dilo in driver.find_element_by_xpath(f"//div[@id='content']/div[{position_of_link}]").text
    # Overi zda je ve vysledcich vyhledavani dilo na konkretni pozici
    # Napr. pri hledani Picasso je dilo Guernica na 2 miste ve vyhledavani
    # coz odpovida XPATH //div[@id='content']/div[2]


def test_nakupni_kosik(browser):
    # Otestuje vyhledani produktu, vybrani nekolika parametru - laminace, jineho rozmeru,
    # vlozeni zbozi do kosiku a odstraneni zbozi z kosiku
    search_input = driver.find_element_by_name('q')
    search_button = driver.find_element_by_id('searchButton')
    search_input.send_keys("Les Philoshophes II" + Keys.RETURN)
    # Vyhleda "Les Philoshophes II" produkt
    driver.find_element_by_xpath("//a[contains(text(),'Les Philoshophes II')]").click()
    # Klikne na link ve vysledku hledani obsahujici text "Les Philoshophes II"
    driver.find_element_by_xpath("//input[@id='eshopSelLaminovat']").click()
    # Vybere Checkbox "Laminovat"
    driver.find_element_by_xpath('id("eshop_right_part_container")/div[4]/ul[1]/li[2]').click()
    # Vybere Roundbox pro velikost 30x40 cm
    driver.find_element_by_xpath("//div[@id='eshop_to_cart_button']").click()
    # Klikne na pridani produktu do kosiku, pote by se mel zobrazit obsah kosiku
    assert driver.current_url == r"https://www.hdart.cz/kosik?new"
    # Overi zda URL odpovida nakupnimu kosiku s jednim vlozenym produktem
    assert "Nákupní košík" == driver.find_element_by_xpath("//div[@id='content']/h2").text
    # Overi zda sedi nadpis nakupniho kosiku, ktery je na strance v H2
    assert  "Les Philoshophes II" == driver.find_element_by_xpath('id("orderFirstPart")/div[@class="kosikItem"]/h3[1]').text
    # Overi zda je v nakupnim kosiku produkt, ktery byl do nej vlozen

    driver.find_element_by_xpath('id("orderFirstPart")/div[@class="kosikItem"]/div[@class="deleteItemFromCart"]').click()
    # Klikne na ikonu "X" pro odmazani produktu z nakupniho kosiku
    assert "V košíku nemáte žádné položky." == driver.find_element_by_xpath("//div[@id='infoNoItem']").text
    # Overi ze zbozi bylo z nakupniho kosiku odstraneno
    # A ze se zobrazi informace ze v kosiku neni zadna polozka

