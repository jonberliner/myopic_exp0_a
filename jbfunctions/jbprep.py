import numpy as np
import pdb

def sql2pandas(db_url, table_name, locriterion=None):
    """connects to database at db_url and converts psiturk datatable table_name
       to a pandas df.  Only includes trials that meet all criterion functions
       given in locriterion (default takes all trials)"""
    from sqlalchemy import MetaData, Table, create_engine
    from json import loads
    from pandas import DataFrame, concat

    data_column_name = 'datastring'
    # boilerplace sqlalchemy setup
    engine = create_engine(db_url)
    metadata = MetaData()
    metadata.bind = engine
    table = Table(table_name, metadata, autoload=True)
    # make a query and loop through
    s = table.select()
    tablerows = s.execute()

    # convert sql rows to lodicts, each containing a subject's full experiment
    # fields from orig datatable that you want attached to every trial
    expFields = ['uniqueid', 'assignmentid', 'workerid', 'hitid', 'status']
    expData = []
    for row in tablerows:
        try:
            subExpData = loads(row[data_column_name])
            for field in expFields:
                subExpData[field] = row[field]
            expData.append(subExpData)
        except:
            continue

    # turn from nested list to flat list of trials
    minidicts = []
    for subExpData in expData:
        for trial in subExpData['data']:
            trialdata = trial['trialdata']
            for field in expFields:
                trialdata[field] = subExpData[field]

            # check if trial valid if any criterion were passed
            includeThisTrial = True
            if locriterion:
                includeThisTrial = meetsCriterion(trialdata, locriterion)

            if includeThisTrial:
                minidicts.append(trialdata)

    # convert minidicts into dataframe!
    df = DataFrame(minidicts)
    # get rid of residue from minidfs
    df.reset_index(drop=True, inplace=True)
    return df


def meetsCriterion(obj, locrit):
    """passes an object to a list of criterion check functions and returns true
       if all checks return true"""
    for crit in locrit:
        if not crit(obj):
            return False
    return True


def pix2mathX(x, screenW):
    """converts from game pixels to math used to generate along x-axis"""
    return x / screenW


def pix2mathY(y, screenH, groundLineY, ymin, ymax):
    """converts from game pixels to math used to generate along y-axis"""
    groundline2bottom = screenH - groundLineY
    yrange = np.ptp([ymin, ymax])

    y -= groundLineY
    y /= groundline2bottom
    y *= yrange
    y += ymin

    return y


def lonumbers2nparray(df, lonumberFields, ftype=None):
    for f in lonumberFields:
        df[f] = df[f].apply(lambda l: np.array(l))

    ## TODO: modularized this out.  verify that this is cool
    # if type(ftype) is type:  # expand to hash w same ftype for each field
    #     ftype = {f: ftype for f in lonumberFields}
    # if ftype:  # convert fields if hash is none
    #     df = convertNumpyFields(df, ftype)
    return df


def convertNumpyFields(df, doFieldTypePairs):
    for f, ftype in doFieldTypePairs:
        df[f] = df[f].apply(lambda npa: npa.astype(ftype))
    return df


def lo1number2scalar(df, lo1numberFields, ftype=None):
    """takes fields that are stored as lists, but actually only contain
    a scalar, extracts from lists, leaving only the scalar, also can
    optionally to field type conversion (default no conversion)"""
    for f in lo1numberFields:
        df[f] = df[f].apply(lambda l: np.array(l[0]))
    return df


def enforceFieldTypes(df, fieldTypes):
    """verifies that cols of df that match keys in fieldTypes match the
    matching values in fieldTypes.  Converts them if they don't match"""
    for key, ftype in fieldTypes.iteritems():
        if str(df[key].dtype) is not ftype:
            # TODO: verify that we don't need this explicit None replacement
            # df[key] = df[key].replace('None', np.nan)
            # try:
            df[key] = df[key].astype(ftype)
            # except:
            #     pdb.set_trace()

    return df


    # if type(ftype) is type: ftype0 = ftype # same type conv for every field
    # elif type(ftype) is dict:  # diff type conversaion for each field
    #     assert f in ftype, ('if using doftypes, each field in lonumberFields'
    #                         ' must have corresponding key in ftype')
    #     ftype0 = ftype[f]
    # elif ftype is None: ftype0 = None  # no type conversion
    # else: raise ValueError('ftype must be a type, a dict of types for '
    #                        'each field, or None (for no type conversion)')

    # if ftype0:  # list2scalar with type conversion
    #     df[f] = df[f].apply(lambda l: np.array(l[0]).astype(ftype0))
    # else:  # no type conversion
    #     df[f] = df[f].apply(lambda l: np.array(l[0]))
# return df
