#!/usr/bin/env python3
"""Create a short, synthetic, strictly non-vocal outdoor wind/cloth ambience bed."""
import wave
import numpy as np
from pathlib import Path
SR=48000
DURATION=12.25
N=int(SR*DURATION)
rng=np.random.default_rng(2026101306)
freq=np.fft.rfftfreq(N,1/SR)

def shaped_noise(low, high, slope=0.5):
    x=rng.normal(0,1,N)
    spec=np.fft.rfft(x)
    f=np.maximum(freq,1.0)
    weight=1/(f**slope)
    if low:
        weight*=1-np.exp(-(freq/max(low,1))**4)
    if high:
        weight*=np.exp(-(freq/high)**4)
    y=np.fft.irfft(spec*weight,n=N)
    y/=max(np.sqrt(np.mean(y*y)),1e-12)
    return y

t=np.arange(N)/SR
wind=shaped_noise(28,520,0.62)
envelope=0.56+0.18*np.sin(2*np.pi*0.12*t+0.4)+0.10*np.sin(2*np.pi*0.29*t+1.2)
wind=wind*envelope*0.018
rustle=shaped_noise(450,5200,0.18)
# Two quiet, soft fabric/foliage swishes; smooth envelopes avoid clicks.
def bump(center,width): return np.exp(-0.5*((t-center)/width)**2)
rustle_env=0.13*bump(3.6,0.42)+0.10*bump(8.6,0.55)+0.05*bump(10.8,0.35)
rustle=rustle*rustle_env*0.006
mono=wind+rustle
fade=np.minimum(np.minimum(t/0.35,(DURATION-t)/0.8),1.0).clip(0,1)
mono*=fade
# Slight stereo width from decorrelated air noise, kept very subtle.
side=shaped_noise(120,1400,0.45)*0.002*envelope*fade
left=mono+side
right=mono-side
stereo=np.stack([left,right],axis=1)
stereo=np.clip(stereo,-0.12,0.12)
pcm=(stereo*32767).astype('<i2')
out=Path(__file__).with_name('环境音_风声与轻微衣料摩擦.wav')
with wave.open(str(out),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
print(out, 'seconds=',N/SR,'rms=',float(np.sqrt(np.mean(stereo**2))),'peak=',float(np.max(np.abs(stereo))))
