from jbfunctions import jbprep, jbstats, jbsac, jbgp_fit
import pandas as pd
import numpy as np
from numpy.random import RandomState
rng = RandomState()
import pdb
import cProfile
import pstats
from time import time

from ggplot import *

## TEMPLATE FOR TIMING DEBUGGING
# cProfile.run('TEST=fcn(params)', 'fcn_stats')
# p = pstats.Stats('fcn_stats')
# p.sort_stats('tottime')
# p.print_stats()



################################
#  PREPROCESSING DATA
################################

## AWS DB
DB_URL = 'mysql://jsb4:PASSWORD@mydb.c4dh2hic3vxp.us-east-1.rds.amazonaws.com:3306/myexp'
## LOCAL DB (used if dbs recently synced with sync_mysql_aws2local.sh)
# DB_URL = 'mysql://root:PASSWORD@127.0.0.1/myexp'
TABLE_NAME = 'myopic_exp0_e'

FINISHED_STATUSES = [3,4,5,7]
# trials that do not return true for all functions in criterion will not be used
CRITERION = [lambda df: 'round' in df,
             lambda df: df['round'] > 0 and df['round'] <= 200,
             lambda df: df['status'] in FINISHED_STATUSES]

df = jbprep.sql2pandas(DB_URL, TABLE_NAME, CRITERION)

# order properly
SORTORDER = ['condition','counterbalance','workerid', 'round']
df = df.sort(SORTORDER)

# fields saved as lists, but actually only containing scalars
LO1NUMBER2SCALARFIELDS = {'samX', 'samY'}
df = jbprep.lo1number2scalar(df, LO1NUMBER2SCALARFIELDS)

# make fields with lists of numbers numpy arrays
LONUMBERFIELDS = {'d2locsX', 'd2locsY', 'pxObs', 'pyObs'}
df = jbprep.lonumbers2nparray(df, LONUMBERFIELDS)

# convert any improperly converted fields
FIELDTYPES = {'LENSCALE': 'float64',
              'NOISEVAR2': 'float64',
              'RNGSEED': 'float64',
              'SIGVAR': 'float64',
              'condition': 'int64',
              'counterbalance': 'int64',
              'd2locsX': 'O',
              'd2locsY': 'O',
              'pxObs': 'O',
              'pyObs': 'O',
              'drillX': 'float64',
              'drillY': 'float64',
              'psamX': 'float64',
              'psamY': 'float64',
              'samX': 'float64',
              'samY': 'float64',
              'expScore': 'float64',
              'nObs': 'int64',
              'round': 'int64',
              'roundGross': 'float64',
              'roundNet': 'float64',
              'workerid': 'O'}
df = jbprep.enforceFieldTypes(df, FIELDTYPES)

# convert condition to a factor
df.condition = df.condition.astype(str)

# something got goofed and psiTurk save pxObs and pyObs but not xObs and yObs.
# Have to hack a fix here instead
SCREENW = 1028
SCREENH = 784
GROUNDLINEY = SCREENH - SCREENH*0.9
YMIN = -3
YMAX = 3
df['xObs'] = df['pxObs'].apply(lambda row: jbprep.pix2mathX(row, SCREENW))
df['yObs'] = df['pyObs'].apply(lambda row:
        jbprep.pix2mathY(row, SCREENH, GROUNDLINEY, YMIN, YMAX))

# remove extra info
# (1 drops along cols, 0 along rows)
DROPCOLS = ['uniqueid', 'hitid', 'assignmentid', 'pdrillX', 'pdrillY', 'pxObs', 'pyObs']
df = df.drop(DROPCOLS, 1)

