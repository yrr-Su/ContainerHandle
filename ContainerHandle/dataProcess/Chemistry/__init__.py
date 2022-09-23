
from ..core import _writter
from datetime import datetime as dtm

__all__ = [

			'Chemistry',

	]

class Chemistry(_writter):
	
	## Reconstruction
	def ReConstrc_basic(self,*df_chem,df_ref=None,df_water=None,nam_lst=['NH4+','SO42-','NO3-','Fe','Na+','OC','EC'],nam='reconstrc_basic'):
		from ._mass_volume import _basic

		print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Process \033[92mChemistry - reconstruction basic\033[0m -> {nam}")

		out = _basic(df_chem,df_ref,df_water,nam_lst=nam_lst)
		out = self._pre_process(out)

		self._save_out(nam,out)
		
		return out

	## OCEC
	def OCEC_basic(self,df_lcres,df_res,df_mass=None,ocec_ratio=None,ocec_ratio_month=1,hr_lim=200,
				   least_square_range=(0.1,2.5,0.1),nam='ocec_basic'):
		from ._ocec import _basic

		print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Process \033[92mChemistry - OC/EC basic\033[0m -> {nam}")

		out = _basic(df_lcres,df_res,df_mass,ocec_ratio,ocec_ratio_month,hr_lim,least_square_range)
		out = self._pre_process(out)

		self._save_out(nam,out)
		
		return out

	## TEOM
	def TEOM_basic(self,df_teom,df_check=None,nam='teom_basic'):
		from ._teom import _basic

		print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Process \033[92mChemistry - TEOM basic\033[0m -> {nam}")

		out = _basic(df_teom,df_check)
		out = self._pre_process(out)

		self._save_out(nam,out)
		
		return out




