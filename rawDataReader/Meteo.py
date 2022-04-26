
# read meteorological data from google sheet


from .core import _reader
from pandas import read_csv
from datetime import datetime as dtm
from pathlib import Path


class reader(_reader):

	nam = 'Meteo'

	def _raw_reader(self,_file):
		
		with (_file).open('r',encoding='utf-8',errors='ignore') as f:
			_df = read_csv(f,parse_dates=['Time'],index_col='Time',na_values=['-'])

		return _df