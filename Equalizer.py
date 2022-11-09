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


def change_frequency(sliderNumber,amplituideValue,sliders_mode):
    maxFrequency=st.session_state['maxFrequency'] 
    if sliders_mode==10:   
        maxFrequencyRange=(math.ceil(sliderNumber*maxFrequency/10))
        minFrequencyRange=maxFrequencyRange-int(maxFrequency/10)
    elif sliders_mode==6: 
        st.write("F")
        maxFrequencyRange=(math.ceil(sliderNumber*maxFrequency/10))
        minFrequencyRange=maxFrequencyRange-int(maxFrequency/10)

    else: 
        st.write("F")
        maxFrequencyRange=(math.ceil(sliderNumber*maxFrequency/10))
        minFrequencyRange=maxFrequencyRange-int(maxFrequency/10)

    pointsPerFrequency=int (len(st.session_state['frequency'])/maxFrequency)
    frequencyRange=[minFrequencyRange*pointsPerFrequency,maxFrequencyRange*pointsPerFrequency]
    dataCopy=st.session_state['mainFourierValues'][frequencyRange[0]:frequencyRange[1]].copy()
    st.session_state.fourierValues[frequencyRange[0]:frequencyRange[1]]= dataCopy*(1+amplituideValue/100)
    


file= st.sidebar.file_uploader("Upload your file",type={"csv","txt",".wav"}, on_change=add_new_uploaded_file,key='uploadedFileCheck')


# x_vals = []
# y_vals = []

# index = count()


# def animate():
   
#     x_vals.append(st.session_state["time"][index])
#     y_vals.append(st.session_state["dataArray"][index])

#     plt.cla()
    
   
#     plt.plot(x_vals, y_vals, label='Channel 1')
#     # plt.legend(loc='upper left')
#     # plt.tight_layout()


        
def control_music(control):
    if st.session_state['uploadedFile'] is not None:
        if control== "play": 
            pygame.mixer.init()
            if st.session_state['modified_wav_file']  is not None:
                pygame.mixer.music.load(st.session_state['modified_wav_file'])
                pygame.mixer.music.play()  
            else:
                pygame.mixer.music.load(file) 
                pygame.mixer.music.play()

                # fig=plt.figure(figsize=(15,5))
                # ani=FuncAnimation(fig, animate,frames=np.arange(1,100,0.1),interval=1000,blit=False)

                # with open("myvideo.html","w") as f:
                #     print(ani.to_html5_video(),file=f)

                # HtmlFile=open("myvideo.html","r")
                # source_code=HtmlFile.read()
                # components.html(source_code,height=900,width=900)
                # st.pyplot(fig)

        elif  pygame.mixer.get_init() is not None:
            if control== "pause":
                pygame.mixer.music.pause()
            elif control=="resume":    
                pygame.mixer.music.unpause()



# ani = FuncAnimation(plt.gcf(), animate, interval=1000)

# plt.tight_layout()
# plt.show()



            
    # fig=plt.figure(figsize=(15,5))
    # plt.plot(st.session_state.frequency ,(((2.0/ st.session_state['FileLength']))* abs(st.session_state['fourierValues'])))
    # st.pyplot(fig)
    # st.audio('temp1.wav', format='audio/wav')


radio_check= st.sidebar.radio("choose:",("Frequency","Vowels_Frequency","Music_Instruments"))


if st.session_state['uploadedFile'] is not None:
    if st.button("Play"):
        control_music("play")  
    if st.button("Pause"): 
        control_music("pause")   
    if st.button("Resume"):
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
        min_value = -100
        max_value = 100
        key = idx+1
        with columns[idx]:
            
            sliders[key] = svs.vertical_slider(key=key, default_value=0,
                step=1, min_value=min_value, max_value=max_value)
            if sliders[key] == None:
                sliders[key]  = 0
            else:
                change_frequency(key,sliders[key],sliders_number)

            st.caption(str((key-1)*int((st.session_state['maxFrequency']/10)))+"-"+str(int(key*st.session_state['maxFrequency']/10))+"Hz" )

    if st.button("Apply"):
        modifiedData=fourier.irfft(st.session_state['fourierValues'],n=st.session_state['FileLength'])

        if pygame.mixer.get_init() is not None:
                pygame.mixer.quit()
        soundfile.write('temp1.wav', modifiedData,st.session_state['sampleRate'], subtype='PCM_16')
        st.session_state['modified_wav_file'] ='temp1.wav'

    fig=plt.figure(figsize=(15,5))
    plt.plot(st.session_state['frequency'] ,(((2.0/ st.session_state['FileLength']))* abs(st.session_state['fourierValues'])))
    st.pyplot(fig)