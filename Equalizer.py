import streamlit as st
import streamlit_vertical_slider  as svs
import streamlit.components.v1 as components
import scipy.fft as fourier
import numpy as np
import librosa 
import math
import matplotlib.pyplot as plt 
import soundfile
import pygame
import pandas as pd
import time
import altair as alt
import mpld3
from matplotlib.animation import FuncAnimation



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
    fourierValue=fourier.rfft(x)
    frequency=fourier.rfftfreq(len(x),1/(sampleRate))
    return frequency,fourierValue

def add_new_uploaded_file ():
    if st.session_state['uploadedFileCheck'] is not None:
        st.session_state['uploadedFile']=st.session_state['uploadedFileCheck']
        file=st.session_state['uploadedFile']
        if file.type=='audio/wav':
            st.session_state["dataArray"],sampleRate= librosa.load(st.session_state['uploadedFileCheck'],sr=44100,duration=10) #reading the sampling number of file
            st.session_state['FileLength']=len(st.session_state["dataArray"])
            st.session_state['time']=np.arange(0,st.session_state['FileLength'])/sampleRate
        else :
            file=pd.read_csv(file)
            time =file.iloc[:,0]
            st.session_state['dataArray']=file.iloc[:,1].to_numpy()
            st.session_state['time']=time
            st.session_state['FileLength']=len(st.session_state["dataArray"])
            sampleRate=1/(time[1]-time[0])
        
        st.session_state['modified_data']=st.session_state.dataArray.copy()
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

def maleFemaleChange():
    sampleRate =st.session_state.sampleRate
    shiftBy=st.slider('change Voice',min_value=-50,max_value=50,value=0)
    st.session_state.modified_data=librosa.effects.pitch_shift(st.session_state.dataArray ,sampleRate,n_steps=shiftBy)

def make_sliders():
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
    elif radio_check=='Male-Female':
        maleFemaleChange()
        sliders_number=0
    else:
        sliders_number=10
    if sliders_number!=0:
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

def play_buttons():
        global spectroCheckBox,Apply
        col1,col2=st.sidebar.columns([1,2])
        with col2:
            spectroCheckBox=st.checkbox('Spectrogram')
            st.checkbox('signal time')

        if col1.button("Play"):
            control_music("play")  
        if col1.button("Pause"): 
            control_music("pause")   
        if col1.button("Resume"):
            control_music("resume")
        Apply =col1.button("Apply")

def apply_action():
        if radio_check !='Male-Female':
            st.session_state['modified_data']=fourier.irfft(st.session_state['fourierValues'],n=st.session_state['FileLength'])
        if pygame.mixer.get_init() is not None:
            pygame.mixer.quit()
        soundfile.write('tem1.wav', st.session_state['modified_data'],st.session_state['sampleRate'], subtype='PCM_16')
        st.session_state['modified_wav_file'] ='tem1.wav'

def spectrogram(data):
    fig =plt.figure(figsize=(8,3))
    plt.specgram(data, Fs=st.session_state.sampleRate,cmap='jet')
    plt.colorbar()
    plt.show()
    return fig 

def drawSpectro(data,title,):
        if spectroCheckBox:
            fig =spectrogram(data)
            plt.title(title, 
                fontsize = 14, fontweight ='bold')
            fig_html = mpld3.fig_to_html(fig)
            components.html(fig_html,height=300)

def sound_mode():
    play_buttons()
    
    leftUpColumns,rightUpColumns=st.columns(2)
    with leftUpColumns:
        drawSpectro(st.session_state.dataArray,title='RealSignal')
    
    make_sliders()

    if Apply: #sidebar
        apply_action()
    with rightUpColumns:
        drawSpectro(st.session_state.modified_data,title='Modified Signal')

def draw_medical_signal(data,title):
    time=st.session_state.time
    fig=plt.figure(figsize=(8,3))
    plt.plot(time,data)
    plt.title(title, 
        fontsize = 14, fontweight ='bold')
    fig_html=mpld3.fig_to_html(fig)
    components.html(fig_html,height=300)

def medical_mode():
    magnitude=st.session_state.dataArray.copy()
    maxFreqeuency=st.session_state.maxFrequency
    mainFourierValues=st.session_state.mainFourierValues.copy()
    PPF=int(len(st.session_state.fourierValues)/maxFreqeuency)#points per frequency

    smallFreq=st.slider('x1',min_value=0.,max_value=1.,value=0.5)
    highFreq=st.slider('x2',min_value=0.,max_value=1.,value=0.5)

    fourierValues=st.session_state['fourierValues']
    fourierValues[PPF*130:]=smallFreq*mainFourierValues[PPF*130:]
    fourierValues[PPF*80:PPF*120]=highFreq*mainFourierValues[PPF*80:PPF*120]
    modifiedData=fourier.irfft(fourierValues)

    col1,col2=st.columns(2)
    with col1:
        draw_medical_signal(magnitude,'Real Signal')
    with col2:
        draw_medical_signal(modifiedData,'Modified Signal')    

def main():
    global file,radio_check
    file= st.sidebar.file_uploader("Upload your file",type={"csv",".wav"}, on_change=add_new_uploaded_file,key='uploadedFileCheck')
    radio_check= st.sidebar.radio("choose:",("Frequency","Vowels_Frequency","Music_Instruments",'Male-Female'))
    if file is not None:
        if file.type =='audio/wav':
            sound_mode()
        else :
            medical_mode()

main()
