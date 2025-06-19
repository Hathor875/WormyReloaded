from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import threading

class MusicPlayer:
    def __init__(self):
        self.current_playback = None
        self.lock = threading.Lock()

    def play(self, file_path, speed=1.0, loop=False):
        """
        Odtwarza plik audio (ogg/wav/mp3) z możliwością zmiany prędkości.
        Jeśli loop=True, odtwarza w pętli (blokuje wątek).
        """
        self.stop()
        sound = AudioSegment.from_file(file_path)
        if speed != 1.0:
            sound = sound._spawn(sound.raw_data, overrides={
                "frame_rate": int(sound.frame_rate * speed)
            }).set_frame_rate(sound.frame_rate)
        def _play():
            while True:
                playback = _play_with_simpleaudio(sound)
                with self.lock:
                    self.current_playback = playback
                playback.wait_done()
                if not loop:
                    break
        t = threading.Thread(target=_play, daemon=True)
        t.start()

    def stop(self):
        with self.lock:
            if self.current_playback:
                self.current_playback.stop()
                self.current_playback = None

music_player = MusicPlayer()
