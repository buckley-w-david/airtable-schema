try:
    import selenium
except ImportError as exc:
    raise ImportError('Please install the optional "selenium" extra dependencies')

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from airtable_schema import AirtableCredentials

WAIT_SECS_FOR_PAGE_LOAD = 15  # set higher/lower as needed for a slow webpage load

# from Kai_Curry
JS_SCRIPT_2 = """
return (
    JSON.stringify(
        _.mapValues(
            application.tablesById,
            table => _.set(
                _.omit(table, ['sampleRows']),
                'columns',
                _.map(
                    table.columns,
                    item => _.set(
                            item,
                            'foreignTable',
                            _.get(item, 'foreignTable.id')
                    )
                )
            )
        )
    )
)
"""


def fetch_schema(
    credentials: AirtableCredentials,
    app_id: str,
    driver: selenium.webdriver.remote.webdriver.WebDriver,
):

    driver.get("https://airtable.com/" + app_id + "/api/docs")

    user_field = driver.find_element_by_name("email")
    password_field = driver.find_element_by_name("password")

    user_field.send_keys(credentials.username)
    password_field.send_keys(credentials.password)
    password_field.submit()

    delay = WAIT_SECS_FOR_PAGE_LOAD  # seconds
    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fields"))
        )
    except TimeoutException:
        raise

    return driver.execute_script(JS_SCRIPT_2)
