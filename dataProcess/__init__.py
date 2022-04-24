


from pathlib import Path
import pickle as pkl
from pandas import ExcelWriter


__all__ = [
			'NEPH',
			'SizeDistr',



	]


class NEPH:
	
	def __init__(self,path_out=None,excel=True):
		from _NEPH import *
		
		self.path_out = path_out
		self.excel	  = excel
		self.csv 	  = csv

	def _save_out(self,_nam,_out):

		if self.path_out is not None:
			with (self.path_out/f'{_nam}.pkl').open('wb') as f:
				pkl.dump(_out,f,protocol=pkl.HIGHEST_PROTOCOL)

			if self.excel:		
				with ExcelWriter(self.path_out/f'{_nam}.xlsx') as f: 
					_out.to_excel(f,sheet_name=f'{_nam}')

	def SAE(self,df,nam='SAE'):

		out = _SAE(df)
		self._save_out(nam,out)

		return out



class SizeDistr:
	
	def __init__(self,path_out=None,excel=True):
		from _SizeDistr import *

		self.path_out = path_out
		self.excel	  = excel
		self.csv 	  = csv

	def _save_out(self,_nam,_out):

		if self.path_out is not None:
			with (self.path_out/f'{_nam}.pkl').open('wb') as f:
				pkl.dump(_out,f,protocol=pkl.HIGHEST_PROTOCOL)

			if self.excel:
				with ExcelWriter(self.path_out/f'{_nam}.xlsx') as f: 
					for _key, _val in _out.items():
						_out.to_excel(f,sheet_name=f'{_key}')

	def basic(self,df,nam):

		out = _basic(df)
		self._save_out(nam,out)

		return out
