from pprint import pprint
from sys import version_info
from time import sleep
from time import time
import typing

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

WAIT_SECS_FOR_PAGE_LOAD = 15  # set higher/lower as needed for a slow webpage load

# from Chester_McLaughlin
JS_SCRIPT_1 = """
var myAT = {
id:window.application.id,
name:window.application.name,
tables:[]
};

for (let table of window.application.tables){
var mytable = {
id:table.id,
isEmpty:table.isEmpty,
name:table.name,
nameForUrl:table.nameForUrl,
primaryColumnName:table.primaryColumnName
,	columns:[]
};

for (let column of table.columns){
	var mycolumn = {
		id:column.id,
		name:column.name,
        type:column.type
        , 			typeOptions:column.typeOptions
	};
	mytable.columns.push(mycolumn);
}
myAT.tables.push(mytable);
}

jQuery('link[rel=stylesheet]').remove();
jQuery("body").html(JSON.stringify(myAT));
// console.log(myAT); // (not used here)
return (myAT);
"""

# from Kai_Curry
JS_SCRIPT_2 = """
return (JSON.stringify( _.mapValues(application.tablesById,
table => .set(.omit(table, ['sampleRows']),
'columns',
_.map(table.columns,
item => _.set(item, 'foreignTable',
_.get(item, 'foreignTable.id')))
))))
"""


class AirtableApp:
    def __init__(self, app_id, username, password) -> None:
        driver = self._driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.FIREFOX,
        )
        driver.get("https://airtable.com/" + app_id + "/api/docs")

        user_field = driver.find_element_by_name("email")
        password_field = driver.find_element_by_name("password")

        user_field.send_keys(username)
        password_field.send_keys(password)
        password_field.submit()
        self._init = time()

    @property
    def schema(self) -> typing.Dict:
        # Sleep the rest of the time needed to wait for page to load
        sleep(max(WAIT_SECS_FOR_PAGE_LOAD - (time() - self._init), 0))
        # return driver.execute_script(js_script_2)
        return self._driver.execute_script(JS_SCRIPT_1)

    def close(self) -> None:
        self._driver.quit()

    def __enter__(self) -> 'AirtableApp':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
