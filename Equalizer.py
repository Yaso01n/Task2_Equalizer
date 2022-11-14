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
from itertools import count
import pandas as pd
import time
import altair as alt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import streamlit.components.v1 as components

#range of frequency domain of letters is (0-4000hz)
st.set_page_config(page_title="Equalizer", page_icon=":headphones:",layout="wide")
 

if 'uploadedFile' not in st.session_state:
    st.session_state['uploadedFile']=None

if 'modified_wav_file' not in st.session_state:
    st.session_state['modified_wav_file']=None   

if 'radio_check' not in st.session_state:
    st.session_state['radio_check']=0 

if 'modified_data' not in st.session_state:
    st.session_state['modified_data']=None  
          

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


def plot_animation(df):
    lines = alt.Chart(df).mark_line().encode(
            x=alt.X("x_axis", axis=alt.Axis(title='Time')),
            y=alt.Y('y_axis', axis=alt.Axis(title='Magnitude')),
        ).properties(
            width=900,
            height=600
        )
    return lines
    
def realtime(file):
    df =file
    lines = plot_animation(df)
    line_plot = st.altair_chart(lines)
    N = df.shape[0]
    burst = 1      
    size = burst    
    for i in range(1, 980):
        step_df = df.iloc[0:size]
        lines = plot_animation(step_df)
        line_plot = line_plot.altair_chart(lines)
        size = i + burst
        if size >= N:
            size = N - 1
        time.sleep(.000000001)
    st.experimental_rerun()     

def fourier_transform(x,sampleRate):
    fourierValue=np.fft.rfft(x)
    frequency=np.fft.rfftfreq(len(x),1/(sampleRate))
    return frequency,fourierValue


def add_new_uploaded_file ():
    if st.session_state['uploadedFileCheck'] is not None:
        st.session_state['uploadedFile']=st.session_state['uploadedFileCheck']
        st.session_state["dataArray"],sampleRate= librosa.load(st.session_state['uploadedFileCheck'],sr=44100,duration=10) #reading the sampling number of file
        st.session_state['FileLength']=len(st.session_state["dataArray"])
        st.session_state['time']=np.arange(0,st.session_state['FileLength'])/sampleRate
        frequency,fourierValues=fourier_transform(st.session_state["dataArray"],sampleRate)
        st.session_state['mainFourierValues']=fourierValues.copy()
        st.session_state['fourierValues']=fourierValues.copy()
        st.session_state['frequency']=frequency
        st.session_state['maxFrequency']=int (sampleRate/2)
        st.session_state['sampleRate']=sampleRate


def change_frequency(sliderNumber,amplituideValue,sliders_number):
    maxFrequency=st.session_state['maxFrequency'] 
    if sliders_number==10:   
        maxFrequencyRange=(math.ceil(sliderNumber*maxFrequency/10))
        minFrequencyRange=maxFrequencyRange-int(maxFrequency/10)
    elif sliders_number==6: 
        maxFrequencyRange=(math.ceil(sliderNumber*maxFrequency/10))
        minFrequencyRange=maxFrequencyRange-int(maxFrequency/10)

    else: 
        if sliderNumber==1:
            minFrequencyRange,maxFrequencyRange=0,800
        elif sliderNumber==2:
            minFrequencyRange,maxFrequencyRange=800,5000
        elif sliderNumber==3:
            minFrequencyRange,maxFrequencyRange=5000,20000
        else:
            minFrequencyRange,maxFrequencyRange=0,0
            
    pointsPerFrequency=int (len(st.session_state['frequency'])/maxFrequency)
    frequencyRange=[minFrequencyRange*pointsPerFrequency,maxFrequencyRange*pointsPerFrequency]
    dataCopy=st.session_state['mainFourierValues'][frequencyRange[0]:frequencyRange[1]].copy()
    st.session_state.fourierValues[frequencyRange[0]:frequencyRange[1]]= dataCopy*(amplituideValue)
    


file= st.sidebar.file_uploader("Upload your file",type={"csv","txt",".wav"}, on_change=add_new_uploaded_file,key='uploadedFileCheck')

def control_music(control):
    if st.session_state['uploadedFile'] is not None:
        if control== "play": 
            pygame.mixer.init()
            if st.session_state['modified_wav_file']  is not None:
                data=pd.DataFrame({'y_axis':st.session_state['modified_data'][::1800],'x_axis':st.session_state['time'][::1800]})
                pygame.mixer.music.load(st.session_state['modified_wav_file'])
                pygame.mixer.music.play()
                realtime(data)
             
            else:
                data=pd.DataFrame({'y_axis':st.session_state["dataArray"][::1800],'x_axis':st.session_state['time'][::1800]})
                pygame.mixer.music.load(file) 
                pygame.mixer.music.play()
                realtime(data) 
        

        elif  pygame.mixer.get_init() is not None:
            if control== "pause":
                pygame.mixer.music.pause()
            elif control=="resume":    
                pygame.mixer.music.unpause()


radio_check= st.sidebar.radio("choose:",("Frequency","Vowels_Frequency","Music_Instruments"))


if st.session_state['uploadedFile'] is not None:
    if st.sidebar.button("Play"):
        control_music("play")  
    if st.sidebar.button("Pause"): 
        control_music("pause")   
    if st.sidebar.button("Resume"):
        control_music("resume")
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
    if radio_check=="Vowels_Frequency":
        sliders_number=6
    elif radio_check== "Music_Instruments":
            sliders_number=4
    else:
        sliders_number=10
        
    columns = st.columns(sliders_number,gap='small')

    for idx in range(sliders_number):
        min_value = 0
        max_value = 2
        key = idx+1
        with columns[idx]:
            
            sliders[key] = svs.vertical_slider(key=key, default_value=1,
                step=0.1, min_value=min_value, max_value=max_value)
            if sliders[key] == None:
                sliders[key]  = 0
            else:
                change_frequency(key,sliders[key],sliders_number)

            st.caption(str((key-1)*int((st.session_state['maxFrequency']/10)))+"-"+str(int(key*st.session_state['maxFrequency']/10))+"Hz" )

    if st.sidebar.button("Apply"):
        st.session_state['modified_data']=fourier.irfft(st.session_state['fourierValues'],n=st.session_state['FileLength'])

        if pygame.mixer.get_init() is not None:
                pygame.mixer.quit()
        soundfile.write('temp1.wav', st.session_state['modified_data'],st.session_state['sampleRate'], subtype='PCM_16')
        st.session_state['modified_wav_file'] ='temp1.wav'