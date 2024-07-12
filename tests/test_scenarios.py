import pytest
from pages.sbis_page import SbisPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from utils import logger, CURRENT_REGION


@pytest.mark.first_scenario
def test_first_scenario(driver):
    sbis = SbisPage(driver)

    sbis.open()

    # Переходим в контакты
    sbis.go_to_contacts()
    try:
        WebDriverWait(driver, 10).until(
            lambda driver: sbis.driver.find_element(*sbis.TENSOR_BANNER).is_displayed()
        )
    except TimeoutException:
        logger.error("Баннер TENSOR не отобразился в течение 10 секунд")

    # Кликаем по банеру и переключаем вкладку
    sbis.click_tensor_banner()
    sbis.switch_to_new_tab()
    assert driver.current_url == "https://tensor.ru/", (
        "Редирект не соответствует ТЗ")

    sbis.wait_for_block_content()
    block = sbis.driver.find_elements(*sbis.BLOCK_CONTENT)
    assert len(block) > 0, "Блок 'Сила в людях' не найден на странице"

    sbis.click_about_link()
    sbis.wait_for_about_page()
    assert driver.current_url == "https://tensor.ru/about", (
        "Редирект не соответствует ТЗ")

    sbis.check_photos_dimensions()


@pytest.mark.second_scenario
def test_second_scenario(driver):
    sbis = SbisPage(driver)

    sbis.open()
    sbis.go_to_contacts()

    # Определяем фактический регион, который показан на странице
    actual_region = sbis.get_region_label()
    assert actual_region.text == CURRENT_REGION, (
        f"Регион не совпадает. Ожидалось '{CURRENT_REGION}', "
        f"получено '{actual_region.text}'")

    # Получаем список партнеров
    partners_list = sbis.get_partners_list()
    assert len(partners_list) > 0, "Список партнеров не найден на странице"

    # Кликаем по новому региону
    actual_region.click()
    sbis.selet_region()
    sbis.wait_for_region_change(sbis.NEW_REGION)

    # Повторно получаем список партнеров после смены региона
    new_partners_list = sbis.get_partners_list()
    assert len(new_partners_list) > 0 and new_partners_list != partners_list, (
        "Список партнеров не обновился после смены региона")

    # Проверяем URL страницы и заголовок
    expected_url_contains = "contacts/41-kamchatskij-kraj"
    assert expected_url_contains in driver.current_url, (
        f"URL страницы не содержит '{expected_url_contains}',"
        f"текущий URL: '{driver.current_url}'")

    assert sbis.NEW_REGION in driver.title, (
        f"Title страницы не содержит выбранный регион '{sbis.NEW_REGION}'")
