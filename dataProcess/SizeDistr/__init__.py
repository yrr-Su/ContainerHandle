
__all__ = [
			'basic'



	]




class _dt_output
	def __init__(self,_nam):
		self._nam = _nam

	def __call__(self,_func):

		def _wrap(*arg,**kwarg):
			_out = _func(*arg,**kwarg)
			return _out

		return _wrap



@_dt_output('surf')
def _S(_df,_path):
	




dS = dN * pi*dp**2
dV = dN * pi*(dp**3)/6
print('\n1 - 4')
from math import *
dN = dN_dlog_1*dlog_dp
dS = dN*pi*dp**2
dV = dN*pi*(dp**3)/6