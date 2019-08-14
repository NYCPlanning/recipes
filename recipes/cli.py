
import os
from pathlib import Path
import click
import json
from cook import Archiver

CONFIG_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'recipe_info'
)

@click.group()
def cli():
    pass


def get_recipes(ctx, args, incomplete):
        return [k for k in os.listdir(CONFIG_PATH) if incomplete in k]

def load_recipe_json(recipe):
    """given a recipe return a python config dictionary"""
    recipe_config_path = Path(CONFIG_PATH)/f'{recipe}.json'

    with open(recipe_config_path, "r") as recipe_config_json:
        recipe_config = json.load(recipe_config_json)
    
    return recipe_config

@cli.command('run')
@click.argument('recipe', type=click.STRING, autocompletion=get_recipes)
def run_recipes(recipe):
    recipe_config = load_recipe_json(recipe)
    try:
        archiver = Archiver(engine=os.environ['RECIPE_ENGINE'], 
                            ftp_prefix=os.environ['FTP_PREFIX'])
        archiver.archive_table(recipe_config)
    except KeyError: 
        click.secho('\n Please set yout RECIPE_ENGINE \n', fg='red')