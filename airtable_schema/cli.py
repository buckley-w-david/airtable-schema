import json

import click
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from airtable_schema import AirtableCredentials
from airtable_schema import fetch


@click.group()
@click.option("--username", required=True, help="Airtable Username")
@click.option("--password", help="Airtable Password")
@click.option("--stdin-password", is_flag=True, default=False, help="read password in from stdin")
@click.pass_context
def main(ctx: click.core.Context, username: str, password: str, stdin_password: bool) -> None:
    if not (password or stdin_password):
        raise click.UsageError("Must supply one of `password` or `stdin_password`")

    if stdin_password:
        password = input()
    ctx.obj = AirtableCredentials(username=username, password=password)


@main.command()
@click.option("--app-id", required=True, help="App ID for table")
@click.option("--remote-driver/--no-remove-driver", default=True)
@click.option("--remote-driver-address", default="http://127.0.0.1:4444/wd/hub")
@click.pass_context
def schema(
    ctx: click.core.Context,
    app_id: str,
    remote_driver: bool,
    remote_driver_address: str,
) -> None:
    if remote_driver:
        driver = webdriver.Remote(
            command_executor=remote_driver_address,
            desired_capabilities=DesiredCapabilities.FIREFOX,
        )
    else:
        opts = webdriver.FirefoxOptions()
        opts.set_headless(True)
        driver = webdriver.Firefox(firefox_options=opts)

    schema = fetch.fetch_schema(ctx.obj, app_id, driver)
    driver.close()
    click.echo(schema)
