# The color of a sound spectrum 

from numpy import log2, floor, dot
import colour
from colour.plotting import *

f1=440 # base frequency for octave reduction to [f1,2f1]

# octave reduction
def integer(freq): # ¡Warning: does not admit 0 frequencies!
    return floor(log2(freq/f1))

def redu(freq):
    return freq/(2**integer(freq))

# from wavelength to frequency
def f_(w):
    return 760*f1/w

# from frequency to wavelength
def w_(freq):
    return f_(redu(freq))    

# CIE color matching functions
cmfs = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']

# conversion from linear RGB to standard RGB 
# (electro-optical transfer function)
def mininon(c): 
    if c<=0.0031308:
        out=c*12.92
    elif c>0.0031308:
        out=1.055*(c)**(1/2.4)-0.055
    return out

def nonlin(RGB):
    return [mininon(c) for c in RGB]
                    
# Color from sound spectrum
def Color(f,a):
    XYZ=colour.wavelength_to_XYZ(w_(f), cmfs) # CIE coordinates
    color=dot(a,XYZ)
    RGB=colour.XYZ_to_sRGB(color)  # CIE to linear RGB conversion
    RGBnl=nonlin(color)  # RGB to usual (non linear) RGB
    plot_single_colour_swatch(RGBnl)
    