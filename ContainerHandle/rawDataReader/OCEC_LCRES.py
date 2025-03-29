

from .core import _reader
from pandas import to_datetime, read_csv
from datetime import datetime as dtm
from pathlib import Path
import numpy as n


class reader(_reader):

	nam = 'OCEC_LCRES'

	def _raw_reader(self,_file):
		with open(_file, 'r', encoding='utf-8', errors='ignore') as f:
			_df = read_csv(f, skiprows=3)

			deflt_key = ['Thermal/Optical OC (ugC/LCm^3)', 'Thermal/Optical EC (ugC/LCm^3)', 'OC=TC-BC (ugC/LCm^3)', 'BC (ugC/LCm^3)',
						 'Sample Volume Local Condition Actual m^3', 'TC (ugC/LCm^3)']
			deflt_nam = ['Thermal_OC', 'Thermal_EC', 'Optical_OC', 'Optical_EC', 'Sample_Volume', 'TC']

			keys = self._oth_set.get('keys') or deflt_key

			_col = {}
			for _dflt_ky, _dflt_nam in zip(keys, deflt_nam):
				_col[_dflt_ky] = _dflt_nam

			_tm_idx = to_datetime(_df['Start Date/Time'], errors='coerce')
			_df['time'] = _tm_idx

			_df = _df.dropna(subset='time').loc[~_tm_idx.duplicated()].set_index('time')

		return _df[_col.keys()].rename(columns=_col)

	## QC data
	def _QC(self,_df):

		_df[['Thermal_OC', 'Optical_OC']] = _df[['Thermal_OC', 'Optical_OC']].where(_df[['Thermal_OC', 'Optical_OC']] > 0.3).copy()
		_df[['Thermal_EC', 'Optical_EC']] = _df[['Thermal_EC', 'Optical_EC']].where(_df[['Thermal_EC', 'Optical_EC']] > .015).copy()

		return _df



# _col = { 'Thermal/Optical OC (ugC/LCm^3)' : 'Thermal_OC',
		 # 'Thermal/Optical EC (ugC/LCm^3)' : 'Thermal_EC',
		 # 'OC=TC-BC (ugC/LCm^3)' : 'Optical_OC',
		 # 'BC (ugC/LCm^3)' 	    : 'Optical_EC',
		 # 'Sample Volume Local Condition Actual m^3' : 'Sample_Volume',
		 # 'TC (ugC/LCm^3)' : 'TC',}
