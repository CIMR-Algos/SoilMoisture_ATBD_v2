
from scipy.optimize import least_squares
import numpy as np
from sklearn.metrics import root_mean_squared_error


def sm_ret(l1x, params, aux, flag, bounds=None, verbose=True):

    def _mironov(f, sm, cf):
        #  Mironov's soil dielectric model
        #  The code is a direct adaptation of Patricia de Rosnay's Fortran
        #  code collected in ECMWF's CMEM v3.0.
        #  Steven Chan, 03/2011; Adapted to Python by M. Link 2023
        #  f = frequency [GHz]
        #  sm = soil moisture [m3/m3]
        #  cf = clay fraction [-]
        eps_0 = 8.854e-12
        eps_winf = 4.9
        fHz = f * 1e9
        # RI & NAC of dry soils
        znd = 1.634 - 0.539 * cf + 0.2748 * cf**2
        zkd = 0.03952 - 0.04038 * cf
        # Maximum bound water fraction
        zxmvt = 0.02863 + 0.30673 * cf
        # Bound water parameters
        zep0b = 79.8 - 85.4 * cf + 32.7 * cf**2
        ztaub = 1.062e-11 + 3.450e-12 * cf
        zsigmab = 0.3112 + 0.467 * cf
        # Unbound (free) water parameters
        zep0u = 100
        ztauu = 8.5e-12
        zsigmau = 0.3631 + 1.217 * cf
        # Computation of epsilon water (bound & unbound)
        zcxb = (zep0b - eps_winf) / (1 + (2*np.pi*fHz*ztaub)**2)
        zepwbx = eps_winf + zcxb
        zepwby = zcxb * (2*np.pi*fHz*ztaub) + zsigmab / (2*np.pi*eps_0*fHz)
        zcxu = (zep0u - eps_winf) / (1 + (2*np.pi*fHz*ztauu)**2)
        zepwux = eps_winf + zcxu
        zepwuy = zcxu * (2*np.pi*fHz*ztauu) + zsigmau / (2*np.pi*eps_0*fHz)
        # Computation of refractive index of water (bound & unbound)
        znb = np.sqrt(np.sqrt(zepwbx**2 + zepwby**2) + zepwbx) / np.sqrt(2)
        zkb = np.sqrt(np.sqrt(zepwbx**2 + zepwby**2) - zepwbx) / np.sqrt(2)
        znu = np.sqrt(np.sqrt(zepwux**2 + zepwuy**2) + zepwux) / np.sqrt(2)
        zku = np.sqrt(np.sqrt(zepwux**2 + zepwuy**2) - zepwux) / np.sqrt(2)
        # Computation of soil refractive index (nm & km): xmv can be a vector
        zxmvt2 = min(sm,zxmvt)
        zflag = np.sum(sm >= zxmvt)
        znm = znd + (znb - 1) * zxmvt2 + (znu - 1) * (sm-zxmvt) * zflag
        zkm = zkd + zkb * zxmvt2 + zku * (sm-zxmvt) * zflag
        # Computation of soil dielectric constant:
        zepmx = znm**2 - zkm**2
        zepmy = znm * zkm * 2
        #eps = complex(zepmx, zepmy)
        e_real = zepmx
        e_im = zepmy
        return e_real

    def _fresnel_roughness(e_real, theta, h, q, n):
        cost = np.cos(np.radians(theta))
        sint = np.sin(np.radians(theta))
        # Fresnel reflectivity
        rv_num = e_real*cost - np.sqrt(e_real - (sint**2))
        rv_den = e_real*cost + np.sqrt(e_real - (sint**2))
        rh_num = cost - np.sqrt(e_real - (sint**2))
        rh_den = cost + np.sqrt(e_real - (sint**2))
        rv = (rv_num / rv_den)**2
        rh = (rh_num / rh_den)**2
        # Roughness correction after Wang & Choudhury, 1981
        coef = np.exp(-h * cost**n)
        rvr = ((1-q)*rv + q*rh) * coef
        rhr = ((1-q)*rh + q*rv) * coef
        return rvr, rhr

    def _tau_omega(r, gamma, omega, t_eff):
        # soil, vegetation, and soil-vegetation-interaction emission
        soil = (1 - r) * gamma * t_eff
        veg = (1 - gamma) * (1 - omega) * t_eff
        veg_soil = veg * r * gamma
        # combine all contributions
        tb = soil + veg + veg_soil
        return tb

    def _forward_model(x):
        # read vegetation opacity and soil moisture
        tau = x[0]
        sm = x[1]
        # calculate transmissivity from nadir vegetation opacity
        gamma = np.exp(-tau * 1. / np.cos(np.radians(theta)))
        # calculate real part of soil dielectric constant
        e_real = _mironov(f, sm, cf)
        # calculate rough surface soil reflectivity
        rv, rh = _fresnel_roughness(e_real, theta, h, q, n)
        # calculate total emission of soil and vegetation (V,  H polarization)
        tbv = _tau_omega(rv, gamma, omega, t_eff)
        tbh = _tau_omega(rh, gamma, omega, t_eff)
        return tbv, tbh

    def _cost_function(x):
        # J_TB
        tbv, tbh = _forward_model(x)
        j_tbv = (tbv - ytar[0])**2 / tb_std**2
        j_tbh = (tbh - ytar[1])**2 / tb_std**2
        # J_tau
        tau_std = np.min([0.1 + 0.3*x[0], 0.3])
        j_tau = (x[0] - tau_ini)**2 / tau_std**2
        # total
        j_total = j_tbh + j_tbv + j_tau
        return j_total

    # Look for L-band data in "L1X" file
    if 'L' in l1x:
        band = 'L'
    elif 'L_E' in l1x:
        band = 'L_E'
    else:
        raise ValueError('bands must be one of L or L_E')

    # extract tbv and tbh from l1x
    l1x_tbv = l1x[band]['brightness_temperature_v']
    l1x_tbh = l1x[band]['brightness_temperature_h']

    # extract grid information and respective AOI
    if l1x[band]['_grid'] == 'Global Equal Area grid (36.0 km)':
        aoi = np.array([82, 120, 463, 501])
    elif l1x[band]['_grid'] == 'Global Equal Area grid (9.0 km)':
        aoi = np.array([82, 120, 463, 501]) * 4
    else:
        raise ValueError('Grid Definition not known')

    # check dimensions of tbv and tbh
    if np.shape(l1x_tbv) != np.shape(l1x_tbh):
        raise Exception('TBV and TBH size not equal')
    else:
        shape = l1x_tbv.shape

    # initialize output arrays with fill values
    ret_sm = np.ones(shape, dtype='f8') * -999
    ret_vod = np.ones(shape, dtype='f8') * -999
    rmse_tb = np.ones(shape, dtype='f8') * -999
    flag_surf = np.ones(shape, dtype='int16') * -999
    flag_ret = np.ones(shape, dtype='int16') * -999

    # initialize parameters
    sm_ini = params['sm_ini']
    theta = params['theta']
    tb_std = params['TB_std']
    f = params['f']
    q = params['Q']
    n = params['n']

    # Loop over each pixel of AOI
    if verbose:
        print('Soil Moisture Retrieval: ' + l1x[band]['_grid'])
    for i in range(aoi[0], aoi[1]):
        for j in range(aoi[2], aoi[3]):

            # indices of aux data
            i_aux = i - aoi[0]
            j_aux = j - aoi[2]

            # Water fraction critical level (no retrieval attempted)
            if flag['Water Fraction'][i_aux, j_aux] > params['wf_th']:
                flag_ret[i, j] = 1

            elif flag['Water Fraction'][i_aux, j_aux] <= params['wf_th']:

                # initialize flag arrays to zero (retrieval attempted)
                flag_surf[i, j] = 0
                flag_ret[i, j] = 0

                # Water fraction [-]
                if flag['Water Fraction'][i_aux, j_aux] >= 0.05:
                    flag_surf[i, j] = flag_surf[i, j] + 2**0

                # Distance to Coast [km]
                if flag['Coast Distance'][i_aux, j_aux] < 36:
                    flag_surf[i, j] = flag_surf[i, j] + 2**1

                # Vegetation Cover [kg/m²]
                if flag['VWC'][i_aux, j_aux] > 5:
                    flag_surf[i, j] = flag_surf[i, j] + 2**2

                # Urban Fraction [-]
                if flag['Urban Fraction'][i_aux, j_aux] > 0.25:
                    flag_surf[i, j] = flag_surf[i, j] + 2**3

                # Precip Rate [mm/h]
                if flag['Precip Rate'][i_aux, j_aux] > 1:
                    flag_surf[i, j] = flag_surf[i, j] + 2**4

                # Frozen Fraction [-]
                if flag['Frozen Fraction'][i_aux, j_aux] > 0.05:
                    flag_surf[i, j] = flag_surf[i, j] + 2**5

                # Snow Fraction [-]
                if flag['Snow Fraction'][i_aux, j_aux] > 0.05:
                    flag_surf[i, j] = flag_surf[i, j] + 2**6

                # DEM Standard Deviation [degree]
                if flag['DEM STD'][i_aux, j_aux] > 3:
                    flag_surf[i, j] = flag_surf[i, j] + 2**7

                # extract TBs and parameters
                tbv = l1x_tbv[i, j]
                tbh = l1x_tbh[i, j]
                omega = aux['omega'][i_aux, j_aux]
                h = aux['h'][i_aux, j_aux]
                cf = aux['cf'][i_aux, j_aux]
                t_eff = aux['LST'][i_aux, j_aux]
                tau_ini = aux['tau_ini'][i_aux, j_aux]

                # initial and target values
                x0 = np.array([tau_ini, sm_ini])
                ytar = np.concatenate(([tbv], [tbh]))

                # SM retrieval
                if bounds == None:
                    sol = least_squares(_cost_function, x0, method='trf',
                                        jac='3-point', ftol=1e-4, xtol=1e-4, 
                                        max_nfev=1000)                
                else:
                    sol = least_squares(_cost_function, x0, method='trf',
                                        jac='3-point', bounds=bounds,
                                        ftol=1e-4, xtol=1e-4, max_nfev=1000)
                
                # extract sm and vod from solution
                ret_sm[i, j] = sol.x[1]
                ret_vod[i, j] = sol.x[0]

                # retrieval flag if not successful
                if sol.success == False:
                    flag_ret[i, j] = 2

                # calculate rmse of TBV,TBH and optimal solution
                yopt = np.array(_forward_model(sol.x))
                rmse_tb[i, j] = root_mean_squared_error(ytar, yopt)

        # define output dictionary
        output = {}
        output['sm'] = ret_sm
        output['vod'] = ret_vod
        output['flag_surf'] = flag_surf
        output['flag_ret'] = flag_ret
        output['rmse_tb'] = rmse_tb
        output['_grid'] = l1x[band]['_grid']

    return output
