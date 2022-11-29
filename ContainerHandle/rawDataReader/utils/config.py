
meta = {

		"__comment"    : "meta data for rawDataReader",
		"__instrument" : ["AE33","AE43","NEPH","SMPS_NTU(SMPS_3080_3788)",
						  "SMPS_TH(SMPS_3080_3772)","APS_3321","TEOM","OCEC"],


		"NEPH" : {
				  "pattern"   : "*.DAT",
				  "freq"	  : "5T",
				  "deter_key" : { "Scatter Coe. (550 nm)" : ["G"] },

				  },

		"Table" : {
				   "pattern"   : "*.csv",
				   "freq"	   : "1h",
				   "deter_key" : None,

				   },

		"EPA_vertical" : {
				   "pattern"   : "*.csv",
				   "freq"	   : "1h",
				   "deter_key" : None,

				   },

		"SMPS_TH" : {
					 "pattern"   : "*.txt",
					 "freq"		 : "6T",
					 "deter_key" : { "Bins" : ["all"] },

					 },

		"APS_3321" : {
					  "pattern"   : "*.TXT",
					  "freq"	  : "6T",
					 "deter_key" : { "Bins" : ["all"] },

					  },

		"AE33" : {
				  "pattern"	  : "[!ST|!CT|!FV]*[!log]_AE33*.dat",
				  "freq"	  : "1T",
				  "deter_key" : { "BC Mass Conc. (880 nm)" : ["BC6"] },

				  },

		"AE43" : {
				  "pattern"	  : "[!ST|!CT|!FV]*[!log]_AE43*.dat",
				  "freq"	  : "1T",
				  "deter_key" : { "BC Mass Conc. (880 nm)" : ["BC6"] },
				},

		"TEOM" : {
				  "pattern"	  : "*.csv",
				  "freq"	  : "6T",
				  "deter_key" : { "PM1.0 Mass Conc." : ["PM_Total"], 
								  "PM1.0 NV Mass Conc." : ["PM_NV"],}

				  },

		"OCEC_LCRES" : {
					    "pattern"   : "*LCRes.csv",
					    "freq"	    : "1h",
					    "deter_key" : { "Thermal OC/EC" : ["Thermal_OC","Thermal_EC",] },

					},

		"OCEC_RES" : {
					    "pattern"   : "*[!LC|!Blanks]Res.csv",
					    "freq"	    : "1h",
					    "deter_key" : None,

					},







}
