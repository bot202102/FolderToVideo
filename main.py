import moviepy.editor as mp
import random
from os import listdir
from os.path import isfile, join
import time
import sys

titleFont = 'Exo-2-Bold'
fadeInTime = 1  # seconds
fadeOutTime = 1  # seconds
VIDEO_FPS = 25
VIDEO_CODEC = 'libx264'


def chek_font():
    # Check if the font is installed in the PC.
    fonts = mp.TextClip.list('font')
    if any(titleFont in s for s in fonts):
        print("Si existe el tipo de letra.")
    else:
        key = input("No EXISTE EL TIPO DE LETRA!!. Escribir ok para continuar. Presiona enter para salir.\n")
        if (key != 'ok'):
            sys.exit()


def get_files(dir_path, tipo):
    print("===================================================")
    files = []
    for f in listdir(dir_path):
        path = join(dir_path, f)
        if isfile(path):
            if tipo == "clips":
                t_str = mp.VideoFileClip(str(path)).set_start(0).audio_fadein(fadeInTime). \
                    audio_fadeout(1).fadein(fadeInTime).fadeout(fadeOutTime)
                files.append(t_str)
                print(f'Video encontrado: {path}')
            if tipo == "audio":
                files.append(path)
                if files:
                    print(f'Audio encontrado: {path}')
            if tipo == "logo":
                if files:
                    print(f'Se entontro un segundo logo: {path}')
                    return files
                else:
                    files.append(path)
                    if files:
                        print(f'Logo encontrado: {path}')

    return files


startTime = time.time()  # Take the time at the beginning to calculate the total time of processing.
chek_font()  # font is installed?
clips = get_files("./clips/", "clips")  # get clip names
if not clips:  # no video = exit
    input("No se encontraron archivos de video en la carpeta 'clips', no se puede continuar. Presiona enter para salir")
    sys.exit()
video = mp.concatenate_videoclips(clips)
bgMusicFiles = get_files("./audio/", "audio")  # get audio file names
if bgMusicFiles:  # if audio file exist, configure background audio
    musicLength = 0
    bgMusicClips = []
    random.shuffle(bgMusicFiles)
    _bgMusicFiles = bgMusicFiles
    while musicLength < video.duration:
        try:
            pop_bgMusicFiles = _bgMusicFiles.pop()
        except IndexError:
            _bgMusicFiles = bgMusicFiles
        bgMusicClips.append(mp.AudioFileClip(pop_bgMusicFiles).audio_fadein(1).audio_fadeout(1))
        musicLength += bgMusicClips[len(bgMusicClips) - 1].duration
    print("Canciones usadas: " + str(len(bgMusicFiles)) + " Duracion musica: " + str(musicLength) + " Duracion Videos: " +
          str(video.duration))
    if len(bgMusicClips) > 1:
        backgroundAudio = mp.CompositeAudioClip(bgMusicClips)
    else:
        backgroundAudio = bgMusicClips[0]
    compAudio = mp.CompositeAudioClip([video.audio.volumex(1.2), backgroundAudio.subclip(0, video.duration).volumex(0.08)])
    video = video.set_audio(compAudio.set_duration(video.duration))
else:
    print("No se encontraron archivos de sonido en la carpeta 'audio', se continua sin musica de fondo.")

# Titles
vid_title = input("Ingresar el nombre de la actividad: ")
if not vid_title:
    vid_title = "Script Python para Edición de Vídeo Automática"
title = mp.TextClip(vid_title, font=titleFont, color='white', fontsize=40, align='West')
title_col = title.on_color(size=(video.w, title.h + 10), color=(0, 0, 0), pos=(6, 'center'), col_opacity=0.3)
# color=(0,102,170)
title_mov = title_col.set_pos(lambda t: (max(video.w / 30, int(video.w - 0.5 * video.w * t)),
                                         max(5 * video.h / 6, int(100 * t))))
title_mov = title_col.set_pos('center', 'center').set_duration(5)
# Logos
logo_path = get_files("./logo/", "logo")
if logo_path:
    logo = (mp.ImageClip(logo_path[0])
            .set_duration(video.duration)
            .resize(height=70)  # if you need to resize...
            .margin(right=10, bottom=10, opacity=0)
            .set_pos(("right", "bottom")))

    final = mp.CompositeVideoClip([video, title_mov, logo])
else:
    final = mp.CompositeVideoClip([video, title_mov])

print(final.duration)
# final.subclip(0,30).write_videofile("test.mp4",fps=VIDEO_FPS, codec=VIDEO_CODEC)
final.subclip(0, video.duration).write_videofile(vid_title + ".mp4", fps=VIDEO_FPS, codec=VIDEO_CODEC, verbose=False)

endTime = time.time()
print("Procesing time:" + str(endTime - startTime))
