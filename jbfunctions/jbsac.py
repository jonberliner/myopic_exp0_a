from pandas import concat

def get_mu_worker(df, fcn, label=None):
    """will take a dataframe, split it by worker, run fcn over each worker,
       label the returned series, attatch condition to series, return a df"""
    dfw = df.groupby('workerid')
    mu_worker = dfw.apply(fcn)
    mu_worker.name = label
    condition = dfw.apply(lambda df0: df0.condition.iat[0])
    condition.name = 'condition'
    return concat([condition, mu_worker], axis=1)


def get_mu_trial(df, fcn, label=None):
    dft = df.groupby('round')
    trial_out = dft.apply(fcn)
    trial_out.name = label
    workerid = dft.apply(lambda df0: df0.workerid.iat[0])
    workerid.name = 'workerid'
    return concat([condition, mu_worker], axis=1)
