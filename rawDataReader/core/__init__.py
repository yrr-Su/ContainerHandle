
from datetime import datetime as dtm
from pandas import date_range, concat
from pathlib import Path
import pickle as pkl
import json as jsn

__all__ = [
			'reader'

	]


# bugs box
"""



# """


# logger setting
# import logging

# LOG_NAM = 'dev'
# FMT = { 'dev' :	dict( format  = '[%(name)s| %(levelname)s]	%(message)s',
					  # level	  = logging.DEBUG,
					# ),
		# 'rls' :	dict( format  = '[%(levelname)s| %(asctime)s] - %(message)s',
					  # datefmt = '%Y-%m-%d %H:%M:%S',
					  # level	  = logging.INFO,
					# ),
# }
# logging.basicConfig(**FMT[LOG_NAM])
# logger = logging.getLogger(LOG_NAM)


# meta data
with (Path(__file__).parent/'meta.json').open('r',encoding='utf-8',errors='ignore') as f:
	meta = jsn.load(f)



# rawDataReader parent class
## parant class (read file)
## list the file in the path and 
## read pickle file if it exisits, else read raw data and dump the pickle file
class readerFlow:
	
	nam = None

	## initial setting
	## input : file path, 
	##		   start time,
	##		   final time,
	##		   reset switch
	## 
	## the pickle file will be generated after read raw data first time,
	## if want to re-read the rawdata, please set 'reset=True'

	def __init__(self,_path,_sta,_fin,reset=False):
		# logger.info(f'\n{self.nam}')
		# print('='*65)
		# logger.info(f"Reading file and process data")

		## class parameter
		self.index = lambda _freq: date_range(_sta,_fin,freq=_freq)
		self.path  = Path(_path)
		self.reset = reset
		self.meta  = meta[self.nam]
		self.pkl_nam = f'{self.nam.lower()}.pkl'
		self.__time	 = (_sta,_fin)
		
		# print(f" from {_sta.strftime('%Y-%m-%d %X')} to {_fin.strftime('%Y-%m-%d %X')}")
		# print('='*65)
		# print(f"{dtm.now().strftime('%m/%d %X')}")

	def __raw_reader(self,_file):
		## customize each instrument
		## read one filess
		return None

	def __raw_process(self,_df,_freq):
		## customize each instrument
		out = _df.resample(_freq).mean().reindex(self.index(_freq))
		return out
	
	## read raw data
	def __reader(self):

		## read pickle if pickle file exisits and 'reset=False' or process raw data
		if (self.pkl_nam in [_.name for _ in self.path.glob('*.pkl')])&(~self.reset):
			print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Reading \033[96mPICKLE\033[0m file of {self.nam}")
			with (self.path/self.pkl_nam).open('rb') as f:
				fout = pkl.load(f)
			return fout
		else: 
			print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Reading \033[96mRAW DATA\033[0m of {self.nam} and process it")
		##=================================================================================================================
		## metadata parameter
		ext_nam, dt_freq = self.meta.values()

		## read raw data
		_df_con = None
		
		for file in self.path.glob(f'*{ext_nam}'):
			# if ext_nam not in file.lower(): continue
			print(f"\r\t\treading {file.name}",end='')

			_df = self.__raw_reader(file)

			if _df is not None:
				_df_con = concat([_df_con,_df]) if _df_con is not None else _df

		## concat the concated list
		fout = self.__raw_process(_df_con,dt_freq)
		print()

		##=================================================================================================================
		## dump pickle file
		with (self.path/self.pkl_nam).open('wb') as f:
			pkl.dump(fout,f,protocol=pkl.HIGHEST_PROTOCOL)

		return fout

	## get process data
	def get_data(self,start=None,final=None,mean_freq=None):

		## get dataframe data and process to wanted time range
		_freq = mean_freq if mean_freq is not None else self.meta['freq']
		_time = (start,final) if start is not None else self.__time

		return self.__reader().resample(_freq).mean().reindex(date_range(*_time,freq=_freq))

	## get process data
	def __call__(self,start=None,final=None,mean_freq=None):

		## get dataframe data and process to wanted time range
		_freq = mean_freq if mean_freq is not None else self.meta['freq']
		_time = (start,final) if start is not None else self.__time

		return self.__reader().resample(_freq).mean().reindex(date_range(*_time,freq=_freq))
