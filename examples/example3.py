import vlc
import time

sounds = list()
sounds.append("output.avi")

vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()

def play_sound(arg):
    media = vlc_instance.media_new(sounds[arg])
    player.set_media(media)
    player.play()
    time.sleep(1)
    duration = player.get_length() / 1000
    print(duration)
    time.sleep(duration)

play_sound(0)
