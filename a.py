import streamlit as st
import streamlit_vertical_slider  as svs
import scipy.fft as fourier
from scipy.io.wavfile import write
import numpy as np
import librosa 
import math
import matplotlib.pyplot as plt 
import soundfile
import pygame

speech,sampleRate1=librosa.load('Zeebo likes Zebra.wav')
letter,sr=librosa.load('Z.wav')
x=letter[1]
for i in speech[len(letter):]:
   letter= np.append(letter,0)


fourierValue_speech=np.fft.rfft(speech)
#st.write(fourierValue_speech)
frequency_speech=np.fft.rfftfreq(len(speech),1/(sampleRate1))

fourierValue_letter=np.fft.rfft(letter)
frequency_letter=np.fft.rfftfreq(len(letter),1/(sampleRate1))
#st.write(max(fourierValue_letter))
#maxfrequency=max(fourierValue_letter)
#st.write(maxfrequency)
#x= np.argmax(fourierValue_letter)
# st.write(maxfrequency)
# st.write(x)
#for i in range (x-50,x+50,1):
#   frequency_speech[i]=frequency_speech[i]*2

fourierValue_speech-=fourierValue_letter*2


result=np.fft.irfft(fourierValue_speech)

fourierValue_letter=np.fft.irfft(letter)


# counter=0

# for i in fourierValue_speech:
#     if fourierValue_speech[counter]>0:
#         fourierValue_speech[counter]*=2
#     counter+=1

soundfile.write('Result.wav', result,sampleRate1, subtype='PCM_24')
st.audio('Z.wav')
st.audio('Zebra.wav')
st.audio('Result.wav')

fig=plt.figure()
plt.plot(abs(letter))
plt.plot (abs(speech))
plt.show()
st.plotly_chart(fig)

# print(fourierValue_letter)
