


from pathlib import Path
import pickle as pkl
from pandas import ExcelWriter
import ContainerHandle.dataProcess.Optical


__all__ = [
			'Optical',
			'SizeDistr',



	]


class SizeDistr:

	def __init__(self,path_out=None,excel=True):

		self.path_out = Path(path_out)
		self.excel	  = excel

	def _save_out(self,_nam,_out):

		if self.path_out is not None:
			with (self.path_out/f'{_nam}.pkl').open('wb') as f:
				pkl.dump(_out,f,protocol=pkl.HIGHEST_PROTOCOL)

			if self.excel:
				with ExcelWriter(self.path_out/f'{_nam}.xlsx') as f:
					for _key, _val in _out.items():
						_val.to_excel(f,sheet_name=f'{_key}')

	def basic(self,df,nam,hybrid_bin_start_loc=None):
		from ._SizeDistr import _basic

		out = _basic(df,hybrid_bin_start_loc)
		self._save_out(nam,out)

		return out
