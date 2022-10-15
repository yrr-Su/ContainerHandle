
from ..core import _writter, _run_process

__all__ = [

			'Chemistry',

	]

class Chemistry(_writter):
	
	## Reconstruction
	@_run_process('Chemistry - reconstruction basic','reconstrc_basic')
	def ReConstrc_basic(self,*df_chem,df_ref=None,df_water=None,nam_lst=['NH4+','SO42-','NO3-','Fe','Na+','OC','EC']):
		from ._mass_volume import _basic

		out = _basic(df_chem,df_ref,df_water,nam_lst=nam_lst)
		
		return self, out

	## OCEC
	@_run_process('Chemistry - OC/EC basic','ocec_basic')
	def OCEC_basic(self,df_lcres,df_res,df_mass=None,ocec_ratio=None,ocec_ratio_month=1,hr_lim=200,
				   least_square_range=(0.1,2.5,0.1)):
		from ._ocec import _basic

		out = _basic(df_lcres,df_res,df_mass,ocec_ratio,ocec_ratio_month,hr_lim,least_square_range)
		
		return self, out

	## TEOM
	@_run_process('Chemistry - TEOM basic','teom_basic')
	def TEOM_basic(self,df_teom,df_check=None):
		from ._teom import _basic

		out = _basic(df_teom,df_check)
		
		return self, out




