

from pathlib import Path
import pickle as pkl

class _writter:

	def __init__(self,path_out=None,excel=True,csv=False):

		self.path_out = path_out
		self.excel	  = excel
		self.csv	  = csv

	def _pre_process(self,_out):

		if type(_out)==dict:
			for _ky, _df in _out.items():
				_df.index.name = 'time'
		else:
			_out.index.name = 'time'

		return _out

	def _save_out(self,_nam,_out):

		if self.path_out is not None:
			self.path_out.mkdir(exist_ok=True,parents=True)
			with (self.path_out/f'{_nam}.pkl').open('wb') as f:
				pkl.dump(_out,f,protocol=pkl.HIGHEST_PROTOCOL)

			if self.excel:
				from pandas import ExcelWriter
				with ExcelWriter(self.path_out/f'{_nam}.xlsx') as f:
					if type(_out)==dict:
						for _key, _val in _out.items():
							_val.to_excel(f,sheet_name=f'{_key}')
					else:
						_out.to_excel(f,sheet_name=f'{_nam}')

			if self.csv:
				if type(_out)==dict:
					_path_out = self.path_out/_nam
					_path_out.mkdir(exist_ok=True,parents=True)

					for _key, _val in _out.items():
						_val.to_csv(_path_out/f'{_key}.csv')
				else:
					_out.to_csv(self.path_out/f'{_nam}.csv')

