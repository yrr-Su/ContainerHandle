

def _basic(df_abs,df_sca):
	from pandas import DataFrame
	import numpy as n

	df_out = DataFrame()

	## extinction coe.
	df_out['extinction'] = df_abs['BC6'].copy()+df_sca['G'].copy()

	## SSA
	df_out['SSA'] = df_sca['G'].copy()/df_out['extinction'].copy()

	return df_out


