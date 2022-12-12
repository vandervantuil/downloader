import PySimpleGUI as sg
import moviepy.editor as mp
from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress
import os
import re

layout = [
         [sg.Text('LINK  ->'), sg.InputText()],
         [sg.Text('Qual a pasta?'), sg.InputText(), sg.FolderBrowse()],
         [sg.Button('Playlist em .MP3'), sg.Button('Vídeo em .MP4'), sg.Button('Vídeo em .MP3'), sg.Button('.MP4 to .MP3'), sg.Button('CANCELAR')]
        ]

janela = sg.Window("YouTube downloader ... by: Frolesta", layout)

def playlist(l, p):
    
    playlist = Playlist(l)
    print(f'Playlist: {playlist.title}')
    counter = 0

    for url in playlist.video_urls:
        counter += 1
        print(f'Downloading ({counter}/{len(playlist)})')
        ys = YouTube(url)
        print(f"Title: {ys.title}")
        v = ys.streams.get_audio_only()
        out_file = v.download(output_path=p)
        
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        os.system('cls')

def musica(l, p):
    yt = YouTube(l, on_progress_callback=on_progress)
    print('Título: ', yt.title)
    print('Downloading ...')
    ys = yt.streams.get_audio_only()
    out_file = ys.download(output_path=p)

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    os.system('cls')

def video(l, p):
    yt = YouTube(l, on_progress_callback=on_progress)
    print('Título: ', yt.title)
    print('Downloading ...')
    ys = yt.streams.get_highest_resolution()
    ys.download(output_path=p)

def converter(p):
    for file in os.listdir(p):
        if re.search('mp4', file):                          
            mp4_temp = os.path.join(p , file)   #Cria uma variavel para armazenar o arquivo .MP4
            mp3_temp = os.path.join(p, os.path.splitext(file)[0]+'.mp3') #Variavel que cria o nome do arquivo e adiciona .MP3 ao final
            new_file = mp.AudioFileClip(mp4_temp)  #Cria o arquivo de áudio (.MP3)
            new_file.write_audiofile(mp3_temp)     #Renomeia o arquivo, setando o nome criado anteriormente
            os.remove(mp4_temp)                    #Remove o arquivo .MP4
    print("Download Completo")

while True: 
    event, values = janela.read()
    if event == "Cancelar" or event == sg.WIN_CLOSED:
        break
    elif event == 'Playlist em .MP3':
        playlist(values[0], values[1])
        sg.popup_ok('TUDO TERMINADO :D')
    elif event == 'Vídeo em .MP4':
        video(values[0], values[1])
        sg.popup_ok('TUDO TERMINADO :D')
    elif event == '.MP4 to .MP3':
        converter(values[1])
        sg.popup_ok('TUDO TERMINADO :D')
    elif event == 'Vídeo em .MP3':
        musica(values[0], values[1])
        sg.popup_ok('TUDO TERMINADO :D')

janela.close()