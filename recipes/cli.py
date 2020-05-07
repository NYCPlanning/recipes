import os
from pathlib import Path
import click
import json
from cook import Archiver
import pandas as pd
import numpy as np
from ast import literal_eval
from sqlalchemy import create_engine

CONFIG_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "recipe_info")

sh_recipes = ["pluto_input_cama_dof", "pluto_pts", "pluto_input_geocodes"]
py_recipes = [
    "dpr_capitalprojects",
    "bpl_libraries",
    "dcp_sfpsd",
    "doe_universalprek",
    "foodbankny_foodbanks",
    "moeo_socialservicesiteloactions",
    "nycdoc_corrections",
    "nypl_libraries",
    "nysdoccs_corrections",
    "uscourts_courts",
    "hra_centers",
    "dcas_ipis",
    "sca_capacity_projects_current",
    "sca_capacity_projects_prev",
    "sca_capacity_projects_tcu",
]


@click.group()
def cli():
    pass


def get_recipes(ctx, args, incomplete):
    return [k for k in os.listdir(CONFIG_PATH) if incomplete in k]


def load_recipe_json(recipe):
    """given a recipe return a python config dictionary"""
    recipe_config_path = Path(CONFIG_PATH) / f"{recipe}.json"

    with open(recipe_config_path, "r") as recipe_config_json:
        recipe_config = json.load(recipe_config_json)

    return recipe_config


def convert_recipe(recipe):
    df = pd.read_csv(Path(__file__).parent / "recipes.csv")
    df = df[df.schema_name == recipe]
    df.loc[:, "layerCreationOptions"] = df.loc[:, "layerCreationOptions"].apply(
        lambda x: x if pd.isna(x) else literal_eval(x)
    )
    df.loc[:, "srcOpenOptions"] = df.loc[:, "srcOpenOptions"].apply(
        lambda x: x if pd.isna(x) else literal_eval(x)
    )
    df.loc[:, "newFieldNames"] = df.loc[:, "newFieldNames"].apply(
        lambda x: x if pd.isna(x) else literal_eval(x)
    )
    df = df.replace(np.nan, "", regex=True)
    for row in df.iterrows():
        recipe = dict(row[1])
        if recipe in py_recipes + sh_recipes:
            pass
        else:
            print(f"converting {recipe['schema_name']} ...")
            with open(
                f"{Path(__file__).parent/'recipe_info'/recipe['schema_name']}.json", "w"
            ) as recipe_json:
                json.dump(recipe, recipe_json, indent=4, ensure_ascii=False)


# def update_metatable():
#     con = create_engine(os.environ['RECIPE_ENGINE'])
#     meta = pd.read_sql("select table_schema from information_schema.views where table_name='latest'", con=con).to_dict('records')
#     for d in meta:
#         d['version'] = pd.read_sql(f'select v from {d.get("table_schema")}.latest limit 1', con=con).to_dict('records')[0]['v']
#     pd.DataFrame(meta).to_sql('metadata', con=con, if_exists='replace')


@cli.command("run")
@click.argument("recipe", type=click.STRING, autocompletion=get_recipes)
def run_recipes(recipe):
    try:
        if recipe in sh_recipes:
            os.system(f"bash {Path(__file__).parent}/recipe_info/{recipe}.sh")
        elif recipe in py_recipes:
            os.system(f"python3 {Path(__file__).parent}/recipe_info/{recipe}.py")
        else:
            convert_recipe(recipe)
            recipe_config = load_recipe_json(recipe)
            archiver = Archiver(
                engine=os.environ["RECIPE_ENGINE"],
                ftp_prefix=os.environ["FTP_PREFIX"],
                s3_endpoint=os.environ.get("AWS_S3_ENDPOINT", "").replace(
                    "https://", ""
                ),
                s3_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
                s3_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", ""),
            )
            archiver.archive_table(recipe_config)
            # update_metatable()
    except KeyError:
        click.secho("\n Did you set your RECIPE_ENGINE and FTP_PREFIX? \n", fg="red")
