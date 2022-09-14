



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


def _basic(df,hybrid,unit):
	
	import numpy as n
	from pandas import DataFrame

	## get number conc. data and total, mode
	dN = df
	dN.columns = dN.keys().to_numpy(float)

	out_dic = {}
	## diameter
	dp = dN.keys().to_numpy()
	if hybrid:
		dlog_dp = n.diff(n.log10(dp)).mean()
	else:
		dlog_dp = n.ones(dp.size)
		dlog_dp[:hybrid] = n.diff(n.log10(dp[:hybrid])).mean()
		dlog_dp[hybrid:] = n.diff(n.log10(dp[hybrid:])).mean()

	## calculate normalize and non-normalize data
	out_dic['number']  = dN*dlog_dp
	out_dic['surface'] = out_dic['number']*n.pi*dp**2
	out_dic['volume']  = out_dic['number']*n.pi*(dp**3)/6

	out_dic['number_norm']  = dN
	out_dic['surface_norm'] = out_dic['number_norm']*n.pi*dp**2
	out_dic['volume_norm']  = out_dic['number_norm']*n.pi*(dp**3)/6

	## mode 
	df_mode = DataFrame(index=dN.index)

	bound = n.array([(11,25),(25,100),(100,1e3),(1e3,2.5e3),])
	if unit=='um':
		bound /= 1e3

	for _nam, _range in zip(['Nucleation','Aitken','Accumulation','Coarse'],bound):

		_dia = dp[(dp>_range[0])&(dp<_range[-1])]

		if ~_dia.any(): continue
		
		_dN = dN[_dia].copy()
		df_mode[f'{_nam}_mode'] = _dN.idxmax(axis=1)
		df_mode[f'{_nam}_conc'] = _dN.max(axis=1)

	out_dic['mode'] = df_mode
	
	## total, GMD and GSD
	df_oth = DataFrame(index=dN.index)

	df_oth['total'], df_oth['GMD'], df_oth['GSD'] = _geometric_prop(dp,out_dic['number'])
	df_oth['total_surf'], df_oth['GMD_surf'], df_oth['GSD_surf'] = _geometric_prop(dp,out_dic['surface'])
	df_oth['total_volume'], df_oth['GMD_volume'], df_oth['GSD_volume'] = _geometric_prop(dp,out_dic['volume'])

	out_dic['other'] = df_oth

	return out_dic