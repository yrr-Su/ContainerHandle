

from .core import _reader
from pandas import to_datetime, read_csv, Series
from datetime import datetime as dtm
from pathlib import Path
import numpy as n


class reader(_reader):

	nam = 'TEOM'

	def _raw_reader(self,_file):
		with open(_file,'r',encoding='utf-8',errors='ignore') as f:
			_df = read_csv(f,skiprows=3,index_col=False)

			_df = _df.rename(columns={ 'Time Stamp' 	   : 'time',
									   'System status' 	   : 'status',
									   'PM-2.5 base MC'    : 'PM_NV',
									   'PM-2.5 MC' 		   : 'PM_Total',
									   'PM-2.5 TEOM noise' : 'noise',})

			_time_replace = { '一月' : '01', '二月' : '02', '三月' : '03', '四月' : '04', '五月' : '05', '六月' : '06',
							  '七月' : '07', '八月' : '08', '九月' : '09', '十月' : '10', '十一月' : '11', '十二月' : '12'}

			_tm_idx = _df.time
			for _ori, _rpl in _time_replace.items():
				_tm_idx = _tm_idx.str.replace(_ori,_rpl)

			_df = _df.set_index(to_datetime(_tm_idx,errors='coerce',format='%d - %m - %Y %X'))

			_df = _df.where(_df['status']<1e-7)

		return _df[['PM_NV','PM_Total','noise',]]

	## QC data
	def _QC(self,_df):
	
		_df_idx = _df.index.copy()

		## remove negative value
		_df = _df.where(_df.noise<0.01)[['PM_NV','PM_Total']].mask((_df<0).copy()).dropna()

		## QC data in 1 hr
		## remove data where size < 8 in 1-hr
		for _key in ['PM_Total','PM_NV']:

			_size = _df[_key].resample('1h').size().reindex(_df_idx).ffill().copy()
			_df[_key] = _df[_key].mask(_size<8)

		return _df.reindex(_df_idx)