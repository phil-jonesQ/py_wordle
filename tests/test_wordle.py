"""Tests for Wordle scoring and keyboard input."""

import os
import unittest
from unittest.mock import patch

import pygame

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from audio import AudioFeedback
from py_wordle import Wordle, parse_args


class WordleTests(unittest.TestCase):
    def setUp(self):
        with patch.object(
                Wordle, "load_random_word",
                return_value=("APPLE", ["APPLE", "CRANE", "LEVEL"])):
            self.game = Wordle()

    def set_guess(self, guess):
        self.game.letter_store[0] = list(guess)

    def test_duplicate_letters_are_only_marked_yellow_once(self):
        self.game.the_word = "APPLE"

        self.assertEqual(
            self.game.translate_guess("ALLEY"),
            ["G", "Y", "_", "Y", "_"])

    def test_duplicate_secret_letters_mark_only_matching_count(self):
        self.game.the_word = "LEVEL"

        self.assertEqual(
            self.game.translate_guess("EEEEE"),
            ["_", "G", "_", "G", "_"])

    def test_extra_letters_are_ignored_when_row_is_full(self):
        col = 0
        for letter in "CRANEB":
            col = self.game.add_letter(0, col, letter)

        self.assertEqual(col, 5)
        self.assertEqual(self.game.decode_guess(0), "CRANE")
        self.assertEqual(len(self.game.letter_store[0]), 5)

    def test_backspace_at_start_is_safe(self):
        self.assertEqual(self.game.remove_letter(0, 0), 0)
        self.assertEqual(self.game.decode_guess(0), "_____")

    def test_backspace_removes_last_entered_letter(self):
        col = self.game.add_letter(0, 0, "C")
        col = self.game.remove_letter(0, col)

        self.assertEqual(col, 0)
        self.assertEqual(self.game.decode_guess(0), "_____")

    def test_incomplete_guess_shows_message_without_changing_score(self):
        self.game.add_letter(0, 0, "A")

        self.assertFalse(self.game.submit_guess(0))
        self.assertEqual(self.game.status_message, "Enter a five-letter word")
        self.assertEqual(self.game.game_data["score"], 90)

    def test_unrecognized_guess_shows_message_without_scoring(self):
        self.set_guess("QWERT")

        self.assertFalse(self.game.submit_guess(0))
        self.assertEqual(self.game.status_message, "Not in word list")
        self.assertEqual(self.game.game_data["score"], 90)
        self.assertEqual(self.game.grid_state[(0, 0)], "DEFAULT")

    def test_valid_guess_is_scored(self):
        self.set_guess("CRANE")

        self.assertTrue(self.game.submit_guess(0))
        self.assertEqual(self.game.status_message, "")
        self.assertEqual(self.game.game_data["score"], 80)
        self.assertEqual(
            [self.game.grid_state[(0, col)] for col in range(5)],
            ["GREY", "GREY", "YELLOW", "GREY", "GREEN"])
        self.assertFalse(self.game.game_data["game_over"])

    def test_correct_guess_ends_the_game(self):
        self.set_guess("APPLE")

        self.assertTrue(self.game.submit_guess(0))
        self.assertTrue(self.game.game_data["win"])
        self.assertTrue(self.game.game_data["game_over"])

    def test_debug_flag_controls_secret_word_logging(self):
        with patch.object(
                Wordle, "load_random_word",
                return_value=("APPLE", ["APPLE"])), patch("builtins.print") as output:
            Wordle(debug=False)
            output.assert_not_called()

            Wordle(debug=True)
            output.assert_called_once_with("Debug: secret word is APPLE")

    def test_debug_command_line_flag(self):
        self.assertFalse(parse_args([]).debug)
        self.assertTrue(parse_args(["-d"]).debug)
        self.assertTrue(parse_args(["--debug"]).debug)

    def test_audio_effects_are_created_without_external_assets(self):
        with patch("audio.pygame.mixer.get_init",
                   return_value=(22050, -16, 1)), patch(
                       "audio.pygame.mixer.Sound",
                       side_effect=lambda buffer: buffer):
            audio = AudioFeedback()

        self.assertEqual(
            set(audio.sounds),
            {"type", "invalid", "submit", "win", "lose"})
        self.assertTrue(all(audio.sounds.values()))

    def test_audio_failure_is_reported_without_stopping_the_game(self):
        with patch("audio.pygame.mixer.get_init", return_value=None), patch(
                "audio.pygame.mixer.init",
                side_effect=pygame.error("no audio device")):
            with patch("sys.stderr") as error_output:
                audio = AudioFeedback()

        self.assertEqual(audio.sounds, {})
        warning = "".join(
            call.args[0] for call in error_output.write.call_args_list)
        self.assertEqual(warning, "Audio disabled: no audio device\n")

    def test_word_lists_contain_five_letter_answers_and_guesses(self):
        answers = Wordle.load_word_list("wordlist.txt")
        guesses = set(Wordle.load_word_list("guess_words.txt"))

        self.assertGreater(len(guesses), 5000)
        self.assertTrue(all(len(word) == 5 and word.isalpha()
                            for word in answers))
        self.assertTrue(set(answers).issubset(guesses))
        self.assertIn("FIBRE", guesses)
        self.assertNotIn("FIBER", guesses)
        self.assertIn("MOULD", guesses)
        self.assertNotIn("MOLD", guesses)


if __name__ == "__main__":
    unittest.main()
