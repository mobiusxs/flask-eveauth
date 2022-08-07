import click


@click.group()
def auth():
    pass


@auth.command()
def createsuperuser():
    pass
