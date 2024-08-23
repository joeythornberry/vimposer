from vimposercore.MidiPlayer import MidiPlayer
import subprocess


class LinuxMidiPlayer(MidiPlayer):

    def initialize_player(self):
        self.player_process = subprocess.Popen(["timidity", "-iA", "> /dev/null", "2> /dev/null"])

    def play_note(self, instrument: int, pitch: int, velocity: int):
        subprocess.Popen(["./sendnote", str(0), str(pitch), str(velocity)])

    def play_file(self, filename: str):
        self.play_file_process = subprocess.Popen(["./playsmf", "--out", "1", filename])

    def stop_playing_file(self):
        if hasattr(self, "play_file_process"):
            self.play_file_process.terminate()

    def close_player(self):
        if hasattr(self, "player_process"):
            self.player_process.terminate()
