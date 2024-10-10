from vimposercore.MidiPlayer import MidiPlayer
import subprocess


class LinuxMidiPlayer(MidiPlayer):

    # This is stupid and doesn't work
    play_file_process: subprocess.Popen | None

    def __init__(self):
        self.play_file_process = None

    def play_note(self, instrument: int, pitch: int, velocity: int):
        """I tried this for playing single notes,
           but there's over a second of latency, so it's not viable"""
        cmd = f"./sendmidi --out 1 --note-on {0} {pitch} {velocity}"
        subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL)

    def play_file(self, filename: str):
        """Literally just call tiMIDIty to play the file, and
           keep track of the spawned background process"""
        cmd = f"timidity {filename}"
        self.play_file_process = subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL)

    def toggle_playing(self, filename):
        """Ideally, press Space to start and stop playing. Once it finishes, you 
           have to press Space twice to start it again, because I can't figure 
           out how to tell if the timidity process has terminated on its own..."""
        if self.play_file_process != None:
            self.play_file_process.kill()

        if (self.play_file_process == None or self.play_file_process.poll() != None):
            self.play_file(filename)
        else:
            self.play_file_process = None

    def is_playing(self):
        """This doesn't work because timidity doesn't seem
           to tell the truth when you poll it."""
        if self.play_file_process == None:
            return False
        return self.play_file_process.poll() == None
