


from pandas import date_range, concat, DataFrame, to_numeric
from scipy.optimize import curve_fit
import numpy as n
np = n

__all__ = [
			'_basic',
			# '_ocec_ratio_cal',



	]


def _ocec_ratio_cal(_lcres_splt,_hr_lim,_range):

	if (_lcres_splt.resample('1m').size().values[0]<=_hr_lim):

		print(f"\t\t{_lcres_splt.index[0].strftime('%Y-%m-%d %X')} to {_lcres_splt.index[-1].strftime('%Y-%m-%d %X')}")
		print('\t\tPlease Modify the Values of "hour_limit" or Input Sufficient Amount of Data !!')
		_lcres_splt[['OC/EC','SOC','POC']] = n.nan

		return _lcres_splt[['OC/EC','SOC','POC']]

	_oc, _ec = _lcres_splt['Thermal_OC'], _lcres_splt['Thermal_EC']

	_ocec_table = n.arange(_range[0],_range[1]+_range[2],_range[2])

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

	_ocec_ratio = DataFrame(_r2_dic,index=[0]).idxmin(axis=1).values[0]

	_lcres_splt['OC/EC'] = _ocec_ratio
	_lcres_splt['SOC']   = _soc_table[_ocec_ratio]
	_lcres_splt['POC']	 = _lcres_splt['Thermal_OC']-_lcres_splt['SOC']

	return _lcres_splt[['OC/EC','SOC','POC']]


def _basic(_lcres,_res,_mass,_ocec_ratio_month,_hr_lim,_range):

	_out = {}

	## OC1, OC2, OC3, OC4, PC
	_out['basic'] = _res/_lcres['Sample_Volume'].to_frame().values.copy()

	## SOC, POC, OC/EC
	_df_lst = []
	for _, _df in _lcres.resample(f'{_ocec_ratio_month}m'):
		_df_lst.append(_ocec_ratio_cal(_lcres,_hr_lim,_range))

	_prcs_df = concat(_df_lst)
	_out['basic'] = concat((_out['basic'].copy(),_prcs_df[['POC','SOC']]),axis=1)

	## ratio
	_ratio_df = DataFrame(index=_out['basic'].index)

	for _ky, _val in _out['basic'].items():
		_ratio_df[f'{_ky}/Thermal_OC'] = _val/_lcres['Thermal_OC']

	if _mass is not None:
		for _ky, _val in _out['basic'].items():
			_ratio_df[f'{_ky}/PM'] = _val/_mass

		_ratio_df[f'Thermal_OC/PM'] = _lcres['Thermal_OC']/_mass
		_ratio_df[f'Thermal_EC/PM'] = _lcres['Thermal_EC']/_mass

	## out
	_out['ratio'] = _ratio_df
	_out['basic'] = concat((_out['basic'].copy(),_lcres),axis=1)
	_out['basic']['OC/EC'] = _prcs_df['OC/EC']

	## ratio status
	for _ky, _df in _ratio_df.items():
		_out['basic'][f'{_ky}_status'] = 'Normal'
		_out['basic'][f'{_ky}_status'] = _out['basic'][f'{_ky}_status'].mask(_df>1,'Warning')

	return _out
