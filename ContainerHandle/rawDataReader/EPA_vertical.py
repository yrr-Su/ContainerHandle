

from .core import _reader
from pandas import read_csv, to_numeric
from datetime import datetime as dtm
from pathlib import Path


class reader(_reader):

	nam = 'EPA_vertical'

	def _raw_reader(self,_file):
		
		with (_file).open('r',encoding='big5',errors='ignore') as f:
			_df = read_csv(f,names=['time','station','comp','data',None],skiprows=1,na_values=['-'],
						   parse_dates=['time'],index_col='time')
			_df['data'] = to_numeric(_df['data'],errors='coerce')
			
			_df_piv = _df.pivot_table(values='data',columns='comp',index='time')
			_df_piv.index.name = 'time'

		return _df_piv