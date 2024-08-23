from abc import abstractmethod


class MidiPlayer:
    
    @abstractmethod
    def initialize_player(self):
        pass

    @abstractmethod
    def play_note(self, instrument: int, pitch: int, velocity: int):
        pass

    @abstractmethod
    def play_file(self, filename: str):
        pass

    @abstractmethod
    def stop_playing_file(self):
        pass

    @abstractmethod
    def close_player(self):
        pass
