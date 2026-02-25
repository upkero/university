from __future__ import annotations

import math
import random
import struct
import wave
from pathlib import Path

import pygame

from .utils import resolve_path


def write_wave(path: Path, samples: list[float], sample_rate: int = 44100) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames = bytearray()
    for s in samples:
        s = max(-1.0, min(1.0, s))
        frames += struct.pack("<h", int(s * 32767))
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(frames)


def tone(freq: float, duration: float, volume: float, sample_rate: int = 44100) -> list[float]:
    total = int(duration * sample_rate)
    return [math.sin(2 * math.pi * freq * i / sample_rate) * volume for i in range(total)]


def noise(duration: float, volume: float, sample_rate: int = 44100) -> list[float]:
    total = int(duration * sample_rate)
    rng = random.Random(0)
    return [(rng.random() * 2 - 1) * volume for _ in range(total)]


def sequence_tones(tones: list[tuple[float, float]], volume: float) -> list[float]:
    samples: list[float] = []
    for freq, dur in tones:
        samples.extend(tone(freq, dur, volume))
    return samples


def generate_music(duration: float = 6.0, sample_rate: int = 44100) -> list[float]:
    total = int(duration * sample_rate)
    freqs = [261.63, 329.63, 392.0]
    samples: list[float] = []
    for i in range(total):
        t = i / sample_rate
        v = sum(math.sin(2 * math.pi * f * t) for f in freqs) / len(freqs)
        env = 0.5 * (1 - math.cos(2 * math.pi * (i / total)))
        samples.append(v * 0.18 * env)
    return samples


def ensure_sound_files(cfg: dict, base_dir: Path) -> None:
    sounds = cfg.get("sounds", {})
    targets = {
        "reveal": (sounds.get("reveal"), tone(880, 0.08, 0.35)),
        "flag": (sounds.get("flag"), tone(660, 0.06, 0.35)),
        "boom": (sounds.get("boom"), noise(0.25, 0.5)),
        "win": (sounds.get("win"), sequence_tones([(523, 0.12), (659, 0.12), (784, 0.2)], 0.4)),
        "lose": (sounds.get("lose"), sequence_tones([(392, 0.14), (330, 0.14), (262, 0.18)], 0.4)),
        "music": (sounds.get("music"), generate_music()),
    }
    for _, (path_str, samples) in targets.items():
        if not path_str:
            continue
        path = resolve_path(path_str, base_dir)
        if not path.exists():
            write_wave(path, samples)


class AudioManager:
    def __init__(self, cfg: dict, base_dir: Path) -> None:
        self.enabled = False
        self.sfx: dict[str, pygame.mixer.Sound] = {}
        self._init_audio(cfg, base_dir)

    def _init_audio(self, cfg: dict, base_dir: Path) -> None:
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1)
        except pygame.error:
            self.enabled = False
            return
        self.enabled = True

        sounds_cfg = cfg.get("sounds", {})
        for key in ("reveal", "flag", "boom", "win", "lose"):
            path_str = sounds_cfg.get(key)
            if not path_str:
                continue
            path = resolve_path(path_str, base_dir)
            if path.exists():
                try:
                    self.sfx[key] = pygame.mixer.Sound(str(path))
                except pygame.error:
                    pass
        music_path = sounds_cfg.get("music")
        if music_path:
            path = resolve_path(music_path, base_dir)
            if path.exists():
                try:
                    pygame.mixer.music.load(str(path))
                    pygame.mixer.music.set_volume(0.35)
                    pygame.mixer.music.play(-1)
                except pygame.error:
                    pass

    def play(self, key: str) -> None:
        if not self.enabled:
            return
        sound = self.sfx.get(key)
        if sound:
            sound.play()
