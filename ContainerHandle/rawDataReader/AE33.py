

from .core import _reader
from pandas import to_datetime, read_table
from datetime import datetime as dtm
from pathlib import Path



class reader(_reader):

	nam = 'AE33'

	def _raw_reader(self,_file):
		with open(_file,'r',encoding='utf-8',errors='ignore') as f:
			_df = read_table(f,parse_dates={'time':[0,1]},index_col='time',
								delimiter='\s+',skiprows=8,names=range(71))

			columns = [ 'Timebase','RefCh1','Sen1Ch1','Sen2Ch1','RefCh2','Sen1Ch2',
						'Sen2Ch2','RefCh3','Sen1Ch3','Sen2Ch3','RefCh4','Sen1Ch4','Sen2Ch4','RefCh5','Sen1Ch5','Sen2Ch5',
						'RefCh6','Sen1Ch6','Sen2Ch6','RefCh7','Sen1Ch7','Sen2Ch7','Flow1','Flow2','FlowC','Pressure (Pa)',
						'Temperature (°C)','BB (%)','ContTemp','SupplyTemp','Status','ContStatus','DetectStatus','LedStatus',
						'ValveStatus','LedTemp','BC11','BC12','BC1','BC21','BC22','BC2','BC31','BC32','BC3','BC41','BC42',
						'BC4','BC51','BC52','BC5','BC61','BC62','BC6','BC71','BC72','BC7','K1','K2','K3','K4','K5','K6','K7',
						'TapeAdvCount','ID_com1','ID_com2','ID_com3','fields_i']

			_df.columns = columns
			_df = _df[['BC1','BC2','BC3','BC4','BC5','BC6','BC7','Status']]

			## remove data without Status=0, 128(Not much filter tape), 256(Not much filter tape)
			_df = _df.where((_df['Status']==0)|(_df['Status']==128)|(_df['Status']==256)).copy()

			return _df[['BC1','BC2','BC3','BC4','BC5','BC6','BC7']]

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

		return _df.resample('1h',group_keys=False).apply(_QC_func).resample('5T').mean()

