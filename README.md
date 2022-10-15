# ContainerHandle
container data process, raw data, different instrument

## rawDataReader

* NEPH
* Table
* APS_3321
* SMPS_TH
* AE33
* AE43
* TEOM
* OCEC_RES
* OCEC_LCRES

## dataProcess

### Chemistry

**ReConstrc_basic(*df_chem, df_ref=None, df_water=None, nam_lst=['NH4+','SO42-','NO3-','Fe','Na+','OC','EC'])**

* ***df_chem** : *DataFrame or Serie scollection*

  * Some chemical compound dataframe(mass concentration), the order of the input dataframe can control by **nam_lst**
* **df_ref** : *DataFrame or Series, default : None*

  * Mass concentration of PM, to compare with the reconstructed mass
* **df_water** : *DataFrame or Series, default : None*
  * Mass concentration of ALWC, to reconstruct the wet parameter
* **nam_lst** : *array-like, default : ['NH4+','SO42-','NO3-','Fe','Na+','OC','EC']*
  * The order of the **df_chem**


***Returns : dictionary***

* *mass* : reconstructed mass concentration, including ALWC and total wet mass if **df_water** is not None
* *volume* : reconstructed volume concentration, including ALWC and total wet volume if **df_water** is not None
* *RI* : refractive index, including wet RI if **df_water** is not None

---

**OCEC_basic(df_lcres, df_res, df_mass=None, ocec_ratio=None, ocec_ratio_month=1, hr_lim=200, least_square_range=(0.1,2.5,0.1))**

* **df_lcres** : *DataFrame*
  * LCRES data made by **rawDataReader.OCEC_LCRES**
* **df_res** : *DataFrame*
  * RES data made by **rawDataReader.OCEC_RES**
* **df_mass** : *DataFrame or Series, default : None*
  * To calculate the mass ratio with PM data
* **ocec_ratio** : *float, default : None*
  * To calculate POC and SOC
* **ocec_ratio_month** : *int, default : 1*
  * The number of the OC/EC calculated month, be ignore if **ocec_ratio** is not none
* **hr_lim** : *int, default : 200*
  * The minimum hours in given month(**ocec_ratio_month**) allow to calculate the OC/EC, be ignore if **ocec_ratio** is not none
* **least_square_range** : *3-tuple, default : (0.1,2.5,0.1)*
  * (start, end, step), the assumed value of OC/EC, be ignore if **ocec_ratio** is not none

***Return : Dictionary***

* *basic* : basic parameters and mass ratio status
* *ratio* : mass ratio

---

**TEOM_basic(df_teom,df_check=None)**

* **df_teom** : *DataFrame*
  * TEOM data made by **rawDataReader.TEOM**
* **df_check** : *DataFrame or Series, default : None*
  * The reference data to check the data accuracy

***Return : DataFrame***

* TEOM parameter

### Optical

**SAE(df_sca)**

* **df_sca** : *DataFrame or Series*
  * Scatter data made by **rawDataReader.NEPH**

***Return : DataFrame***

* Scatter angstrom exponential

---

absCoe

---

**AAE(df_abs)**

* **df_abs** : *DataFrame or Series*
  * Absorption coefficient data

***Return : DataFrame***

* Absorption angstrom exponential

---

**basic(df_abs, df_sca, df_ec=None, df_mass=None)**

* **df_abs** : *DataFrame or Series*
  * Absorption angstrom exponential
* **df_sca** : *DataFrame or Series*
  * Scatter data made by **rawDataReader.NEPH**
* **df_ec** : *DataFrame or Series, default : None*
  * Black Carbon data
* **df_mass** : *DataFrame or Series, default : None*
  * Black Carbon data

---

Mie

---

IMPROVE

### SizeDistr

basic

---

merge_SMPS_APS





