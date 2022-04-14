

__all__ = [
			'SAEcalc',



	]


def SAEcalc(df_neph):

	# def __init__(self):

	def _QCdata(_df):
		_df_ave = _df.mean()
		_df_std = _df.std()
		_df_lowb, _df_highb = _df<(_df_ave-_df_std*1.5), _df>(_df_ave+_df_std*1.5)

		return _df.mask(_df_lowb|_df_highb).copy()

	def _SAEcalc(_df):
		import numpy as n
		from scipy.optimize import curve_fit

		## parameter
		band = n.array([450,550,700])*1e-3

		## 3 pts fitting
		## function
		def _get_slope(__df):
			func = lambda _x, _sl, _int : _sl*_x+_int
			popt, pcov = curve_fit(func,n.log(band),n.log(__df))

			return popt

		## calculate
		_SAE = _df.apply(_get_slope,axis=1,result_type='expand')
		_SAE.columns = ['slope','intercept']

		return _SAE


	df_qc = df_neph[['B','G','R']].resample('1h').apply(_QCdata).dropna()
	return _SAEcalc(df_qc)



