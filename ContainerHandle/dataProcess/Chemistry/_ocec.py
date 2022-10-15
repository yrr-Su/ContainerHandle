


from pandas import date_range, concat, DataFrame, to_numeric
from scipy.optimize import curve_fit
import numpy as n
np = n

__all__ = [
			'_basic',
			# '_ocec_ratio_cal',



	]


def _ocec_ratio_cal(_lcres_splt,_hr_lim,_range):

	## parameter 
	_out = DataFrame(index=_lcres_splt.index)
	_oc, _ec = _lcres_splt['Thermal_OC'], _lcres_splt['Thermal_EC']

	## real data OC/EC
	_ocec_ratio_real = (_oc/_ec).quantile(.5)

	_out['OC/EC_real'] = _ocec_ratio_real
	_out['POC_real'] = _ocec_ratio_real*_ec
	_out['SOC_real'] = _oc-_out['POC_real']

	## estimated OC/EC
	## the least R2 method
	if (_lcres_splt.resample('1m').size().values[0]<=_hr_lim):

		print(f"\t\t{_lcres_splt.index[0].strftime('%Y-%m-%d %X')} to {_lcres_splt.index[-1].strftime('%Y-%m-%d %X')}")
		print('\t\tPlease Modify the Values of "hour_limit" or Input Sufficient Amount of Data !!')
		_out[['OC/EC','POC','SOC']] = n.nan

		return _out

	_ocec_ratio = False
	_st, _ed, _stp = _range

	for _ in range(2):
		if _ocec_ratio:
			_ocec_table = n.arange(_ocec_ratio-_stp/2,_ocec_ratio+_stp/2,.01).round(2)
		else:
			_ocec_table = n.arange(_st,_ed+_stp,_stp).round(2)

		_ocec_mesh, _oc_mesh = n.meshgrid(_ocec_table,_oc)
		_ocec_mesh, _ec_mesh = n.meshgrid(_ocec_table,_ec)

		_soc_table = DataFrame(_oc_mesh-_ocec_mesh*_ec_mesh,index=_oc.index,columns=_ocec_table)
		
		## calculate R2
		_r2_dic = {}
		_func = lambda _x, _sl, _inte : _sl*_x+_inte
		for _ocec, _soc in _soc_table.items():

			_df = DataFrame([_soc.values,_ec.values]).T.dropna()
			_x, _y = _df[0], _df[1]

			_opt, _ = curve_fit(_func,_x,_y)

			_tss = n.sum((_y-_y.mean())**2.)
			_rss = n.sum((_y-_func(_x,*_opt))**2.)

			_r2_dic[round(_ocec,2)] = 1.-_rss/_tss

		## get the min R2
		_ocec_ratio = DataFrame(_r2_dic,index=[0]).idxmin(axis=1).values[0]

	## out
	_out['OC/EC'] = _ocec_ratio
	_out['SOC']   = _soc_table[_ocec_ratio]
	_out['POC']	  = _oc-_out['SOC']

	return _out[['OC/EC','POC','SOC','OC/EC_real','POC_real','SOC_real']]


def _basic(_lcres,_res,_mass,_ocec_ratio,_ocec_ratio_month,_hr_lim,_range):

	_out = {}

	## OC1, OC2, OC3, OC4, PC
	_df_bsc = _res/_lcres['Sample_Volume'].to_frame().values.copy()

	## SOC, POC, OC/EC
	if _ocec_ratio is not None:
		try:
			iter(_ocec_ratio)
		except TypeError:
			raise TypeError('"ocec_ratio" Only Accept a Single Value !!')

		_prcs_df = DataFrame(index=_df_bsc.index)
		_prcs_df['OC/EC'] = _ocec_ratio
		_prcs_df['POC']	  = _ocec_ratio*_lcres['Thermal_EC']
		_prcs_df['SOC']   = _lcres['Thermal_OC']-_prcs_df['POC']

	else:
		_df_lst = []
		for _, _df in _lcres.resample(f'{_ocec_ratio_month}m'):
			_df_lst.append(_ocec_ratio_cal(_df,_hr_lim,_range))

		_prcs_df = concat(_df_lst)

	_df_bsc = concat((_df_bsc.copy(),_prcs_df),axis=1)

	## ratio
	_df_ratio = DataFrame(index=_df_bsc.index)

	for _ky, _val in _df_bsc.items():
		if 'OC/EC' in _ky: continue
		_df_ratio[f'{_ky}/Thermal_OC'] = _val/_lcres['Thermal_OC']

	if _mass is not None:
		for _ky, _val in _df_bsc.items():
			_df_ratio[f'{_ky}/PM'] = _val/_mass

		_df_ratio[f'Thermal_OC/PM'] = _lcres['Thermal_OC']/_mass
		_df_ratio[f'Thermal_EC/PM'] = _lcres['Thermal_EC']/_mass

	## ratio status
	_df_bsc = concat((_lcres,_df_bsc.copy()),axis=1)

	for _ky, _df in _df_ratio.items():
		_df_bsc[f'{_ky}_status'] = 'Normal'
		_df_bsc[f'{_ky}_status'] = _df_bsc[f'{_ky}_status'].mask(_df>1,'Warning')
	
	## out
	_out['ratio'] = _df_ratio
	_out['basic'] = _df_bsc


	return _out
