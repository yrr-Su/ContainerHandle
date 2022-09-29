


from pandas import date_range, concat, DataFrame, to_numeric


def _basic(df_che,df_ref,df_water,nam_lst):

	df_all = concat(df_che,axis=1)
	index  = df_all.index.copy()
	df_all.columns = nam_lst

	## parameter
	mol_A, mol_S, mol_N  = df_all['NH4+']/18, df_all['SO42-']/96, df_all['NO3-']/62
	df_all['status'] = (mol_A)/(2*mol_S+mol_N)

	convert_nam = {'AS'   : 'SO42-',
				   'AN'   : 'NO3-',
				   'OM'   : 'OC',
				   'Soil' : 'Fe',
				   'SS'   : 'Na+',
				   'EC'   : 'EC',
				   }

	mass_coe = {'AS'   : 1.375,
				'AN'   : 1.29,
				'OM'   : 1.8,
				'Soil' : 23.57,
				'SS'   : 2.54,
				'EC'   : 1,
				}

	vol_coe  = {'AS'   : 1.76,
				'AN'   : 1.73,
				'OM'   : 1.4,
				'Soil' : 2.6,
				'SS'   : 2.16,
				'EC'   : 1.5,
				}

	RI_coe	 = {'ALWC' : 1.333+0j,
			    'AS'   : 1.53+0j,
			    'AN'   : 1.55+0j,
			    'OM'   : 1.55+0.0179j,
			    'Soil' : 1.56+0.01j,
			    'SS'   : 1.54+0j,
			    'EC'   : 1.80+0.54j
				}

	## mass
	## NH4 Enough
	df_mass   = DataFrame()
	df_enough = df_all.where(df_all['status']>=1).dropna().copy()

	for _mass_nam, _coe in mass_coe.items():
		df_mass[_mass_nam] = df_all[convert_nam[_mass_nam]]*_coe

	## NH4 Deficiency
	defic_idx = df_all['status']<1

	if defic_idx.any():
		residual = mol_A-2*mol_S

		## residual > 0
		_status = residual>0
		if _status.any():

			_cond = _status&(residual<=mol_N)
			df_mass.loc[_cond,'AN'] = residual.loc[_cond]*80

			_cond = _status&(residual>mol_N)
			df_mass.loc[_cond,'AN'] = mol_N.loc[_cond]*80

		## residual < 0
		_status = residual<=0
		if _status.any():

			df_mass.loc[_status,'AN'] = 0

			_cond = _status&(mol_A<=2*mol_S)
			df_mass.loc[_cond,'AS'] = mol_A.loc[_cond]/2*132

			_cond = _status&(mol_A>2*mol_S)
			df_mass.loc[_cond,'AS'] = mol_S.loc[_cond]*132

	df_mass = df_mass.dropna()

	## volume
	df_vol = DataFrame()
	for _vol_nam, _coe in vol_coe.items():
		df_vol[_vol_nam] = df_mass[_vol_nam]/_coe

	if df_water is not None:
		df_vol['ALWC'] = df_water
		df_vol = df_vol.dropna()
		df_vol['total_wet'] = df_vol.sum(axis=1)

	df_vol['total_dry'] = df_vol[vol_coe.keys()].sum(axis=1)

	## refractive index
	df_RI = DataFrame()

	for _ky, _df in df_vol.items():
		if 'total' in _ky: continue
		df_RI[_ky] = (_df*RI_coe[_ky])
	
	if df_water is not None:
		df_RI['RI_wet'] = (df_RI/df_vol['total_wet'].to_frame().values).sum(axis=1)

	df_RI['RI_dry'] = (df_RI[vol_coe.keys()]/df_vol['total_dry'].to_frame().values).sum(axis=1)

	## out
	out = { 'mass'   : df_mass.reindex(index),
			'volume' : df_vol.reindex(index),
			'RI' 	 : df_RI[['RI_dry','RI_wet']].reindex(index),
			}

	return out
	


# '''


def mass_ratio(_df):
    if _df['PM25'] >= _df['total_mass']:
        _df['others'] = _df['PM25'] - _df['total_mass']
        for _val, _species in zip(_df.values, _df.index):
            _df[f'{_species}_ratio'] = _val / _df['PM25'].__round__(3)

    if _df['PM25'] < _df['total_mass']:
        _df['others'] = 0
        for _val, _species in zip(_df.values, _df.index):
            _df[f'{_species}_ratio'] = _val / _df['PM25'].__round__(3)

    return _df['others':].drop(labels=['PM25_ratio', 'total_mass_ratio'])






