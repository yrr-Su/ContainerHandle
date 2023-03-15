
# read meteorological data from google sheet


from .core import _reader
from pandas import read_csv
from datetime import datetime as dtm
from pathlib import Path


class reader(_reader):

	nam = 'Table'

	def _raw_reader(self,_file):
		
		with (_file).open('r',encoding='utf-8-sig',errors='ignore') as f:

			_df = read_csv(f,parse_dates=[0],index_col=[0],na_values=['-'])

			_df.columns = _df.keys().str.strip(' ')
			_df.index.name = 'time'
			
		return _df.loc[_df.index.dropna()].loc[~_df.index.duplicated()]
