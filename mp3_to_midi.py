#!/usr/bin/env python3
"""
MP3 to MIDI Transcription Tool
Converts an MP3 file to MIDI, extracts notes with timing, and displays piano keys.
"""

from __future__ import annotations

import sys
import os
from pathlib import Path
from typing import Optional, List, Dict

from basic_pitch.inference import predict
import pretty_midi


SOLFEGE = {
    "C": "Do", "D": "Ré", "E": "Mi", "F": "Fa",
    "G": "Sol", "A": "La", "B": "Si",
}


def mp3_to_midi(mp3_path: str, output_midi_path: str | None = None) -> str:
    """Convert an MP3 file to MIDI using basic-pitch.

    Args:
        mp3_path: Path to the input MP3 file.
        output_midi_path: Optional path for the output MIDI file.
            Defaults to the same name with a .mid extension.

    Returns:
        Path to the generated MIDI file.
    """
    mp3_path = Path(mp3_path)
    if not mp3_path.exists():
        raise FileNotFoundError(f"File not found: {mp3_path}")

    if output_midi_path is None:
        output_midi_path = mp3_path.with_suffix(".mid")
    else:
        output_midi_path = Path(output_midi_path)

    print(f"Transcribing '{mp3_path.name}' ...")
    model_output, midi_data, note_events = predict(str(mp3_path))

    midi_data.write(str(output_midi_path))
    print(f"MIDI saved to '{output_midi_path}'")

    return str(output_midi_path)


def midi_note_to_name(midi_number: int) -> dict:
    """Convert a MIDI note number to note name info.

    Args:
        midi_number: MIDI note number (0-127).

    Returns:
        Dict with English name, French name, octave, and whether it's a sharp.
    """
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = (midi_number // 12) - 1
    note_index = midi_number % 12
    english = note_names[note_index]

    base = english.replace("#", "")
    is_sharp = "#" in english
    french = SOLFEGE[base] + ("#" if is_sharp else "")

    return {
        "english": english,
        "french": french,
        "octave": octave,
        "is_sharp": is_sharp,
    }


def extract_notes(midi_path: str) -> list[dict]:
    """Extract all notes from a MIDI file with timing information.

    Args:
        midi_path: Path to the MIDI file.

    Returns:
        List of dicts sorted by start time, each containing:
        - name_en: English note name (e.g. "C4")
        - name_fr: French note name (e.g. "Do4")
        - midi_number: MIDI note number
        - start: Start time in seconds
        - duration: Duration in seconds
        - velocity: Note velocity (0-127)
    """
    midi = pretty_midi.PrettyMIDI(str(midi_path))
    notes = []

    for instrument in midi.instruments:
        for note in instrument.notes:
            info = midi_note_to_name(note.pitch)
            notes.append({
                "name_en": f"{info['english']}{info['octave']}",
                "name_fr": f"{info['french']}{info['octave']}",
                "midi_number": note.pitch,
                "start": round(note.start, 3),
                "duration": round(note.end - note.start, 3),
                "velocity": note.velocity,
                "is_sharp": info["is_sharp"],
            })

    notes.sort(key=lambda n: (n["start"], n["midi_number"]))
    return notes


def display_notes(notes: list[dict]) -> None:
    """Display extracted notes in a readable table format."""
    if not notes:
        print("No notes found.")
        return

    print(f"\n{'='*70}")
    print(f"{'Time':>8s}  {'Duration':>8s}  {'Note (EN)':>10s}  {'Note (FR)':>10s}  {'MIDI#':>5s}  {'Vel':>3s}")
    print(f"{'-'*70}")

    for n in notes:
        marker = " #" if n["is_sharp"] else "  "
        print(
            f"{n['start']:8.3f}s  "
            f"{n['duration']:8.3f}s  "
            f"{n['name_en']:>10s}  "
            f"{n['name_fr']:>10s}  "
            f"{n['midi_number']:5d}  "
            f"{n['velocity']:3d}{marker}"
        )

    print(f"{'='*70}")
    print(f"Total notes: {len(notes)}")


def display_piano_roll(notes: list[dict], time_step: float = 0.5) -> None:
    """Display a simple text-based piano roll showing notes over time.

    Args:
        notes: List of note dicts from extract_notes().
        time_step: Time resolution in seconds for each row.
    """
    if not notes:
        return

    max_time = max(n["start"] + n["duration"] for n in notes)
    print(f"\nPiano Roll (step={time_step}s):")
    print(f"{'-'*60}")

    t = 0.0
    while t <= max_time:
        active = [
            n for n in notes
            if n["start"] <= t < n["start"] + n["duration"]
        ]
        if active:
            names = ", ".join(n["name_fr"] for n in active)
            print(f"  {t:7.2f}s | {names}")
        t += time_step

    print(f"{'-'*60}")


def process(mp3_path: str, output_midi: str | None = None) -> list[dict]:
    """Full pipeline: MP3 -> MIDI -> note extraction -> display.

    Args:
        mp3_path: Path to the input MP3 file.
        output_midi: Optional path for the MIDI output.

    Returns:
        List of extracted note dicts.
    """
    midi_path = mp3_to_midi(mp3_path, output_midi)
    notes = extract_notes(midi_path)
    display_notes(notes)
    display_piano_roll(notes)
    return notes


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <input.mp3> [output.mid]")
        sys.exit(1)

    mp3_file = sys.argv[1]
    midi_output = sys.argv[2] if len(sys.argv) > 2 else None
    process(mp3_file, midi_output)
