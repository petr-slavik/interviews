import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
# import pytest frameworku a Selenia + Chrome webdriveru

#Fixutre je nastaveni, bude pouzito v kazdem z testu, kterym je predano jako parametr
@pytest.fixture
def browser():
    global driver, USER, PASS, MESSAGE_NO_PASSWORD, MESSAGE_NO_USER, MESSAGE_NO_CREDENTIALS, MESSAGE_WRONG_CREDENTIALS, user_input, pass_input, submit_button
    driver = Chrome() 
    # Pro testovaci ucely jsem pouzil Chrome,
    # na testovacim stroji mam webdrover v PATH, jinak bych mu zadal cestu. 
    # Pro dalsi testovani by se testum predvaly i ostatni drivery jako: 
    # EventFiringWebDriver, FirefoxDriver, HtmlUnitDriver, InternetExplorerDriver, Edge webdriver,
    # PhantomJSDriver, RemoteWebDriver, SafariDriver, Opera driver, iOS driver, Android driver
    driver.get(r"https://hdart.cz/hd-admin/")
    driver.maximize_window()
    driver.implicitly_wait(10)
    # mplicity_wait metoda se postara o to, aby se nacetly vsechny prvky na strance
    # v tomto pripade mam nastaveno 10s, ale doba cekani je takova, nez se vsechny prvny nactou,
    # 10s je horni limit. Pokud se stranka nacte drive, tak cekani dale nepokracuje

    # promene pro nasledujici testy 
    # (vetsinou se to nedava do fixtures, ale do externiho confing.json souboru, 
    # ale pro prehlednost jsem to nechal tady)
    USER = "testovaci jmeno"
    PASS = "testovaci heslo"
    MESSAGE_NO_PASSWORD = "Není vyplněna položka HesloZZZZZ"
    MESSAGE_NO_USER = "Není vyplněna položka Login.XXXX"
    MESSAGE_NO_CREDENTIALS = "\nNení vyplněna položka Login.\nNení vyplněna položka Heslo."
    MESSAGE_WRONG_CREDENTIALS = "Zadané přihlašovací údaje nejsou správné."

    user_input = driver.find_element_by_id('login')
    pass_input = driver.find_element_by_id('pass')
    submit_button = driver.find_element_by_class_name('submit.sendButton')

    yield driver
    # Iterator vraci objekt browseru

    driver.close()
    # Po ukonceni testu zavre browser.
    # V tomto pripade je pro kazdy test pouzita nova instance browseru

################################ TESTOVACI CAST ###############################


def test_login_admin_load(browser):
    # Verify if login page for administration is loaded
    assert driver.current_url == r"https://hdart.cz/hd-admin/"
    # Overuje zda odpovida URL
    assert driver.title == "H&D ART admin ~ Přihlášení"
    # Overuje zda sedi title
    
def test_login_without_password(browser):
    # Verify login without password
    user_input.send_keys(USER + Keys.RETURN)
    # Zada jmeno uzivatele a odesle ENTER
    login_error_message = driver.find_element_by_class_name('alert.marb0').text
    # Do promene nacte string z elementu urcenem class name
    assert MESSAGE_NO_PASSWORD in login_error_message
    # Overi zda sedi chybove hlaseni pro chybejici heslo

def test_login_without_user_name(browser):
    # Verify login without username
    pass_input.send_keys(PASS + Keys.RETURN)
    # Zada heslo a odesle ENTER
    login_error_message = driver.find_element_by_class_name('alert.marb0').text
    # Do promene nacte string z elementu urcenem class name
    assert MESSAGE_NO_USER in login_error_message
    # Overi zda sedi chybove hlaseni pro chybejici jmeno uzivatele

def test_login_without_credentials(browser):
    # Verify login without credentials
    submit_button.click()
    login_error_message = driver.find_element_by_class_name('alert.marb0').text
    # Do promene nacte string z elementu urcenem class name
    assert MESSAGE_NO_CREDENTIALS in login_error_message
    # Overi zda sedi chybove hlaseni pro chybejici jmeno uzivatele a heslo

def test_login_with_wrong_credentials(browser):
    # Verify login using wrong credentials
    user_input.send_keys(USER)
    pass_input.send_keys(PASS)
    # Vlozi jmeno uzivatele a heslo
    submit_button.click()
    # Klikne na tlacitko "PRIHLASIT SE"
    login_error_message = driver.find_element_by_class_name('alert.marb0').text
    # Do promene nacte string z elementu urcenem class name
    assert MESSAGE_WRONG_CREDENTIALS in login_error_message
    # Overi zda sedi chybove hlaseni pro spatne prihlasovaci udaje

    
def test_login_with_correct_credentials(browser):
    # Verify login using correct credentials
    user = "xslavik"
    password = "Password"
    # Do promenych jsou ulozeny funkcni prihlasovaci udaje
    user_input.send_keys(user)
    pass_input.send_keys(password)
    submit_button.click()
    # Vlozi jmeno uzivatele, heslo a klikne na tlacitko "PRIHLASIT SE"
    assert "Úvodní strana administrace" in driver.title
    # Overi zda se po zadani spravnych prihlasovacich udaju zobrazi stranka administrace
    # Overeni se provede skrz cast textu ktery se nachazi v title

