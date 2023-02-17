
# read meteorological data from google sheet


from .core import _reader
from pandas import read_csv
from datetime import datetime as dtm
from pathlib import Path


class reader(_reader):

	nam = 'Table'

	def _raw_reader(self,_file):
		
		with (_file).open('r',encoding='utf-8-sig',errors='ignore') as f:

			_time_idx = f.readlines(1)[0][:-2].lower().split(',').index('time')

			f.seek(0)

			_df = read_csv(f,parse_dates=[_time_idx],index_col=_time_idx,na_values=['-'])
			_df.columns = _df.keys().str.strip(' ')
			
		return _df.loc[_df.index.dropna()].loc[~_df.index.duplicated()]