import streamlit as st
import streamlit_vertical_slider  as svs
import scipy.fft as fourier
from scipy.io.wavfile import write
import numpy as np
import librosa 
import math
import matplotlib.pyplot as plt 
import soundfile

#range of frequency domain of letters is (0-4000hz)
st.set_page_config(page_title="Equalizer", page_icon=":headphones:",layout="wide")

if 'audio_file' not in st.session_state:
    st.session_state['audio_file'] = 0    

if 'uploadedFile' not in st.session_state:
    st.session_state['uploadedFile']=None

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)




button_style = """
        <style>
        .stButton > button {
            width: 90px;
            height: 35px;
        }
        </style>
        """
st.markdown(button_style, unsafe_allow_html=True)



def fourier_transform(x,sampleRate):

    fourierValue=np.fft.rfft(x)
    frequency=np.fft.rfftfreq(len(x),1/(sampleRate))
    print('values')
    print(len(frequency))
    print(len(fourierValue))
    print(len(x))
    print('max Frequency is :')
    print(np.max(frequency))
    return frequency,fourierValue


def add_new_uploaded_file ():
    if st.session_state['uploadedFileCheck'] is not None:
        st.session_state['uploadedFile']=st.session_state['uploadedFileCheck']
        dataArray,sampleRate= librosa.load(st.session_state['uploadedFileCheck'],sr=44100) #reading the sampling number of file
        frequency,fourierValues=fourier_transform(dataArray,sampleRate)
        st.session_state['mainFourierValues']=fourierValues.copy()
        st.session_state['fourierValues']=fourierValues.copy()
        st.session_state['frequency']=frequency
        st.session_state['maxFrequency']=int (sampleRate/2)
        st.session_state['sampleRate']=sampleRate


def change_frequency(sliderNumber,amplituideValue):
    maxFrequency=st.session_state['maxFrequency']
    st.write(type(maxFrequency))
    
    maxFrequencyRange=(math.ceil(sliderNumber*maxFrequency/10))
    minFrequencyRange=maxFrequencyRange-int(maxFrequency/10)

    pointsPerFrequency=int (len(st.session_state['frequency'])/maxFrequency)
    frequencyRange=[minFrequencyRange*pointsPerFrequency,maxFrequencyRange*pointsPerFrequency]
    dataCopy=st.session_state['mainFourierValues'][frequencyRange[0]:frequencyRange[1]].copy()
    st.session_state.fourierValues[frequencyRange[0]:frequencyRange[1]]= dataCopy*(1+amplituideValue/100)
     


if st.session_state['uploadedFile'] is None:
    st.sidebar.file_uploader("Upload your file", on_change=add_new_uploaded_file,key='uploadedFileCheck')
    isFileUploaded=False
else :
    browse=st.sidebar.button("Browse")
    isFileUploaded=True
    if browse:
        st.session_state['uploadedFile']=None
        st.experimental_rerun()
        


if isFileUploaded:
    # fig=plt.figure()
    # plt.plot(st.session_state['frequency'],abs(st.session_state['fourierValues']))
    # st.pyplot(fig)  
    groups = [  ('slider1',0),
            ('slider2',0),
            ('slider3',0),
            ('slider4',0),
            ('slider5',0),
            ('slider6',0),
            ('slider7',0),
            ('slider8',0),
            ('slider9',0),
            ('slider10',0),]
    sliders = {}
    columns = st.columns(len(groups),gap='small')

    for idx, i in enumerate(groups):
        min_value = -100
        max_value = 100
        key = idx+1
        with columns[idx]:
            sliders[key] = svs.vertical_slider(key=key, default_value=0,
                step=1, min_value=min_value, max_value=max_value)
            if sliders[key] == None:
                sliders[key]  = 0
            else:
                change_frequency(key,sliders[key])
    fig=plt.figure(figsize=(15,5))
  
    plt.plot(st.session_state.frequency ,abs(st.session_state['fourierValues']))
    modifiedData=fourier.irfft(st.session_state['fourierValues'])
    
    st.pyplot(fig)
    soundfile.write('temp1.wav', modifiedData,st.session_state.sampleRate, subtype='PCM_24')
    st.audio('temp1.wav', format='audio/wav')

    st.write(sliders)
 





st.button("Play")
st.button("Pause")
if st.sidebar.checkbox("Wave_Frequency"):
    st.write('a')
if st.sidebar.checkbox("Audio_Frequency"):
    st.write('b')
if st.sidebar.checkbox("Vowels_Frequency"):
    st.write('c')
if st.sidebar.checkbox("Medical_Instruments"):
    st.write('d')
if st.sidebar.checkbox("Music_Instruments"):
    st.write('e')



