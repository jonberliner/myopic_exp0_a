import pdb
from ggplot import *
# log-log plot
def loglog(df, xfield, yfield, labs=None,\
           base=2, size=80, alpha=0.3, position='jitter'):
    ggp = ggplot(aes(x=xfield, y=yfield), data=df)
    ggp += geom_point(position='jitter', size=size, alpha=alpha) +\
        scale_color_gradient() +\
        scale_x_log(base=base) +\
        scale_y_log(base=base)
    if labs:
        for f in labs:
            if f is 'x':
                ggp += labs(x=labs[f])
            if f is 'y':
                ggp += labs(y=labs[f])
            if f is 'title':
                ggp += labs(title=labs[f])
    return ggp

# # density plot
# ggp = ggplot(aes(x='fit', fill='factor(act)'), data=lsfitdf)
# ggp +\
#     geom_density(alpha=0.7) +\
#     geom_vline(xintercept=[0.015625, 0.0625, 0.25], linetype='dashed') +\
#     scale_x_log(base=2) +\
#     labs(x='fit lengthscale',
#          y='density',
#          title='Subject Lengthscale Fits')

