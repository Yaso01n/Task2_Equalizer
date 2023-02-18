import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import librosa
from numpy.fft import rfft, irfft, rfftfreq
import matplotlib.pyplot as plt


fig1 = go.Figure()
# set x axis label
fig1.update_xaxes(
    title_text="frequency",  # label
    title_font={"size": 20},
    title_standoff=25)
# set y axis label
fig1.update_yaxes(
    title_text="Amplitude(mv)",
    title_font={"size": 20},
    # label
    title_standoff=25)

fig2 = go.Figure()
# set x axis label
fig2.update_xaxes(
    title_text="frequency",  # label
    title_font={"size": 20},
    title_standoff=25)
# set y axis label
fig2.update_yaxes(
    title_text="Amplitude(mv)",
    title_font={"size": 20},
    # label
    title_standoff=25)

fig3 = go.Figure()
# set x axis label
fig3.update_xaxes(
    title_text="frequency",  # label
    title_font={"size": 20},
    title_standoff=25)
# set y axis label
fig3.update_yaxes(
    title_text="Amplitude(mv)",
    title_font={"size": 20},
    # label
    title_standoff=25)
file =st.file_uploader('Browse',type={'csv'})
file_uploaded = pd.read_csv(file)

ig_sig = fig1.add_scatter(
    x=file_uploaded.iloc[:, 0], y=file_uploaded.iloc[:, 1]  )

st.plotly_chart(ig_sig, use_container_width=True)


def plot(y_axis):
    fig_sig = fig2.add_scatter(x=file_uploaded.iloc[:, 0], y=y_axis)
    st.plotly_chart(fig_sig, use_container_width=True)


def fourier_for_input(data):
    time = data.iloc[:, 0]
    magnitude = data.iloc[:, 1]
    sample_period = time[1]-time[0]
    n_samples = len(time)
    fourier = rfft(magnitude)

    frequencies = rfftfreq(n_samples, sample_period)
    counter = 0
    factor = 1
    print ( len (frequencies))
    print(len(fourier))
    # print (frequencies)
    for frequencies in range(0,50):
        if frequencies == 32:
            fourier[counter] *= w
        counter += 1
    return np.real(irfft(fourier))


def main():
    magnitudes = fourier_for_input(file_uploaded)
    fig_si = fig3.add_scatter(x=file_uploaded.iloc[:, 0], y=magnitudes)
    st.plotly_chart(fig_si, use_container_width=True)

w = st.slider(label="slider", min_value=0.0, max_value=1.0, value=0.5)
y = st.slider(label="slider1", min_value=-5.0, max_value=5.0, value=0.5)
z = st.slider(label="slider2", min_value=-5.0, max_value=5.0, value=0.5)
if __name__ == "__main__":
    main()
