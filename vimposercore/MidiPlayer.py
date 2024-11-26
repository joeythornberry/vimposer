import rtmidi
import time
import queue
import threading
from dataclasses import dataclass

@dataclass
class NoteMessage:
    kind: int
    instrument: int
    pitch: int
    velocity: int
    when: float

class MidiPlayer():
    """Manages and controls MIDI synthesizer to play notes."""

    def __init__(self):
        self.queue = queue.Queue()
        threading.Thread(target=self.listen, daemon=True).start()
        self.midiout = rtmidi.MidiOut()
        self.midiout.open_port(1)
        self.waiting_messages: list[NoteMessage] = []

    def play_note(self, instrument: int, pitch: int, velocity: int):
        """Play a note with the given attributes."""
        on = NoteMessage(0x90, instrument, pitch, velocity, 0)
        self.queue.put(on)
        note_duration = 1000
        off_time = time.time_ns() + note_duration
        off = NoteMessage(0x80, instrument, pitch, velocity, off_time)
        self.queue.put(off)

    def send_waiting_messages(self):
        """Send MIDI events that need to "wait" for a certain 
           time, like note-off events."""
        for message in self.waiting_messages:
            if message.when < time.time_ns():
                note_off = [0x80, message.pitch, 0]
                self.midiout.send_message(note_off)
                self.waiting_messages.remove(message)

    def send_note_on(self, message: NoteMessage):
            note_on = [0x90, message.pitch, message.velocity]
            self.midiout.send_message(note_on)

    def listen(self):
        """Background function that checks input queue for 
           events to send, and then send them."""
        while True:
            try:
                message = self.queue.get_nowait()
                if message.kind == 0x90:
                    self.send_note_on(message)
                    self.send_waiting_messages()
                elif message.kind == 0x80:
                    self.waiting_messages.append(message)
                    self.send_waiting_messages()
            except:
                pass
            finally:
                time.sleep(0.01)
