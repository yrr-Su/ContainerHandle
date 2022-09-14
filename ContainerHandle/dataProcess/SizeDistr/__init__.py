

from ..core import _writter
from datetime import datetime as dtm

__all__ = [

			'SizeDistr',

	]


class SizeDistr(_writter):

	## basic
	def basic(self,df,hybrid_bin_start_loc=None,unit='nm',nam='distr_basic'):
		from ._size_distr import _basic

		print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Process \033[92mSizeDistr - basic\033[0m -> {nam}")
		out = _basic(df,hybrid_bin_start_loc,unit)
		out = self._pre_process(out)

		self._save_out(nam,out)

		return out

	## merge
	def merge_SMPS_APS(self,df_smps,df_aps,nam='distr_merge',aps_unit='um',shift_mode='mobility',
					   smps_overlap_lowbound=523,aps_fit_highbound=800):
		from ._merge import _merge_SMPS_APS
		
		print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Process \033[92mSizeDistr - merge_SMPS_APS\033[0m -> {nam}")

		out = _merge_SMPS_APS(df_smps,df_aps,aps_unit,shift_mode,smps_overlap_lowbound,aps_fit_highbound)
		out = self._pre_process(out)

		self._save_out(nam,out)

		return out


