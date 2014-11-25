from pandas import concat, DataFrame
import pdb


def sac(df, fcn, reducefield, groupfields=None, fcnlabel=None):
    """sac(df, fcn, reducefield, groupfields=None, fcnlabel=None) -> df

    split-apply-combine in a sensible manner.  takes a function fcn, and
    applies it to every group in reducefield.  groupfields are the fields
    above it that, although not necessary for the analysis per se, you want
    to keep around for a nice melted, labeled dataframe to return."""
    # TODO: finish docs

    if fcnlabel is None:
        fcnlabel = fcn.__name__
    dfg = df.groupby(groupfields + [reducefield])  # condition here for melt
    # analysis run on every row in reducefield
    reduceddf = dfg.apply(fcn)
    reduceddf = reduceddf.reset_index()  # melt
    reduceddf.rename(columns={0: fcnlabel}, inplace=True)
    return reduceddf


def hsac(df, fcns, reducefields, fcnlabels=None, fieldsHi2Lo=True,
        keepAll=True):
    """"hsac(df, fcns, reducefields, fcnlabels=None, fieldsHi2Lo=True,
             keepAll=True) -> df or do_dfs

    hierarchical sac.  fcn to sac from the lowest grouping to the highest.
    fcns are lofunctions to apply at each level.  reducefields are grouping
    hierarching of column names (e.g. ['condition', 'subject', 'trial'])."""
    # TODO: finish docs

    if keepAll:
        out = {}

    # reverse to make chain go from lo 2 high
    # default is True because makes more sense conceptually
    # (e.g. condition -> subject -> trial is more intuitive than t -> s -> c)
    if fieldsHi2Lo:
        fcn = fcns[::-1]
        reducedfields = reducefields[::-1]
        if fcnlabels: fcnlabels = fcnlabels[::-1]

    # pass analyses up the grouping stack!
    df0 = df
    for findex, f in enumerate(reducefields):
        reducefield = reducefields[findex]
        if f != reducefields[-1]:
            groupfields = reducefields[findex+1:]
        else:
            groupfields = None
        df0 = hsac(df0, fcns[findex], reducefield, groupfields)
        if keepAll:
            out[f] = df0

    if not keepAll:
        out = df0
    return out


def cond_worker_trial(df, trialfcn, workerfcn, conditionfcn,
        condition='condition', workerid='workerid', trial='round',
        trialfcnLabel=None, workerfcnLabel=None, conditionfcnLabel=None):
    if trialfcnLabel is None:
        trialfcnLabel = trialfcn.__name__
    if workerfcnLabel is None:
        workerfcnLabel = workerfcn.__name__
    if conditionfcnLabel is None:
        conditionfcnLabel = conditionfcn.__name__

    dft = df.groupby([condition, workerid, trial])  # condition here for melt
    trialAnalysis = DataFrame(dft.apply(trialfcn))  # analysis run on every trial
    # remove cols that will be melted from indices to cols on reset_index()
    trialAnalysis = dropIndexCols(trialAnalysis)
    trialAnalysis.reset_index(inplace=True)

    # run whatever function you want to run on each subject
    dfw = trialAnalysis.groupby([condition, workerid])
    workerAnalysis = DataFrame(dfw.apply(workerfcn))
    workerAnalysis = dropIndexCols(workerAnalysis)
    workerAnalysis.reset_index(inplace=True)

    # run whatever function you want to run on each condition
    dfc = workerAnalysis.groupby(condition)
    conditionAnalysis = DataFrame(dfw.apply(conditionfcn))
    conditionAnalysis = dropIndexCols(conditionAnalysis)
    conditionAnalysis.reset_index(inplace=True)

    # save renaming this field so we can always access trialAnalysis
    # output under column name 0
    trialAnalysis.rename(columns={0: trialfcnLabel}, inplace=True)
    workerAnalysis.rename(columns={0: workerfcnLabel}, inplace=True)
    conditionAnalysis.rename(columns={0: conditionfcnLabel}, inplace=True)

    return {'trialAnalysis': trialAnalysis,
            'workerAnalysis': workerAnalysis,
            'conditionAnalysis': conditionAnalysis}


def dropIndexCols(df):
    [df.drop(cname, axis=1, inplace=True)
        for cname in df.keys()
        if cname in df.index.names]
    return df
