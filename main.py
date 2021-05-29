import moviepy.editor as mp
from random import randint
import time
import sys

titleFont = 'Exo-2-Bold'
fadeInTime = 1  # seconds
fadeOutTime = 1  # seconds
VIDEO_FPS = 25
VIDEO_CODEC = 'libx264'
vid_title = "Script Python para Edición de Vídeo Automática"
startTime = time.time()  # Take the time at the beginning to calculate the total time of processing.
fonts = mp.TextClip.list('font')


if any(titleFont in s for s in fonts):
    print("Title font installed.")
else:
    key = input("TITLE FONT NOT INSTALLED!!. "
                "Press ok and press enter to continue using default font. Press Enter to exit\n")
    if key != 'ok':
        sys.exit()
bgMusicFiles = ["sunday_plans","no_good_right","slow_burn","whiskey","zigzag","ambient_1","at_the_mansion"
    ,"deeper","autumn"]
numberOfClips = 0
video = mp.VideoFileClip("./clips/1.MP4").set_start(0).audio_fadein(1).audio_fadeout(1).fadein(1).fadeout(1)

'''
clip1 = mp.VideoFileClip("./clips/1.MP4").set_start(0).audio_fadein(fadeInTime).audio_fadeout(1).fadein(fadeInTime).fadeout(fadeOutTime)
clip2 = mp.VideoFileClip("./clips/2.MP4").set_start(0).audio_fadein(fadeInTime).audio_fadeout(1).fadein(fadeInTime).fadeout(fadeOutTime)

video = mp.concatenate_videoclips([clip1,clip2])'''

musicLength = 0
bgMusicClips = []

print("Audio Clips Used:")

randomNumber = lastRandomNumber = 0

while musicLength < video.duration:
    while randomNumber == lastRandomNumber:
        randomNumber = randint(0, len(bgMusicFiles) - 1)

    lastRandomNumber = randomNumber
    print(bgMusicFiles[randomNumber] + ".mp3")
    bgMusicClips.append(
        mp.AudioFileClip("./audio/" + bgMusicFiles[randomNumber] + ".mp3").audio_fadein(1).audio_fadeout(1))
    musicLength += bgMusicClips[len(bgMusicClips) - 1].duration

print("Songs used:" + str(len(bgMusicFiles)) + " Music duration:" + str(musicLength) + " Video Length:" + str(
    video.duration))

if len(bgMusicClips) > 1:
    backgroundAudio = mp.CompositeAudioClip(bgMusicClips)
else:
    backgroundAudio = bgMusicClips[0]

compAudio = mp.CompositeAudioClip([video.audio.volumex(1.2), backgroundAudio.subclip(0, video.duration).volumex(0.08)])

video = video.set_audio(compAudio.set_duration(video.duration))

title = mp.TextClip(vid_title, font=titleFont, color='white', fontsize=40, align='West')

title_col = title.on_color(size=(video.w, title.h + 10),
                           color=(0, 0, 0), pos=(6, 'center'), col_opacity=0.3)
# color=(0,102,170)

title_mov = title_col.set_pos(lambda t: (max(video.w / 30, int(video.w - 0.5 * video.w * t)),
                                         max(5 * video.h / 6, int(100 * t))))

logo = (mp.ImageClip("logo.png")
        .set_duration(video.duration)
        .resize(height=70)  # if you need to resize...
        .margin(right=10, bottom=10, opacity=0)
        .set_pos(("right", "bottom")))

final = mp.CompositeVideoClip([video, title_mov, logo])
print(final.duration)
# final.subclip(0,30).write_videofile("test.mp4",fps=VIDEO_FPS, codec=VIDEO_CODEC)
final.subclip(0, video.duration).write_videofile(vid_title + ".mp4", fps=VIDEO_FPS, codec=VIDEO_CODEC, verbose=False,
                                                 progress_bar=True)

endTime = time.time()
print("Procesing time:" + str(endTime - startTime))


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('lll')
