

def _basic(df_abs,df_sca,df_ec,df_mass):
	from pandas import DataFrame
	import numpy as n

	df_out = DataFrame()

	## abs and sca coe
	df_out['abs'] = df_abs.copy()
	df_out['sca'] = df_sca.copy()

	## extinction coe.
	df_out['ext'] = df_out['abs']+df_out['sca']

	## SSA
	df_out['SSA'] = df_out['sca']/df_out['ext']

	## MAE, MSE, MEE
	if df_mass is not None:
		df_out['MAE'] = df_out['abs']/df_mass
		df_out['MSE'] = df_out['sca']/df_mass
		df_out['MEE'] = df_out['MSE']+df_out['MAE']

	## other
	if df_ec is not None:
		df_out['eBC'] = df_ec

	return df_out


