

def _basic(df_abs,df_sca,df_pm25):
	from pandas import DataFrame
	import numpy as n

	df_out = DataFrame()

	## extinction coe.
	df_out['extinction'] = df_abs['BC6'].copy()+df_sca['G'].copy()

	## SSA
	df_out['SSA'] = df_sca['G'].copy()/df_out['extinction'].copy()

	## MAE, MSE, MEE
	df_out['MAE'] = df_abs['BC6'].copy()/df_pm25
	df_out['MSE'] = df_sca['G'].copy()/df_pm25
	df_out['MEE'] = df_out['MSE']+df_out['MAE']

	return df_out


