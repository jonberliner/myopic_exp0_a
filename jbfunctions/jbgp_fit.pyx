from jbfunctions.jbgp import K_se, conditioned_mu, conditioned_covmat, sample
from numpy import abs, linspace, unique, zeros, array
from matplotlib import pyplot as plt
from numpy cimport ndarray
from pandas import Series, DataFrame


def plot_posterior(posterior, X=linspace(0, 1, 1028)):
    mu = posterior['mu']
    sd = posterior['covmat'].diagonal()
    f = plt.figure()
    plt.plot(X, mu, 'red')
    plt.fill_between(X, mu-sd*1.96, mu+sd*1.96, color='red', alpha=0.3)
    plt.show()
    return f


cpdef ndarray[double, ndim=1] exploit(ndarray[double, ndim=1] mu,
                                      ndarray[double, ndim=1] X):
    # TODO: add in uncertaintly
    cdef int imax = mu.argmax()
    cdef double yhat = mu.max()
    return array([X[imax], yhat])


cpdef ndarray[double, ndim=1] get_trialError(ndarray[double, ndim=1] xObs,
                                             ndarray[double, ndim=1] yObs,
                                             float drillX,
                                             float drillY,
                                             ndarray[double, ndim=1] X,
                                             ndarray[double, ndim=2] KX,
                                             float lenscale):

    # condition on obs
    cdef double SIGVAR=1.
    cdef double NOISEVAR2 = 1e-7

    posterior_mu = conditioned_mu(X, xObs, yObs, lenscale, SIGVAR, NOISEVAR2)
    posterior_covmat = conditioned_covmat(X, KX, xObs, lenscale, SIGVAR, NOISEVAR2)

    # get point with lowest expected value
    cdef ndarray[double, ndim=1] hat = exploit(posterior_mu, X)

    # get error
    # TODO: abstract out error fcn?
    #  maybe introduct something with yerr?
    xerr = abs(hat[0] - drillX)
    yerr = abs(hat[1] - drillY)

    return array([xerr, yerr, hat[0], hat[1]])


cpdef ndarray[double, ndim=2] get_experimentError(df, lenscale, X):
    cdef double SIGVAR = 1.
    cdef ndarray[double, ndim=2] KX = K_se(X, X, lenscale, SIGVAR)
    rounds = unique(df.round)
    # cdef ndarray[int, ndim=1] rounds = unique(df.round)
    cdef ndarray[double, ndim=2] trialError = zeros([len(rounds), 4])
    cdef int r
    for r in rounds:
        dfr = df[df.round==r]
        trialError[r-1] = get_trialError(dfr.xObs.iat[0],
                                         dfr.yObs.iat[0],
                                         dfr.drillX.iat[0],
                                         dfr.drillY.iat[0],
                                         X,
                                         KX,
                                         lenscale)

    return trialError


def fit_lenscale(df):
    # FIXME: this is just for testing.  need lenscale to be optimized
    LENSCALEPOWSOF2 = [2., 4., 6.]
    LENSCALEPOOL = [1./2.**n for n in LENSCALEPOWSOF2]

    X = linspace(0, 1, 1028)
    trialErrors = [get_experimentError(df, lenscale, X)
                   for lenscale in LENSCALEPOOL]
    # trialErrors = DataFrame([{lenscale: get_experimentError(df, lenscale)
    #                          for lenscale in LENSCALEPOOL}])
    return trialErrors


