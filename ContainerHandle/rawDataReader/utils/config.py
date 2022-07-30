
meta = {

		"__comment"    : "meta data for rawDataReader",
		"__instrument" : ["AE33","AE43","NEPH","SMPS_NTU(SMPS_3080_3788)",
						  "SMPS_TH(SMPS_3080_3772)","APS_3321","TEOM"],


		"NEPH" : {
				  "pattern"   : "*.DAT",
				  "freq"	  : "5T",
				  "deter_key" : "G",

				  },

		"Meteo" : {
				   "pattern"   : "*.csv",
				   "freq"	   : "1h",
				   "deter_key" : None,

				   },

		"SMPS_TH" : {
					 "pattern"   : "*.txt",
					 "freq"		 : "6T",
					 "deter_key" : "mode",

					 },

		"APS_3321" : {
					  "pattern"   : "*.TXT",
					  "freq"	  : "6T",
					  "deter_key" : "mode",

					  },

		"AE33" : {
				  "pattern"	  : "[!ST|!CT|!FV]*[!log]_AE33*.dat",
				  "freq"	  : "1T",
				  "deter_key" : "BC6",

				  },

		"AE43" : {
				  "pattern"	  : "[!ST|!CT|!FV]*[!log]_AE43*.dat",
				  "freq"	  : "1T",
				  "deter_key" : "BC6",

				  },







}
