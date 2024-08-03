from testutils.MockFrontend import MockFrontend
from testutils.MockMidiViewport import MockMidiViewport
from vimposercore.VimposerAPI import VimposerAPI
from vimposermidi.TrackMidiManager import TrackMidiManager

class VimposerTester:
    mock_frontend: MockFrontend
    mock_midi_viewport: MockMidiViewport
    track_midi_manager: TrackMidiManager
    track_midi_manager_observed: bool

    def __init__(self):
        self.mock_frontend = MockFrontend()
        self.mock_midi_viewport = MockMidiViewport()
        self.track_midi_manager_observed = False

    def assert_note_exists(self, p: int, x: int, l: int, track: int):
        assert self.track_midi_manager_observed, "You forgot to observe the TrackMidiManager."
        note_exists, msg = self.mock_frontend.has_note(p, x, l)
        assert note_exists, msg
        assert self.track_midi_manager.has_note(p, x, l, track), "That note does not exist in the TrackMidiManager."

    def observe_track_midi_manager(self, vimposer_api: VimposerAPI):
        self.track_midi_manager = vimposer_api.midi_manager.track_midi_manager
        self.track_midi_manager_observed = True
