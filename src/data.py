import pandas as pd
import pathlib
import country_converter as coco

p = pathlib.Path('.')
path_name = {path:path.name.replace('tbl','').replace('.csv', '') for path in list(p.glob('**/*.csv'))}
tables = {path.name.replace('tbl','').replace('.csv', ''):pd.read_csv(path, index_col=f'{path_name[path]}ID') for path in path_name}


tables['Film'] = tables[tables['Film'][[['FilmBoxOfficeDollars']]].isna() == False]

tables['Film']['FilmReleaseDate'] = pd.to_datetime(tables['Film']['FilmReleaseDate'])
tables['Film']['FilmBoxOfficeDollars'] = tables['Film']['FilmBoxOfficeDollars'] /10**6
tables['Film']['FilmBudgetDollars'] = tables['Film']['FilmBudgetDollars'] /10**6
tables['Film']['FilmBenefits'] = tables['Film']['FilmBoxOfficeDollars'] - tables['Film']['FilmBudgetDollars']
tables['Film']['FilmReleaseDate'] = pd.to_datetime(tables['Film']['FilmReleaseDate'])
tables['Film']['FilmReleaseYear'] = tables['Film']['FilmReleaseDate'].dt.year
tables['Actor']['ActorDOB'] = pd.to_datetime(tables['Actor']['ActorDOB'])
tables['Director']['DirectorDOB'] = pd.to_datetime(tables['Director']['DirectorDOB'])
cc = coco.CountryConverter()
tables['Country']['CountryCode'] = cc.pandas_convert(tables['Country']['CountryName'])