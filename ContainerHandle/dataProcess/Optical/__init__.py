
from ..core import _writter
from datetime import datetime as dtm

__all__ = [

			'Optical',

	]

class Optical(_writter):
	
	## scatter
	def SAE(self,df,nam='SAE'):
		from ._scattering import _SAE

		print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Process \033[92mOptical - SAE\033[0m -> {nam}")

		out = _SAE(df)
		out = self._pre_process(out)

		self._save_out(nam,out)

		return out
	
	## absorption
	def absCoe(self,df,abs_band=550,nam='absCoe'):
		from ._absorption import _absCoe

		print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Process \033[92mOptical - absCoe\033[0m -> {nam}")

		out = _absCoe(df,abs_band)
		out = self._pre_process(out)

		self._save_out(nam,out)

		return out

	def AAE(self,df,nam='AAE'):
		from ._absorption import _AAE

		print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Process \033[92mOptical - AAE\033[0m -> {nam}")

		out = _AAE(df)
		out = self._pre_process(out)

		self._save_out(nam,out)

		return out

	## extinction
	def basic(self,df_abs,df_sca,df_ec=None,df_mass=None,nam='opt_basic'):
		from ._extinction import _basic

		print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Process \033[92mOptical - basic\033[0m -> {nam}")

		out = _basic(df_abs,df_sca,df_ec,df_mass)
		out = self._pre_process(out)

		self._save_out(nam,out)
		
		return out