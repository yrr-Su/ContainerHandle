



__all__ = [
			'_basic'



	]


def _geometric_prop(_dp,_prop):
	import numpy as n

	_prop_t = _prop.sum(axis=1)
	_prop_t = _prop_t.where(_prop_t>0).copy()

	_dp = n.log(_dp)
	_gmd = (((_prop*_dp).sum(axis=1))/_prop_t.copy())


	_dp_mesh, _gmd_mesh = n.meshgrid(_dp,_gmd)
	_gsd = ((((_dp_mesh-_gmd_mesh)**2)*_prop).sum(axis=1)/_prop_t.copy())**.5

	return _prop_t, _gmd.apply(n.exp), _gsd.apply(n.exp)


def _basic(df):
	import numpy as n

	## get number conc. data and total, mode
	dN 	   = df[df.keys()[:-2]].copy()
	df_oth = df[df.keys()[-2:]].copy()

	out_dic = {}
	## diameter
	dp 		= dN.keys().to_numpy(float)
	dlog_dp = n.diff(n.log10(dp)).mean()
	
	## calculate normalize and non-normalize data
	out_dic['number']  = dN*dlog_dp
	out_dic['surface'] = out_dic['number']*n.pi*dp**2
	out_dic['volume']  = out_dic['number']*n.pi*(dp**3)/6

	out_dic['number_norm']  = dN
	out_dic['surface_norm'] = out_dic['number_norm']*n.pi*dp**2
	out_dic['volume_norm']  = out_dic['number_norm']*n.pi*(dp**3)/6

	## mode, total and GMD
	df_oth['total'], df_oth['GMD'], df_oth['GSD'] = _geometric_prop(dp,out_dic['number'])
	df_oth['total_surf'], df_oth['GMD_surf'], df_oth['GSD_surf'] = _geometric_prop(dp,out_dic['surface'])
	df_oth['total_volume'], df_oth['GMD_volume'], df_oth['GSD_volume'] = _geometric_prop(dp,out_dic['volume'])

	out_dic['other'] = df_oth

	return out_dic

   


