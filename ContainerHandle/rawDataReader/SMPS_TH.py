

from .core import _reader
from pandas import to_datetime, read_table
from datetime import datetime as dtm
from pathlib import Path



class reader(_reader):

	nam = 'SMPS_TH'

	def _raw_reader(self,_file):
		with open(_file,'r',encoding='utf-8',errors='ignore') as f:
			_df  = read_table(f,skiprows=18,parse_dates={'Time':['Date','Start Time']}).set_index('Time')
			_key = list(_df.keys()[6:-26])

			_newkey = {}
			for _k in _key: 
				_newkey[_k] = float(_k).__round__(4)

			_newkey['Total Conc.(#/cm)'] = 'total'
			_newkey['Mode(nm)']	= 'mode'

		return _df[_newkey.keys()].rename(_newkey,axis=1)

	## QC data
	def _QC(self,_df):
		
		## 1-hr mean
		_df_1hr = _df.resample('1h').mean().copy()

		## 1-hr data clean
		## mask out the data size lower than 7
		_df_size = _df['total'].dropna().resample('1h').size().reindex(_df_1hr.index)
		_df_1hr  = _df_1hr.mask(_df_size<7)

		## remove the bin over 400 nm which num. conc. larger than 4000 
		_df_remv_ky = _df_1hr.keys()[:-2][_df_1hr.keys()[:-2]>=400.]

		_df_1hr[_df_remv_ky] = _df_1hr[_df_remv_ky].copy().mask(_df_1hr[_df_remv_ky]>4000.)

		return _df_1hr

