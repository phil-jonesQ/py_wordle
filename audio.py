"""Small synthesized sound effects for game feedback."""

from array import array
import math
import sys

import pygame


class AudioFeedback:
    """Generate short tones without requiring additional audio assets."""

    def __init__(self):
        self.sounds = {}
        if pygame.mixer.get_init() is None:
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=1)
            except pygame.error as error:
                print(f"Audio disabled: {error}", file=sys.stderr)
                return

        frequency, _, channels = pygame.mixer.get_init()
        self.sounds = {
            "type": self._tone(frequency, channels, 440, 0.035),
            "invalid": self._tone(frequency, channels, 180, 0.13),
            "submit": self._tone(frequency, channels, 620, 0.09),
            "win": self._tone(frequency, channels, 880, 0.22),
            "lose": self._tone(frequency, channels, 240, 0.24),
        }

    @staticmethod
    def _tone(frequency, channels, pitch, duration):
        sample_count = int(frequency * duration)
        samples = array('h')
        for index in range(sample_count):
            envelope = 1 - index / sample_count
            sample = int(
                math.sin(2 * math.pi * pitch * index / frequency)
                * 7000 * envelope)
            samples.extend([sample] * channels)
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play(self, sound_name):
        """Play a sound effect if the audio mixer initialized successfully."""
        sound = self.sounds.get(sound_name)
        if sound is not None:
            sound.play()
