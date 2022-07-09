import pickle as pkl
from pandas import ExcelWriter

__all__ = [
			'scattering',
			'absorption',
			'basic',



	]


class _writter:

	def __init__(self,path_out=None,excel=True,csv=False):

		self.path_out = path_out
		self.excel	  = excel
		self.csv	  = csv

	def _save_out(self,_nam,_out):

		if self.path_out is not None:
			with (self.path_out/f'{_nam}.pkl').open('wb') as f:
				pkl.dump(_out,f,protocol=pkl.HIGHEST_PROTOCOL)

			if self.excel:		
				with ExcelWriter(self.path_out/f'{_nam}.xlsx') as f:
					if type(_out)==dict():
						for _key, _val in _out.items():
							_val.to_excel(f,sheet_name=f'{_key}')
					else:
						_out.to_excel(f,sheet_name=f'{_nam}')

			if self.csv:
				if type(_out)==dict():
					_path_out = self.path_out/_nam
					_path_out.mkdir()

					for _key, _val in _out.items():
						_val.to_csv(_path_out/f'{_key}.csv')
				else:
					_out.to_csv(self.path_out/f'{_nam}.csv')



class scattering(_writter):

	def SAE(self,df,nam='SAE'):
		from ._scattering import _SAE

		out = _SAE(df)
		self._save_out(nam,out)

		return out

class absorption(_writter):

	def absCoe(self,df,nam='absCoe'):
		from ._absorption import _absCoe

		out = _absCoe(df)
		self._save_out(nam,out)

		return out

	def AAE(self,df,nam='AAE'):
		from ._absorption import _AAE

		out = _AAE(df)
		self._save_out(nam,out)

		return out

class basic(_writter):
	
	def __call__(self,df_abs,df_sca,df_pm25,nam='basic'):
		from ._extinction import _basic

		out = _basic(df_abs,df_sca,df_pm25)
		self._save_out(nam,out)
		
		return out