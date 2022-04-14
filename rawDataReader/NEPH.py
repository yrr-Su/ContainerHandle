

from .core import readerFlow
from pandas import to_datetime, read_csv
from datetime import datetime as dtm
from pathlib import Path



class reader(readerFlow):

	nam = 'NEPH'

	def _readerFlow__raw_reader(self,_file):

		## pre-process data as csv file
		with (_file).open('r',encoding='utf-8',errors='ignore') as f_rd, \
			 (self.path/f'temp.csv').open('w',encoding='utf-8',errors='ignore') as f_wri:

			for _l in f_rd:
				f_wri.write(_l.rstrip('\n')+','*(11-_l.split(',').__len__())+'\n')

		## read csv file
		with (self.path/f'temp.csv').open('r',encoding='utf-8',errors='ignore') as f:

			_df = read_csv(f,header=None,names=range(11))
			_df_grp = _df.groupby(0)

			## T : time
			_df_tm = _df_grp.get_group('T')[[1,2,3,4,5,6]].astype(int)

			for _k in [2,3,4,5,6]:
				_df_tm[_k] = _df_tm[_k].astype(int).map('{:02d}'.format).copy()
			_df_tm = _df_tm.astype(str)

			_idx_tm = to_datetime((_df_tm[1]+_df_tm[2]+_df_tm[3]+_df_tm[4]+_df_tm[5]+_df_tm[6]),format='%Y%m%d%H%M%S')

			## D : data
			## col : 3~8 B G R BB BG BR
			## 1e6
			_df_dt = _df_grp.get_group('D')[[1,2,3,4,5,6,7,8]].set_index(_idx_tm)
			_df_out = (_df_dt.groupby(1).get_group('NBXX')[[3,4,5,6,7,8]]*1e6).reindex(_idx_tm)
			_df_out.columns = ['B','G','R','BB','BG','BR']
			_df_out.index.name = 'Time'

			## Y : state
			## col : 5 RH
			_df_out['RH'] = _df_grp.get_group('Y')[5].values
			
		return _df_out



