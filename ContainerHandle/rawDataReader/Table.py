
# read meteorological data from google sheet


from .core import _reader
from pandas import read_csv, to_datetime
from datetime import datetime as dtm
from pathlib import Path


class reader(_reader):

	nam = 'Table'

	def _raw_reader(self,_file):

		self.meta['freq'] = self._oth_set.get('data_freq') or self.meta['freq']
		
		with (_file).open('r', encoding='utf-8-sig', errors='ignore') as f:
			_df = read_csv(f, low_memory=False)

			_df_index = to_datetime( _df.iloc[:,0], errors='coerce', format=self._oth_set.get('date_format') )
			_df.index = _df_index
		
			_df.columns = _df.keys().str.strip(' ')
			_df.index.name = 'time'

			_df = _df.loc[_df.index.dropna()].copy()
			# breakpoint()
		return _df.loc[~_df.index.duplicated()]



