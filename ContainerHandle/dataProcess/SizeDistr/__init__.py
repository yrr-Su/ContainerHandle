

from ..core import _writter, _run_process

__all__ = [

			'SizeDistr',

	]


class SizeDistr(_writter):

	## basic
	@_run_process('SizeDistr - basic','distr_basic')
	def basic(self,df,hybrid_bin_start_loc=None,unit='nm'):
		from ._size_distr import _basic

		out = _basic(df,hybrid_bin_start_loc,unit)

		return self, out

	## merge
	@_run_process('SizeDistr - merge_SMPS_APS','distr_merge')
	def merge_SMPS_APS(self,df_smps,df_aps,aps_unit='um',shift_mode='mobility',
					   smps_overlap_lowbound=523,aps_fit_highbound=800):
		from ._merge import _merge_SMPS_APS
		
		out = _merge_SMPS_APS(df_smps,df_aps,aps_unit,shift_mode,smps_overlap_lowbound,aps_fit_highbound)

		return self, out


