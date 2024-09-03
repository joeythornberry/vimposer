from vimposercore.MidiPlayer import MidiPlayer
import subprocess


class LinuxMidiPlayer(MidiPlayer):

    def initialize_player(self):
        cmd = "timidity -iA"
        self.player_process = subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL)

    def play_note(self, instrument: int, pitch: int, velocity: int):
        cmd = f"./sendmidi --out 1 --note-on {0} {pitch} {velocity}"
        subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL)

    def play_file(self, filename: str):
        self.play_file_process = subprocess.Popen(["./playsmf", "--out 1", filename], stdout=subprocess.DEVNULL)

    def stop_playing_file(self):
        if hasattr(self, "play_file_process"):
            self.play_file_process.terminate()

    def close_player(self):
        if hasattr(self, "player_process"):
            self.player_process.kill()
