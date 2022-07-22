
from datetime import datetime as dtm
from datetime import timedelta as dtmdt
from pandas import date_range, concat
from pathlib import Path
from ..utils.config import meta
import pickle as pkl

# import json as jsn

__all__ = [
			'_reader'

	]


# bugs box
"""

acquisition rate
yield rate

# """
# meta data
# with (Path(__file__).parent/'meta.json').open('r',encoding='utf-8',errors='ignore') as f:
	# meta = jsn.load(f)



# rawDataReader parent class
## parant class (read file)
## list the file in the path and 
## read pickle file if it exisits, else read raw data and dump the pickle file
class _reader:
	
	nam = None

	## initial setting
	## input : file path, 
	##		   reset switch
	## 
	## the pickle file will be generated after read raw data first time,
	## if want to re-read the rawdata, please set 'reset=True'

	def __init__(self,_path,QC=True,csv_raw=True,reset=False):
		# logger.info(f'\n{self.nam}')
		# print('='*65)
		# logger.info(f"Reading file and process data")

		## class parameter
		self.index = lambda _freq: date_range(_sta,_fin,freq=_freq)
		self.path  = Path(_path)
		self.meta  = meta[self.nam]

		self.reset = reset
		self.qc    = QC
		self.csv   = csv_raw

		self.pkl_nam = f'read_{self.nam.lower()}.pkl'
		self.csv_nam = f'read_{self.nam.lower()}.csv'
		
		# print(f" from {_sta.strftime('%Y-%m-%d %X')} to {_fin.strftime('%Y-%m-%d %X')}")
		# print('='*65)
		# print(f"{dtm.now().strftime('%m/%d %X')}")

	## dependency injection function
	## read raw data
	def _raw_reader(self,_file):
		## customize each instrument
		## read one file
		pass

	## QC data
	def _QC(self,_df):
		## customize each instrument
		return _df

	## built-in function
	## get time from df and set time to whole time to create time index
	def _time2whole(self,_df):
		## set time index to whole time
		_st, _ed  = _df.index[[0,-1]]
		_tm_index = date_range(_st.strftime('%Y%m%d %H00'),
							  (_ed+dtmdt(hours=1)).strftime('%Y%m%d %H00'),
							  freq=self.meta['freq'])
		return _tm_index

	## set each to true datetime(18:30:01 -> 18:30:00) and rindex data
	def _raw_process(self,_df):

		_tm_index = self._time2whole(_df)

		_out = _df.resample(self.meta['freq']).mean().reindex(_tm_index)
		return _out

	## read raw data
	def _run(self,_start,_end):

		## read pickle if pickle file exisits and 'reset=False' or process raw data
		if (self.path/self.pkl_nam in list(self.path.glob('*.pkl')))&(~self.reset):
			print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Reading \033[96mPICKLE\033[0m file of {self.nam}")
			with (self.path/self.pkl_nam).open('rb') as f:
				_fout = pkl.load(f)
				_start, _end = _start or _fout.index[0], _end or _fout.index[0]

			return _fout.reindex(date_range(_start,_end,freq=_fout.index.freq.copy()))
		else: 
			print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Reading \033[96mRAW DATA\033[0m of {self.nam} and process it")
		##=================================================================================================================
		## read raw data
		_df_con = None

		for file in self.path.glob(f"*{self.meta['extension']}"):
			print(f"\r\t\treading {file.name}",end='')

			_df = self._raw_reader(file)

			## concat the concated list
			if _df is not None:
				_df_con = concat([_df_con,_df]) if _df_con is not None else _df
		
		## reindex data and QC
		_fout = self._raw_process(_df_con)
		_start, _end = _start or _fout.index[0], _end or _fout.index[0]

		_fout = _fout.reindex(date_range(_start,_end,freq=_fout.index.freq.copy()))

		if self.qc:
			_fout_qc = self._QC(_fout)

			if self.meta['deter_key'] is not None:
				_key = self.meta['deter_key']

				_the_size  = len(_fout.resample('1h').mean().index)
				_real_size = len(_fout[_key].resample('1h').mean().copy().dropna().index)
				_QC_size   = len(_fout_qc[_key].resample('1h').mean().copy().dropna().index)
				_acq_rate  = round((_real_size/_the_size)*100,2)
				_yid_rate  = round((_QC_size/_real_size)*100,2)

				with (self.path/f'{self.nam}.log').open('a+') as f:
					f.write(f"\n{dtm.now().strftime('%Y/%m/%d %X')}\n")
					f.write(f"{'-'*30}\n")
					f.write(f"acquisition rate : {_acq_rate}%\n")
					f.write(f'yield rate : {_yid_rate}%\n')
					f.write(f"{'-'*30}\n")

				print(f'\n\t\tacquisition rate : {_acq_rate}%')
				print(f'\t\tyield rate : {_yid_rate}%')
				print()

			_fout = _fout_qc

		##=================================================================================================================
		## dump pickle file
		with (self.path/self.pkl_nam).open('wb') as f:
			pkl.dump(_fout,f,protocol=pkl.HIGHEST_PROTOCOL)

		## dump csv file
		if self.csv:
			_fout.to_csv(self.path/self.csv_nam)

		return _fout

	## get data
	def __call__(self,start=None,end=None,mean_freq=None):

		fout = self._run(start,end)
		# _fout = self._run()

		if mean_freq is not None:
			fout = fout.resample(mean_freq).mean()

		return fout
