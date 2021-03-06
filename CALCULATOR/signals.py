"""
@author: 
"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from scipy.signal import freqz
#
def Ftrans(datos , ndats , dt , fs):
    """
     Computes the Fourier spectra of datos[] and
     returns the result in SaS after smoothing by the
     smootinh factor fs.
    """
    nfr=int(ndats/2)
    df=1.0/(ndats*dt)
    x=np.zeros([nfr-1], dtype=float)
    x=np.arange(df,nfr*df,df)
    A   = np.zeros([ndats],dtype=float)
    Aa  = np.zeros([ndats],dtype=float) 
    A=np.fft.fft(datos)
    Aa=np.abs(A)
    """
    Smooth the spectrum.
    """
    Sa = Aa[1:nfr]
    Samag = smooth(Sa , x , fs)
    nfs = nfr-1
#
    return x, Samag , A , nfs
#
def IFtrans(datos , ndats , dt):
#
# Intgrates an acceleration history into a velocity history
# proceeding in the frequency domain.
#
	B=np.fft.ifft(datos)
#
	return np.real(B) 
#    
#
def smooth(Sa, Freq , fftfs):
#
    #  **** Input :
    #  Sa: Original spectrum
    #  Freq: Frequency
    #  fftfs: Smoothing factor
#
    Sas  = np.zeros([len(Sa)],dtype=float)
    fia = 1
    fma = 1
    suma = Sa[0] * Sa[0]
    pot = 1./2./fftfs
    fsexpi = 2**(-pot)
    fsexpm = 2**( pot)
    Sas[0] = Sa[0]
    NNfft = len(Sa)
    for i in range(1,NNfft):
    # #    for i=2:NNfft
        fi = int((i + 1) * fsexpi)
        fm = int((i + 1) * fsexpm)
        if fi < 1:
            fi = 1
        if fm > NNfft:
            fm = NNfft

        for Num in range(fia - 1, fi - 1):
        #         #for j=fia:fi-1:
            suma = suma - Sa[Num] * Sa[Num]

        for Num in range(fma, fm):
        #         #for j=fma+1:fm:
            suma = suma + Sa[Num]*Sa[Num]

        Nf = fm - fi + 1
        fia = fi
        fma = fm
        Sas[i]=np.sqrt(suma/Nf)
#
    return (Sas)
#
def ricker(nt, Tt, tc, fc):
	
     Rick=np.zeros(nt)
     T=np.zeros(nt)
     dt=Tt/(nt-1)
	
     for i in range(nt):
         tao=np.pi*fc*(dt*i-tc)
         Rick[i]=(2.*tao**2-1.)*np.exp(-tao**2)    
         T[i]= i*dt
	
     return (Rick, T)
#