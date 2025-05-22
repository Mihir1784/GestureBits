from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui

class MediaController:
    def __init__(self):
        # Initialize volume control using pycaw
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume_range = self.volume.GetVolumeRange()
        self.min_vol, self.max_vol = volume_range[0], volume_range[1]
        self.is_playing = True

    def volume_up(self):
        current_vol = self.volume.GetMasterVolumeLevelScalar()
        new_vol = min(1.0, current_vol + 0.05)
        self.volume.SetMasterVolumeLevelScalar(new_vol, None)
        return new_vol

    def volume_down(self):
        current_vol = self.volume.GetMasterVolumeLevelScalar()
        new_vol = max(0.0, current_vol - 0.05)
        self.volume.SetMasterVolumeLevelScalar(new_vol, None)
        return new_vol

    def toggle_play_pause(self):
        pyautogui.press('playpause')
        self.is_playing = not self.is_playing
        return self.is_playing

    def next_track(self):
        pyautogui.press('nexttrack')

    def previous_track(self):
        pyautogui.press('prevtrack')

    def get_current_volume(self):
        return self.volume.GetMasterVolumeLevelScalar() 