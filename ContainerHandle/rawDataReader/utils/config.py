
meta = {

		"__comment"    : "meta data for rawDataReader",
		"__instrument" : ["AE33","AE43","NEPH","SMPS_NTU(SMPS_3080_3788)",
						  "SMPS_TH(SMPS_3080_3772)","APS_3321","TEOM","OCEC"],


		"Aurora" : {
				  "pattern"   : r".*\.csv$",
				  "freq"	  : "1T",
				  "deter_key" : { "Scatter Coe. (550 nm)" : ["G"] },

				  },

		"NEPH" : {
				  "pattern"   : r".*\.DAT$",
				  "freq"	  : "5T",
				  "deter_key" : { "Scatter Coe. (550 nm)" : ["G"] },

				  },

		"Table" : {
				   "pattern"   : r".*\.csv$",
				   "freq"	   : "1h",
				   "deter_key" : None,

				   },

		"EPA_vertical" : {
				   "pattern"   : r".*\.csv$",
				   "freq"	   : "1h",
				   "deter_key" : None,

				   },

		"SMPS_TH" : {
					 "pattern"   : r".*\.txt$",
					 "freq"		 : "6T",
					 "deter_key" : { "Bins" : ["all"] },

					 },

		"SMPS_genr" : {
					 "pattern"   : r".*\.txt$",
					 "freq"		 : "6T",
					 "deter_key" : { "Bins" : ["all"] },

					 },

		"SMPS_aim11" : {
					 "pattern"   : r".*\.csv$",
					 "freq"		 : "6T",
					 "deter_key" : { "Bins" : ["all"] },

					 },

		"APS_3321" : {
					  "pattern"   : r".*\.TXT$",
					  "freq"	  : "6T",
					 "deter_key" : { "Bins" : ["all"] },

					  },

		"AE33" : {
				  "pattern"	  : r"^(?!.*(ST|CT|FV|log)).*_AE33.*\.dat$",
				  "freq"	  : "1T",
				  "deter_key" : { "BC Mass Conc. (880 nm)" : ["BC6"] },

				  },

		"AE43" : {
				  "pattern"	  : r"^(?!.*(ST|CT|FV|log)).*_AE43.*\.dat$",
				  "freq"	  : "1T",
				  "deter_key" : { "BC Mass Conc. (880 nm)" : ["BC6"] },
				},

		"TEOM" : {
				  "pattern"	  : r".*\.csv$",
				  "freq"	  : "6T",
				  "deter_key" : { "PM1.0 Mass Conc." : ["PM_Total"], 
								  "PM1.0 NV Mass Conc." : ["PM_NV"],}

				  },

		"OCEC_LCRES" : {
					    "pattern"   : r".*LCRes\.csv$",
					    "freq"	    : "1h",
					    "deter_key" : { "Thermal OC/EC" : ["Thermal_EC", "Thermal_OC"],
										"Thermal OC" : ["Thermal_OC"],
										"Thermal EC" : ["Thermal_EC"],
										"Optical OC/EC" : ["Optical_EC", "Optical_OC"],
										"Optical OC" : ["Optical_OC"],
										"Optical EC" : ["Optical_EC"],}

					},

		"OCEC_RES" : {
					    "pattern"   : r"^(?!(.*LC|.*Blanks)).*Res\.csv$",
					    "freq"	    : "1h",
					    "deter_key" : None,

					},

		"IGAC_TH" : {
				   "pattern"   : r".*\.csv$",
				   "freq"	   : "1h",
				   "deter_key" : { "Na+"   : ["Na+"],
								   "NH4+"  : ["NH4+"],
								   "K+"	   : ["K+"],
								   "Mg2+"  : ["Mg2+"],
								   "Ca2+"  : ["Ca2+"],
								   "Cl-"   : ["Cl-"],
								   "NO2-"  : ["NO2-"],
								   "NO3-"  : ["NO3-"],
								   "SO42-" : ["SO42-"],
								   "Main Salt (NH4+, NO3-, SO42-)" : ["NO3-","SO42-","NH4+"],
								},
				   },

		"IGAC_ZM" : {
				   "pattern"   : r".*\.csv$",
				   "freq"	   : "1h",
				   "deter_key" : { "Na+"   : ["Na+"],
								   "NH4+"  : ["NH4+"],
								   "K+"	   : ["K+"],
								   "Mg2+"  : ["Mg2+"],
								   "Ca2+"  : ["Ca2+"],
								   "Cl-"   : ["Cl-"],
								   "NO2-"  : ["NO2-"],
								   "NO3-"  : ["NO3-"],
								   "SO42-" : ["SO42-"],
								   "Main Salt (NH4+, NO3-, SO42-)" : ["NO3-","SO42-","NH4+"],
								},

				   },

		"VOC_TH" : {
				   "pattern"   : r".*\.csv$",
				   "freq"	   : "1h",
				   "deter_key" : None,

				   },

		"VOC_ZM" : {
				   "pattern"   : r".*\.csv$",
				   "freq"	   : "1h",
				   "deter_key" : None,

				   },







}
