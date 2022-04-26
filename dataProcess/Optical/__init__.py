

__all__ = [
			'scattering',
			'absorption',



	]


class scattering:
	
	def __init__(self,path_out=None,excel=True):

		self.path_out = path_out
		self.excel	  = excel

	def _save_out(self,_nam,_out):

		if self.path_out is not None:
			with (self.path_out/f'{_nam}.pkl').open('wb') as f:
				pkl.dump(_out,f,protocol=pkl.HIGHEST_PROTOCOL)

			if self.excel:		
				with ExcelWriter(self.path_out/f'{_nam}.xlsx') as f: 
					_out.to_excel(f,sheet_name=f'{_nam}')

	def SAE(self,df,nam='SAE'):
		from ._scattering import _SAE

		out = _SAE(df)
		self._save_out(nam,out)

		return out




class absorption:
	
	def __init__(self,path_out=None,excel=True):

		self.path_out = path_out
		self.excel	  = excel

	def _save_out(self,_nam,_out):

		if self.path_out is not None:
			with (self.path_out/f'{_nam}.pkl').open('wb') as f:
				pkl.dump(_out,f,protocol=pkl.HIGHEST_PROTOCOL)

			if self.excel:		
				with ExcelWriter(self.path_out/f'{_nam}.xlsx') as f: 
					_out.to_excel(f,sheet_name=f'{_nam}')

	def AAE(self,df,nam='AAE'):
		from ._absorption import _AAE

		out = _AAE(df)
		self._save_out(nam,out)

		return out