from jbfunctions import jbprep, jbstats, jbsac, jbgp_fit
import pandas as pd
import numpy as np
from numpy.random import RandomState
rng = RandomState()
import ipdb as pdb
import cProfile
import pstats
from time import time

from ggplot import *

## TEMPLATE FOR TIMING DEBUGGING
# cProfile.run('TEST=fcn(params)', 'fcn_stats')
# p = pstats.Stats('fcn_stats')
# p.sort_stats('tottime')
# p.print_stats()

# RELOAD AND REPREP DATA
RELOAD = True
if RELOAD:
    execfile("loadData.py")


################################
#  ANALYSIS
################################
mu_worker_drill2obs = jbsac.get_mu_worker(df, jbstats.drill2obs, 'mu_drill2obs')

mu_dfwc = mu_worker_drill2obs.groupby('condition')
mu_dfwc.describe()

# smaller df to speed up costly lenscale analysis
keeps = ['xObs', 'yObs', 'drillX', 'drillY', 'round', 'workerid', 'LENSCALE']
dfsmall = df[keeps]
# # for testing
# ids = np.unique(df.workerid)
# workerid0 = ids[4:6]
# df0 = dfsmall[np.in1d(df.workerid, workerid0)]

## lenscale fitting with grid search
# LENMIN = -10
# LENMAX = -1
# NLEN = 100

# LENSCALEPOOL = np.logspace(LENMIN, LENMAX, NLEN, base=2)
# lsfitdf = jbstats.fit_lenscale_analysis(dfsmall, LENSCALEPOOL)

## _opt uses scipy.optimize.minimize_scalar instead of a grid search
lsfitdf = jbstats.fit_lenscale_analysis_opt(dfsmall)
lsfitdf['actual_lenscale'] = lsfitdf['actual_lenscale'].astype('float')
# BELOW NOW REPLACED WITH jbstats.fit_lenscale_analysis
# def fit_lenscale(df, lenscalepool):
#     print 'workerid: ' + df.workerid.iat[0]
#     X = np.linspace(0, 1, 1028)
#     trialFits = [jbgp_fit.get_experimentError(df, lenscale, X)
#                    for lenscale in lenscalepool]
#     trialFits = np.asarray(trialFits)
#     xerr = trialFits[:,:,0]
#     mu_xerr_byLenscale = xerr.mean(axis=1)
#     iBestLen = mu_xerr_byLenscale.argmin()
#     fit_lenscale = lenscalepool[iBestLen]
#     return fit_lenscale
# dfw = dfsmall.groupby('workerid')
# # WARNING!: THIS PART TAKES ABOUT 15-45 MINUTES!!
# # fit lenscales using gridsearch
# lenscaleFits = dfw.apply(lambda df0: fit_lenscale(df0, LENSCALEPOOL))
# # get experiment lengethscales
# exp_lenscales = dfw.apply(lambda df0: df0.LENSCALE.iat[0])
# # merge fit and actual lengthscales into single df
# lsfitdf = pd.concat([exp_lenscales, lenscaleFits], axis=1)\
#                     .rename(columns={0:'exp_lenscale', 1:'fit_lenscale'})\
#                     .reset_index()

# LENSCALE FITS PLOTS
# log-log plot
ggp = ggplot(aes(x='act', y='fit'), data=lsfitdf)
# ggp = ggplot(aes(x='actual_lengthscale', y='fit_lengthscale'), data=lsfitdf)
ggp + geom_point(position='jitter', size=80, alpha=0.3) +\
      scale_color_gradient() +\
      scale_x_log(base=2) +\
      scale_y_log(base=2) +\
      labs(x='experiment lengthscale',
           y='fit lengthscale',
           title='Lengthscale Fits')

# density plot
ggp = ggplot(aes(x='fit', fill='factor(act)'), data=lsfitdf)
ggp +\
    geom_density(alpha=0.7) +\
    geom_vline(xintercept=[0.015625, 0.0625, 0.25], linetype='dashed') +\
    scale_x_log(base=2) +\
    labs(x='fit lengthscale',
         y='density',
         title='Subject Lengthscale Fits')

## ANALYSES ONLY ON TRIALS WITH 2 OBS
df2obs = df.groupby('workerid').apply(lambda df0: df0[df0.d2locsX.notnull()])\
                               .reset_index(drop=True)

drill2obs_2sam = jbstats.drill2obs_analysis(df2obs)
# log-log plot
ggp = ggplot(aes(x='act', y='fit'), data=drill2obs_2sam['cond_mu_drill2obs'])
# ggp = ggplot(aes(x='actual_lengthscale', y='fit_lengthscale'), data=lsfitdf)
ggp + geom_point(position='jitter', size=80, alpha=0.3) +\
      scale_color_gradient() +\
      scale_x_log(base=2) +\
      scale_y_log(base=2) +\
      labs(x='experiment lengthscale',
           y='fit lengthscale',
           title='Lengthscale Fits')

# density plot
ggp = ggplot(aes(x='fit', fill='factor(act)'), data=lsfitdf)
ggp +\
    geom_density(alpha=0.7) +\
    geom_vline(xintercept=[0.015625, 0.0625, 0.25], linetype='dashed') +\
    scale_x_log(base=2) +\
    labs(x='fit lengthscale',
         y='density',
         title='Subject Lengthscale Fits')

## ANALYSES ONLY ON TRIALS WITH 2 OBS
df2obs = df.groupby('workerid').apply(lambda df0: df0[df0.d2locsX.notnull()])\
                               .reset_index(drop=True)
# THE FOLLOWING WAS MOVED TO jbstats.drill2obs_analysis
# # define analysis we're gonna use on every subject
# def d2drill(df0):
#     return df0.apply(lambda df00: (np.abs(df00.d2locsX - df00.drillX)).mean(), axis=1)
# # get avg dist for every trial for every sub
# mutrial_d2obs = df2obs.groupby('workerid').apply(d2drill).reset_index()
# # get each sub's experiment avg
# mu_d2obs = mutrial_d2obs.groupby('workerid').mean().reset_index()
# # flatten and label grouped df
# mu_d2obs = mu_d2obs.drop('level_1', axis=1).rename(columns={0: 'mu_d2obs'})
# # get and merge subject conditions (lengthscales)
# exp_lenscale = df.groupby('workerid').apply(lambda df0: df0.LENSCALE.iat[0])
# exp_lenscale = pd.DataFrame(exp_lenscale).reset_index()\
#                  .rename(columns={0: 'exp_lenscale'})
# mu_d2obs = mu_d2obs.merge(exp_lenscale, on='workerid')
# # get condition averages
# cond_mu_d2obs = mu_d2obs.groupby('exp_lenscale').mean()
