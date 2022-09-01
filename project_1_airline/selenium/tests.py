import os
import pathlib
import unittest

from selenium import webdriver


def file_uri(filename):                                                                #uri je uopsteniji pojam od url, uri je putanja do filename; file_uri znaci vraca putanju do tog fajla
    return pathlib.Path(os.path.abspath(filename)).as_uri()

driver = webdriver.Chrome()                                                            #sluzi za vezu driver objekta unutar pythona i browsera

#driver = webdriver.Firefox()                              


class WebpageTests(unittest.TestCase):                                                 #klasa za testiranje izvedena iz unittest

    def test_title(self):                                                              #provera imena fajla
        driver.get(file_uri("counter.html"))                                           #driver uzima putanju do fajla counter.html
        self.assertEqual(driver.title, "Counter")                                      #tu putanju poredi i ako je ime isto sto i counter, vraca True 

    def test_increase(self):                                                           #provera klik dugmeta za increase
        driver.get(file_uri("counter.html"))
        increase = driver.find_element_by_id("increase")                               #uzima dugme "increase" koje u counter.html kroz javascript kod povecava za 1
        increase.click()                                                               #dugme increase klikne jednom (sam softver klikne), a mozemo kroz petlju da zadamo da klikce vise puta
        self.assertEqual(driver.find_element_by_tag_name("h1").text, "1")              #i proverava da li je novi izlaz h1 jednak 1 (sto ocekujemo)

    def test_baci_5(self):
        driver.get(file_uri("counter.html"))
        baci_5 = driver.find_element_by_id("baci_5")
        baci_5.click()
        self.assertEqual(driver.find_element_by_tag_name("h1").text, "5")

    def test_decrease(self):                                                           #provera klik dugmeta za decrease
        driver.get(file_uri("counter.html"))
        decrease = driver.find_element_by_id("decrease")
        decrease.click()
        self.assertEqual(driver.find_element_by_tag_name("h1").text, "-1")

    def test_multiple_increase(self):                                                  #test gde simuliramo kliktanje od vise puta
        driver.get(file_uri("counter.html")) 
        increase = driver.find_element_by_id("increase")
        for i in range(1000):                                                          #kroz petlju damo naredbu da klikce 1000x
            increase.click()
        self.assertEqual(driver.find_element_by_tag_name("h1").text, "1000")           #provera da li je posle 1000 klikova jednako 1000


if __name__ == "__main__":
    unittest.main()