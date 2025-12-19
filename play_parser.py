"""
Author: Anna Monaghan
Course: Artificial Intelligence CSCI 2400
Assignment: Final Project
Date: 12/19/2025

Description: Parses each file passed to it into json objects to be stored in the data file. Each json object contains the text from each line in the play, along with tags for its play of origin, act and scene numbers, and speaker.
Known Bugs: None
"""
import re

class Parser:
    """
    Represents a Parser object for play files.

    Attributes: play_id - the name of the play currently being parsed.
                    act - the act number for the current lines to be tagged under.
                    scene - the scene number for the current lines to be tagged under.
                    speaker - the speaker name for the current lines to be tagged under.
                    lines - the list of lines in the current speaker's speech.
                    object - the full block to be added to the data file, with text and
                    tags included.
    """
    ACT_RE = re.compile(r"^\s*ACT\s+(\d+)\s*$") # For act number tags.
    SCENE_RE = re.compile(r"^\s*Scene\s+(\d+)\s*$") # For scene number tags.
    UNDERLINE_RE = re.compile(r"^\s*[=\-]{3,}\s*$")
    SPEAKER_RE = re.compile(r"^\s*([A-Z][A-Z\s'\-]+?)(?:\s{2,}(.*))?\s*$") # For speaker tags.
    STAGE_RE = re.compile(r"^\s*\[.*\]\s*$") # For stage directions.

    def __init__(self, play_id):
        """
        Initialize a Parser class.
        
        Args: play_id - the name of the play file in which the line to be loaded was said.
        Returns: None
        """
        self.play_id = play_id
        self.act = None
        self.scene = None
        self.speaker = None
        self.lines = []
        self.object = []


    def _clear(self):
        """DOCSTRING"""
        if self.speaker is not None and self.lines:
            text = "\n".join(self.lines).strip()
            if text:
                self.object.append({
                    "play_id" : self.play_id,
                    "act" : self.act,
                    "scene" : self.scene,
                    "speaker" : self.speaker,
                    "text" : text
                })
        
        self.speaker = None
        self.lines = []


    def parse_line(self, line):
        """DOCSTRING"""
        line = line.rstrip()

        matches = self.ACT_RE.match(line)
        if matches:
            self._clear()
            self.act = int(matches.group(1))
            self.scene = None
            return
        
        matches = self.SCENE_RE.match(line)
        if matches:
            self._clear()
            self.scene = int(matches.group(1))
            return
        
        if (
            self.UNDERLINE_RE.match(line)
            or self.STAGE_RE.match(line)
            or self.act is None
            or self.scene is None
        ):
            return
        
        if not line.strip():
            if self.speaker is not None and self.lines:
                self._clear()
            return
        
        matches = self.SPEAKER_RE.match(line)
        if matches:
            name = matches.group(1).strip()
            remainder = (matches.group(2) or "").rstrip()

            if name == name.upper():
                self._clear()
                self.speaker = name
                if remainder:
                    self.lines.append(remainder)
                return
        
        if self.speaker is not None:
            self.lines.append(line)


    def parse_file(self, path):
        """DOCSTRING"""
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            self.parse_line(line)

        self._clear()
        return self.object
