
from pandas import date_range, concat, DataFrame

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
	


