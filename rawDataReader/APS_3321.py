

from .core import _reader
from pandas import to_datetime, read_table
from datetime import datetime as dtm
from pathlib import Path
import numpy as n



class reader(_reader):

	nam = 'APS_3321'

	def _raw_reader(self,_file):
		with open(_file,'r',encoding='utf-8',errors='ignore') as f:
			_df  = read_table(f,skiprows=6,parse_dates={'Time':['Date','Start Time']}).set_index('Time')
			_key = list(_df.keys()[3:54]) ## 542 ~ 1981

			_newkey = {}
			for _k in _key: 
				_newkey[_k] = float(_k).__round__(4)
			_newkey['Total Conc.'] = 'total'
			_newkey['Mode(m)'] = 'mode'

			_df = _df[_newkey.keys()].rename(_newkey,axis=1)
			_df['total'] = (_df.total.copy().map(lambda _: _.strip('(#/cm3)'))).astype(float)

		return _df

	## QC data
	def _QC(self,_df):
		
		## 1-hr mean
		_df_1hr = _df.resample('1h').mean().copy()

		## 1-hr data clean
		## mask out the data size lower than 7
		_df_size = _df['total'].dropna().resample('1h').size().reindex(_df_1hr.index)
		_df_1hr  = _df_1hr.mask(_df_size<7)

		## remove the bin over 4000 nm which num. conc. larger than 1 
		_df_remv_ky = _df_1hr.keys()[:-2][_df_1hr.keys()[:-2]>=4.]

		_df_1hr[_df_remv_ky] = _df_1hr[_df_remv_ky].copy().mask(_df_1hr[_df_remv_ky]>1.)

		## remove total num. conc. larger than 1000
		_df_1hr = _df_1hr.mask(_df_1hr.total>1000)

		return _df_1hr
