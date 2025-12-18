import re

class Parser:
    """
    Docstring for Parser
    """
    ACT_RE = re.compile(r"^\s*ACT\s+(\d+)\s*$") # For act number tags.
    SCENE_RE = re.compile(r"^\s*Scene\s+(\d+)\s*$") # For scene number tags.
    UNDERLINE_RE = re.compile(r"^\s*[=\-]{3,}\s*$")
    SPEAKER_RE = re.compile(r"^\s*([A-Z][A-Z\s'\-]+?)(?:\s{2,}(.*))?\s*$") # For speaker tags.
    STAGE_RE = re.compile(r"^\s*\[.*\]\s*$") # For stage directions.

    def __init__(self, play_id):
        """
        Initialize a Parser class.
        
        Attributes: play_id - the name of the play currently being parsed.
                    act - the act number for the current lines to be tagged under.
                    scene - the scene number for the current lines to be tagged under.
                    speaker - the speaker name for the current lines to be tagged under.
                    lines - the list of lines in the current speaker's speech.
                    object - the full block to be added to the data file, with text and
                    tags included.
        """
        self.play_id = play_id
        self.act = None
        self.scene = None
        self.speaker = None
        self.lines = []
        self.object = []


    def clear(self):
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
            self.clear()
            self.act = int(matches.group(1))
            self.scene = None
            return
        
        matches = self.SCENE_RE.match(line)
        if matches:
            self.clear()
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
                self.clear()
            return
        
        matches = self.SPEAKER_RE.match(line)
        if matches:
            name = matches.group(1).strip()
            remainder = (matches.group(2) or "").rstrip()

            if name == name.upper():
                self.clear()
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

        self.clear()
        return self.object
