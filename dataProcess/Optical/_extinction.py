

def _extCoe(df_abs,df_sca):

	df_ext = DataFrame()
	df_ext['ext'] = df_abs['BC6']+df_sca['G']

	return df_ext['ext']


def _SSA(df_abs,df_sca):

	_extCoe

	df_ext = DataFrame()
	df_ext['ext'] = df_abs['BC6']+df_sca['G']

	return df_ext['ext']



def _basic(df_abs,df_sca):
	from pandas import DataFrame
	import numpy as n

	df_out = DataFrame(n.nan).set_index(df_abs.index)

	## extinction coe.
	df_out['ext'] = df_abs['BC6']+df_sca['G']


