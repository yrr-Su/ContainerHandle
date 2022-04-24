



__all__ = [
			'_basic'



	]



def _basic(df):
	import numpy as n

	## get number conc. data and total, mode
	dN 	   = df[df.keys()[:-2]]
	df_oth = df[df.keys()[-2:]]

	out_dic = {}
	## diameter
	dp 		= dN.keys().to_numpy()
	dlog_dp = n.diff(n.log10(dp)).mean()
	
	## calculate normalize and non-normalize data
	out_dic['number']  = dN*dlog_dp
	out_dic['surface'] = out_dic['number']*n.pi*dp**2
	out_dic['volume']  = out_dic['number']*n.pi*(dp**3)/6

	out_dic['number_norm']  = dN
	out_dic['surface_norm'] = out_dic['number_norm']*n.pi*dp**2
	out_dic['volume_norm']  = out_dic['number_norm']*n.pi*(dp**3)/6

	## mode and total
	out_dic['other'] = df_oth

	return out_dic




