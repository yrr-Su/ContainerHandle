


def _absCoe(df):
	import numpy as n

	MAE = n.array([18.47,14.54,13.14,11.58,10.35,7.77,7.19])*1e-3

	return df*MAE





def _AAE(df):
	import numpy as n
	from scipy.optimize import curve_fit

	def _AAEcalc(_df):

		## parameter
		MAE  = n.array([18.47,14.54,13.14,11.58,10.35,7.77,7.19])*1e-3
		band = n.array([370,470,520,590,660,880,950])
		_df *= MAE

		## 7 pts fitting
		## function
		def _get_slope(__df):
			func = lambda _x, _sl, _int : _sl*_x+_int
			popt, pcov = curve_fit(func,n.log(band),n.log(__df))

			return popt

		## calculate
		_AAE = _df.apply(_get_slope,axis=1,result_type='expand')
		_AAE.columns = ['slope','intercept']

		return _AAE

	df_out = _AAEcalc(df[['BC1','BC2','BC3','BC4','BC5','BC6','BC7']].dropna())
	df_out = df_out.mask((-df_out.slope<0.8)|(-df_out.slope>2.)).copy()

	return df_out.reindex(df.index)