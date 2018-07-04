from selenium import webdriver
from pprint import pprint
from sys import version_info
from time import sleep

# NOTE: it's a security risk to put login info in a plain text file. take appropriate precautions to protect/secure your data.
AIRTABLE_APP_ID = "app012345abcdef"
AIRTABLE_USER_ID = "userID@example.com"
AIRTABLE_PASSWORD = "mySecretPW"

WAIT_SECS_FOR_PAGE_LOAD = 15  # set higher/lower as needed for a slow webpage load

# from Chester_McLaughlin
js_script_1 = """
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
js_script_2 = """
return (JSON.stringify( _.mapValues(application.tablesById,
table => .set(.omit(table, ['sampleRows']),
'columns',
_.map(table.columns,
item => _.set(item, 'foreignTable',
_.get(item, 'foreignTable.id')))
))))
"""

print(
    "\nUsing: Python v"
    + f"{version_info.major}.{version_info.minor}.{version_info.micro} / ",
    end="",
)
print("Selenium v" + webdriver.version)

opts = webdriver.FirefoxOptions()
opts.set_headless(False)
driver = webdriver.Firefox(firefox_options=opts)
sess_id = driver.session_id

print(
    "WebDriver version: "
    + driver.capabilities["browserName"]
    + " v"
    + driver.capabilities["browserVersion"]
    + "\n"
)

driver.get("https://airtable.com/" + AIRTABLE_APP_ID + "/api/docs")

userID_field = driver.find_element_by_name("email")
passwd_field = driver.find_element_by_name("password")

userID_field.send_keys(AIRTABLE_USER_ID)
passwd_field.send_keys(AIRTABLE_PASSWORD)
passwd_field.submit()

print("Pausing for Airtable API page to load…")
sleep(WAIT_SECS_FOR_PAGE_LOAD)

schema_dict_1 = driver.execute_script(js_script_1)
schema_dict_2 = driver.execute_script(js_script_2)

print("\n=== Script results 1: ======================\n")
pprint(schema_dict_1)

print("\n=== Script results 2: ======================\n")
pprint(schema_dict_2)

driver.quit()

print("\n=== Done ==================================\n")
