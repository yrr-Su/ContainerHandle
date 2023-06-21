

from PyMieScatt import Mie_SD
from pandas import date_range, concat, DataFrame, to_numeric


def _mie(_psd_ori, _RI_ori, _wave):


	_ori_idx = _psd_ori.index.copy()
	_cal_idx = _psd_ori.loc[_RI_ori.dropna().index].dropna(how='all').index
	
	_psd, _RI = _psd_ori.loc[_cal_idx], _RI_ori.loc[_cal_idx]

	## parameter
	_bins = _psd.keys().tolist()
	
	## calculate
	_dt_lst = []
	for _dt, _m in zip(_psd.values,_RI.values):

		_out_dic = Mie_SD(_m,_wave,_bins,_dt,asDict=True)
		_dt_lst.append(_out_dic)

	_out = DataFrame(_dt_lst,index=_cal_idx).reindex(_ori_idx)

	_out = _out.rename(columns={ 'Bext'   : 'ext',
								 'Bsca'   : 'sca',
								 'Babs'   : 'abs',
								 'Bback'  : 'back',
								 'Bratio' : 'ratio',
								 'Bpr'	  : 'pr',})

	return _out[['abs','sca','ext','back','ratio','pr','G']]


