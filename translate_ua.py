from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from in_out_word import InOut


class Translate(InOut):

    @staticmethod
    def lang_search(lang_sear, lang_sel: str, driver) -> None:
        # select options "more"
        lang_sear.select_by_value('more')
        # will select  original's language
        driver.find_element(By.ID, lang_sel).click()

    def select_language(self, inl: str, out: str, driver) -> None:
        lang = ['en', 'ru', 'uk']
        # search ID for button original's language
        lang_in = Select(driver.find_element(By.ID, "LangFrom"))
        # search ID for button's select language translate
        lang_out = Select(driver.find_element(By.ID, "LangTo"))
        if inl not in lang:
            self.lang_search(lang_in, inl, driver)
        else:
            lang_in.select_by_value(inl)
        if out not in lang:
            self.lang_search(lang_out, out, driver)
        else:
            lang_out.select_by_value(out)

    @staticmethod
    def loading_text(text, driver) -> str:
        # search field for the original text
        id_text_input = driver.find_element(By.ID, "SrcTxt")
        # enter text in field
        id_text_input.send_keys(text)
        # search of translate button
        element = driver.find_element(By.ID, "Traslate")
        # creating chain of actions
        action = ActionChains(driver)
        # running chain of actions
        action.click(element).perform()
        # wait loading translate
        time.sleep(2)
        # search of field output
        id_text_out = driver.find_element(By.CLASS_NAME, "DstText")
        # driver.find_element(By.ID, "SrcTxt")
        return id_text_out.text

    def translated(self, text_in: tuple) -> None:
        # create driver, delete cookies
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("prefs", {"profile.block_third_party_cookies": True,
                                                         "profile.default_content_setting_values.cookies": 2})
        driver = webdriver.Chrome(chrome_options=chrome_options)
        # connect to site
        driver.get("http://translate.ua/ru/on-line")
        # search frame
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')
        # connect to frame
        driver.switch_to.frame(iframe[0])
        # switching/select language
        self.select_language(self.orig, self.transl, driver)
        temp: list =[]
        out_text: list = []
        for ind, length_ in enumerate(text_in[1]):
            if length_ == 1:
                temp_text = self.loading_text(text_in[0][ind], driver)
                out_text.append(temp_text)
                id_text_input = driver.find_element(By.ID, "SrcTxt")
                id_text_input.clear()
            else:
                for text_temp in text_in[0][ind]:
                    temp_text = self.loading_text(text_temp, driver)
                    temp.append(temp_text)
                    id_text_input = driver.find_element(By.ID, "SrcTxt")
                    id_text_input.clear()
                out_text.append('.'.join(temp))
        self.word_write(out_text)
        driver.close()
