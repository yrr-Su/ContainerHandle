








from pandas import date_range, concat, DataFrame, to_numeric


# def _mass_cal(df_am,df):




def _basic(df_che,df_ref,df_water,nam_lst):

	df_all = concat(df_che,axis=1)
	index  = df_all.index.copy()
	df_all.columns = nam_lst

	## parameter
	mol_A, mol_S, mol_N  = df_all['NH4+']/18, df_all['SO42-']/96, df_all['NO3-']/62
	df_all['status'] = (mol_A)/(2*mol_S+mol_N)

	convert_nam = { 'AS'   : 'SO42-',
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

	## mass
	## NH4 Enough
	df_mass   = DataFrame()
	df_enough = df_all.where(df_all['status']>=1).dropna().copy()

	for _mass_nam, _coe in mass_coe.items():
		df_mass[_mass_nam] = df_all[convert_nam[_mass_nam]]*_coe

	## NH4 Deficiency
	defic_idx = df_all['status']<1
	# defic_idx = df_all['status']>5

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

	## volume
	df_vol = DataFrame()
	for _vol_nam, _coe in vol_coe.items():
		df_vol[_vol_nam] = df_mass[_vol_nam]/_coe
	
	if df_water:
		df_vol['ALWC'] = df_water

	## out
	out = { 'mass'   : df_mass.reindex(index),
			'volume' : df_vol.reindex(index),

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


def volume(_df):
    _df['AS_volume']   = (_df['AS_mass'] / 1.76).__round__(3)
    _df['AN_volume']   = (_df['AN_mass'] / 1.73).__round__(3)
    _df['OM_volume']   = (_df['OM_mass'] / 1.4).__round__(3)
    _df['Soil_volume'] = (_df['Soil_mass'] / 2.6).__round__(3)
    _df['SS_volume']   = (_df['SS_mass'] / 2.16).__round__(3)
    _df['EC_volume']   = (_df['EC_mass'] / 1.5).__round__(3)
    _df['ALWC_volume'] = (_df['ALWC'] / 1).__round__(3)
    _df['total_volume'] = sum(_df['AS_volume':'ALWC_volume']).__round__(3)

    V_dry = sum(_df['AS_volume':'EC_volume']).__round__(3)
    V_wet = _df['total_volume']
    _df['gRH'] = (V_wet**(1/3)) / (V_dry**(1/3))

    for _val, _species in zip(_df['AS_volume':'ALWC_volume'].values, _df['AS_volume':'ALWC_volume'].index):
        _df[f'{_species}_ratio'] = _val / _df['total_volume'].__round__(3)

    _df['n_amb'] = (1.53 * _df['AS_volume_ratio']+ \
                   1.55 * _df['AN_volume_ratio']+\
                   1.55 * _df['OM_volume_ratio']+\
                   1.56 * _df['Soil_volume_ratio']+\
                   1.54 * _df['SS_volume_ratio']+\
                   1.8 * _df['EC_volume_ratio']+\
                   1.333 * _df['ALWC_volume_ratio']).__round__(4)

    _df['k_amb'] = (0.00*_df['OM_volume_ratio']+\
                   0.01*_df['Soil_volume_ratio']+\
                   0.54*_df['EC_volume_ratio']).__round__(4)

    _df['n_dry'] = ((1.53 * _df['AS_volume_ratio']+ \
                   1.55 * _df['AN_volume_ratio']+\
                   1.55 * _df['OM_volume_ratio']+\
                   1.56 * _df['Soil_volume_ratio']+\
                   1.54 * _df['SS_volume_ratio']+\
                   1.8 * _df['EC_volume_ratio']) * (1/(1-_df['ALWC_volume_ratio']))).__round__(4)

    _df['k_dry'] = ((0.00*_df['OM_volume_ratio']+\
                    0.01*_df['Soil_volume_ratio']+\
                    0.54*_df['EC_volume_ratio']) * (1/(1-_df['ALWC_volume_ratio']))).__round__(4)

    return _df['AS_volume':]
# '''








