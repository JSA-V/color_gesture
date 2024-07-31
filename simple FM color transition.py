import numpy as np
from scipy.special import jv as J
from numpy import sign, dot
import colour
from colour.plotting import *
from Sound_Colors import w_,nonlin,cmfs

# operator frequencies 
f_base = 440
Qvec=[1,2]

# N is the list of subindices that we use from the color series
p=50
N=range(-p,p+1)

def RGBnl(f,Q,I):
    """from a simple FM wave with carrier frequency f,
    modulator frequency Q[1]*f,
    and modulation index I to standard RGB"""
    # dictionary assigning to frequency ratios
    # their amplitudes
    D={}
    for n in N:
        # turn all frequency signs positive 
        key=Q[0]+n*Q[1]
        s=sign(key)
        # sum all amplitudes for the same frequency 
        if s*key in D:
            D[s*key]+=s*J(n,I)
        else:
            D[s*key]=s*J(n,I)
   
    freq=f*np.array(list(D.keys()))
    a=np.abs(list(D.values()))
    XYZ=colour.wavelength_to_XYZ(w_(freq), cmfs)
    # the color series
    color=dot(a,XYZ)        
    RGB=colour.XYZ_to_sRGB(color)
    RGBnonl=nonlin(color)
    return RGBnonl

import time
start=time.time()
shade=[RGBnl(f_base,Qvec,i/10) for i in range(201)] # final transition, 20 seconds
print('Runtime: {} seconds'.format(time.time()-start))

plot_multi_colour_swatches(shade,columns=10) # transition rendering

