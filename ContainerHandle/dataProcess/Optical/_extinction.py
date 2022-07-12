

def _basic(df_abs,df_sca,df_pm25):
	from pandas import DataFrame
	import numpy as n

	df_out = DataFrame()

	## abs and sca coe
	df_out['abs'] = df_abs['BC6'].copy()
	df_out['sca'] = df_sca['G'].copy()

	## extinction coe.
	df_out['ext'] = df_out['abs']+df_out['sca']

	## SSA
	df_out['SSA'] = df_out['sca']/df_out['ext']

	## MAE, MSE, MEE
	df_out['MAE'] = df_out['abs']/df_pm25
	df_out['MSE'] = df_out['sca']/df_pm25
	df_out['MEE'] = df_out['MSE']+df_out['MAE']

	return df_out


