import jbprep
import pdb

def myopic_exp0(db_url, criterion):
    df = jbprep.sql2pandas(db_url, 'myopic_exp0', criterion)
    df['experiment'] = 'myopic_exp0'

    # order properly
    SORTORDER = ['condition','counterbalance','workerid', 'round']
    df = df.sort(SORTORDER)

    # fields saved as lists, but actually only containing scalars
    LO1NUMBER2SCALARFIELDS = {'samX', 'samY'}
    df = jbprep.lo1number2scalar(df, LO1NUMBER2SCALARFIELDS)

    # make fields with lists of numbers numpy arrays
    LONUMBERFIELDS = {'d2locsX', 'd2locsY', 'pxObs', 'pyObs'}
    df = jbprep.lonumbers2nparray(df, LONUMBERFIELDS)

    # rename columns
    OLDNEWCOLNAMES = {'xObs': 'obsX',
                    'yObs': 'obsY',
                    'pxObs': 'pobsX',
                    'pyObs': 'pobsY',
                    'LENSCALE': 'lenscale',
                    'NOISEVAR2': 'noisevar2',
                    'RNGSEED': 'rngseed',
                    'SIGVAR': 'sigvar'}
    df.rename(columns=OLDNEWCOLNAMES, inplace=True)

    # convert any improperly converted fields
    FIELDTYPES = {'lenscale': 'float64',
                'noisevar2': 'float64',
                'rngseed': 'int64',
                'sigvar': 'float64',
                'condition': 'int64',
                'counterbalance': 'int64',
                'd2locsX': 'O',
                'd2locsY': 'O',
                'pobsX': 'O',
                'pobsY': 'O',
                'obsX': 'O',
                'obsY': 'O',
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
    df['obsX'] = df['pobsX'].apply(lambda row: jbprep.pix2mathX(row, SCREENW))
    df['obsY'] = df['pobsY'].apply(lambda row:
            jbprep.pix2mathY(row, SCREENH, GROUNDLINEY, YMIN, YMAX))

    # remove extra info
    # (1 drops along cols, 0 along rows)
    DROPCOLS = ['uniqueid', 'hitid', 'assignmentid', 'pdrillX', 'pdrillY',
                'pobsX', 'pobsY', 'psamX', 'psamY']
    df = df.drop(DROPCOLS, 1)

    return df


def noChoice_exp0(db_url, criterion):
    ################################
    #  PREPROCESSING DATA
    ################################
    ## AWS DB
    # DB_URL = 'mysql://jsb4:PASSWORD@mydb.c4dh2hic3vxp.us-east-1.rds.amazonaws.com:3306/myexp'
    # ## LOCAL DB (used if dbs recently synced with sync_mysql_aws2local.sh)
    # # DB_URL = 'mysql://root:PASSWORD@127.0.0.1/myexp'
    # TABLE_NAME = 'noChoice_exp0'

    # FINISHED_STATUSES = [3,4,5,7]
    # # trials that do not return true for all functions in criterion will not be used
    # CRITERION = [lambda df: 'round' in df,
    #             lambda df: df['round'] > 0 and df['round'] <= 200,
    #             lambda df: df['status'] in FINISHED_STATUSES]

    df = jbprep.sql2pandas(db_url, 'noChoice_exp0', criterion)
    df['experiment'] = 'noChoice_exp0'

    # order properly
    SORTORDER = ['condition','counterbalance','workerid', 'round']
    df = df.sort(SORTORDER)

    # make fields with lists of numbers numpy arrays
    LONUMBERFIELDS = {'d2locsX', 'd2locsY', 'pxObs', 'pyObs'}
    df = jbprep.lonumbers2nparray(df, LONUMBERFIELDS)

    # rename columns
    OLDNEWCOLNAMES = {'xObs': 'obsX',
                    'yObs': 'obsY',
                    'pxObs': 'pobsX',
                    'pyObs': 'pobsY',
                    'LENSCALE': 'lenscale',
                    'NOISEVAR2': 'noisevar2',
                    'RNGSEED': 'rngseed',
                    'SIGVAR': 'sigvar'}
    df.rename(columns=OLDNEWCOLNAMES, inplace=True)



    # convert condition to a factor
    df.condition = df.condition.astype(str)

    # something got goofed and psiTurk save pxObs and pyObs but not xObs and yObs.
    # Have to hack a fix here instead
    SCREENW = 1028
    SCREENH = 784
    GROUNDLINEY = SCREENH - SCREENH*0.9
    YMIN = -3
    YMAX = 3
    df['obsX'] = df['pobsX'].apply(lambda row: jbprep.pix2mathX(row, SCREENW))
    df['obsY'] = df['pobsY'].apply(lambda row:
            jbprep.pix2mathY(row, SCREENH, GROUNDLINEY, YMIN, YMAX))

    # convert any improperly converted fields
    FIELDTYPES = {'lenscale': 'float64',
                'noisevar2': 'float64',
                'rngseed': 'int64',
                'sigvar': 'float64',
                'condition': 'int64',
                'counterbalance': 'int64',
                'd2locsX': 'O',
                'd2locsY': 'O',
                'pobsX': 'O',
                'pobsY': 'O',
                'obsX': 'O',
                'obsY': 'O',
                'drillX': 'float64',
                'drillY': 'float64',
                'expScore': 'float64',
                'nObs': 'int64',
                'round': 'int64',
                'roundGross': 'float64',
                'roundNet': 'float64',
                'workerid': 'O'}
    df = jbprep.enforceFieldTypes(df, FIELDTYPES)

    # remove extra info
    # (1 drops along cols, 0 along rows)
    DROPCOLS = ['uniqueid', 'hitid', 'assignmentid', 'pdrillX', 'pdrillY',
                'pobsX', 'pobsY']
    df = df.drop(DROPCOLS, 1)

    return df
