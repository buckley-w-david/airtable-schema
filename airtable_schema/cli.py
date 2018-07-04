import json

import click
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from airtable_schema import AirtableCredentials
from airtable_schema import fetch


@click.group()
@click.option(
    "--username", required=True, envvar="AIRTABLE_USER", help="Airtable username"
)
@click.option("--password", envvar="AIRTABLE_PASSWORD", help="Airtable password")
@click.option(
    "--stdin-password", is_flag=True, default=False, help="Read password in from stdin"
)
@click.pass_context
def main(
    ctx: click.core.Context, username: str, password: str, stdin_password: bool
) -> None:
    if not (password or stdin_password):
        raise click.UsageError("Must supply one of `password` or `stdin_password`")

    if stdin_password:
        password = input()
    ctx.obj = AirtableCredentials(username=username, password=password)


@main.command()
@click.option("--app-id", required=True, envvar="APP_ID", help="App ID for workspace")
@click.option(
    "--remote-driver-address",
    envvar="REMOTE_DRIVER_HOST",
    help="Remote selenium host",
)
@click.pass_context
def schema(ctx: click.core.Context, app_id: str, remote_driver_address: str) -> None:
    if remote_driver_address:
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
