from jbfunctions import jbload
from jbfunctions import jbstats
from jbfunctions import jbsac
from pandas import concat
from matplotlib import pyplot as plt

#TODO: for now, will just bind to r for plotting
# hoping one day can do this all in python
# if using ipython, this will be the r binding
from rpy2.robjects.packages import importr
base = importr('base')
import rpy2.robjects as ro
import rpy2.robjects.lib.ggplot2 as gg
import pandas.rpy.common as com

# # needed to use %R magic in ipython
# %load_ext rpy2.ipython
# # closes a plot plotted through R
# %R dev.off()


NROUND = 200

## LOCAL DB (used if dbs recently synced with sync_mysql_aws2local.sh)
# DB_URL = 'mysql://root:PASSWORD@127.0.0.1/myexp'
## AWS DB
DB_URL = 'mysql://jsb4:PASSWORD@mydb.c4dh2hic3vxp.us-east-1.rds.amazonaws.com:3306/myexp'

FINISHED_STATUSES = [3,4,5,7]   # psiturk markers for a completed experiment
# trials that do not return true for all functions in criterion will not be used
CRITERION = [lambda df: 'round' in df,  # gets rid of non-my-exp trials (e.g. psiturk gunk)
            lambda df: df['round'] > 0 and df['round'] <= 200,  # same as above
            lambda df: df['status'] in FINISHED_STATUSES]  # taking complete exps only

# get experiments data
dfm = jbload.myopic_exp0(DB_URL, CRITERION)  #load myopic experiment
dfn = jbload.noChoice_exp0(DB_URL, CRITERION)  #load noChoice experiment
#TODO: move rngseed conversion to jbload
dfm['rngseed'] = dfm['rngseed'].astype(str)
dfn['rngseed'] = dfn['rngseed'].astype(str)
df = concat([dfm, dfn])  # combine both experiments into same df
df.reset_index(inplace=True, drop=True)

# verify that our yolking worked out correctly
for r in range(NROUND):
    rdf = df[df.round==r]  # get this round
    # get number of samples in this round for everyone in this yolk set
    tmp = rdf.groupby('rngseed').apply(lambda df0: df0.nObs.unique())
    # assert everyone in this counterbalance had same stream of number of obs
    for rr in tmp:
        assert(len(rr)==1)

# get average distance between myopic and noChoice
m_mu_sam2obs = jbsac.sac(dfm, lambda df0:
        jbstats.dBetween(df0, 'samX', 'obsX'),
        'workerid', ['condition', 'experiment', 'rngseed'], 'mu_d')

n_mu_drill2obs = jbsac.sac(dfn, lambda df0:
        jbstats.dBetween(df0, 'drillX', 'obsX'), 'workerid',
        ['condition', 'experiment', 'rngseed'], 'mu_d')

d2obs = concat([m_mu_sam2obs, n_mu_drill2obs])
d2obs.reset_index(drop=True, inplace=True)
r_d2obs = com.convert_to_r_dataframe(d2obs, strings_as_factors=True)

# plotting with R's ggplot2
pp = gg.ggplot(r_d2obs) +\
        gg.aes_string(x='experiment', y='mu_d', col='condition') +\
        gg.geom_boxplot()

m_mu_sam2obs = jbstats.dBetween_analysis(dfm, 'samX', 'obsX')['worker_mu_d']
n_mu_drill2obs = jbstats.dBetween_analysis(dfn, 'drillX', 'obsX')['worker_mu_d']
worker_mu_d2obs = concat([m_mu_sam2obs, n_mu_drill2obs])


msamx = dfm.samX
msamy = dfm.samY
# get noChoice exploit
ndrillx = dfn.drillX
ndrilly = dfn.drillY
