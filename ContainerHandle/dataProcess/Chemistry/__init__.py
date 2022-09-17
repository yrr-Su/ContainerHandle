
from ..core import _writter
from datetime import datetime as dtm

__all__ = [

			'Chemistry',

	]

class Chemistry(_writter):
	
	## extinction
	def basic(self,*df_chem,df_ref=None,df_water=None,nam_lst=['NH4+','SO42-','NO3-','Fe','Na+','OC','EC'],nam='che_basic'):
		from ._mass_volume import _basic

		print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Process \033[92mChemistry - basic\033[0m -> {nam}")

		out = _basic(df_chem,df_ref,df_water,nam_lst=nam_lst)
		out = self._pre_process(out)

		self._save_out(nam,out)
		
		return out