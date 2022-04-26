

__all__ = [
			'scattering',
			'absorption',



	]


class _writter:

	def __init__(self,path_out=None,excel=True):

		self.path_out = path_out
		self.excel	  = excel

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


class scattering(_writter):

	def SAE(self,df,nam='SAE'):
		from ._scattering import _SAE

		out = _SAE(df)
		self._save_out(nam,out)

		return out

class absorption(_writter):

	def absCoe(self,df,nam='absCoe'):
		from ._absorption import _absCoe

		out = _AAE(df)
		self._save_out(nam,out)

		return out

	def AAE(self,df,nam='AAE'):
		from ._absorption import _AAE

		out = _AAE(df)
		self._save_out(nam,out)

		return out

class basic(_writter):
	
	def __call__(self,df_abs,df_sca,nam='basic'):
		from ._extinction import _basic

		out = _basic(df_abs,df_sca)
		self._save_out(nam,out)
		
		return out