

from .core import _reader
from pandas import to_datetime, read_table
from datetime import datetime as dtm
from pathlib import Path



class reader(_reader):

	nam = 'AE33'

	def _raw_reader(self,_file):
		with open(_file,'r',encoding='utf-8',errors='ignore') as f:
			_df = read_table(f,parse_dates={'time':['Date(yyyy/MM/dd);','Time(hh:mm:ss);']},
							 index_col='time',delimiter=' ',skiprows=[0,1,2,3,4,6,7])
			_df = _df[['BC1;','BC2;','BC3;','BC4;','BC5;','BC6;','BC7;',]]

			_df.columns = ['BC1','BC2','BC3','BC4','BC5','BC6','BC7',]

			return _df

	## QC data
	def _QC(self,_df):
		
		## remove negative value
		_df = _df.mask((_df<0).copy())

		## call by _QC function
		## QC data in 1 hr
		def _QC_func(_df_1hr):

			_df_ave = _df_1hr.mean()
			_df_std = _df_1hr.std()
			_df_lowb, _df_highb = _df_1hr<(_df_ave-_df_std*1.5), _df_1hr>(_df_ave+_df_std*1.5)

			return _df_1hr.mask(_df_lowb|_df_highb).copy()

		return _df.resample('1h').apply(_QC_func)

