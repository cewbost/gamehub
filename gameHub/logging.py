"""Logging for gameHub backend.
    
    Currently all messages are written to stderr when settings.DEBUG==True, and
    also to a rotating log file, specified by the LOG_FILE environment variable.
    
    The log messages are stored with date, time, message level, and the sender module,
    separated by tabs.
    
    The raw logs can be quite difficult to read, so it's recommended to have some kind
    of reader program that can filter the messages. There is a simple python script
    called rlog which has been added to the repository just for convenience. It's a
    bit wonky, but it's capable of reading and filtering the logs, so what more can
    you want? Run 'python rlog.py -h' for help.
"""

import logging
from logging import StreamHandler, Formatter

from django.utils import timezone

def reverseEscape(string):
    """
    Replaces newline and tab with their escape sequences, and isolates '\\' in an
    escape sequence.
    """
    return string.replace('\\', '<%\\%>').replace('\n', '\\n').replace('\t', '\\t').replace('<%', '<%<%><%%%>').replace('%>', '<%%%><%>%>')

class SingleLineFormatter(Formatter):
    """
    Standard compliant formatter for formatting a single line in the log files.
  
    Formats any log message onto a single line, along with timestamp, logging level
    and name of the logger, separated by tab.
    """
    
    def __init__(self, fmt=None, datefmt=None, style='%'):
        self.datefmt = datefmt
        super(SingleLineFormatter, self).__init__(fmt, datefmt, style)
  
    def format(self, record):
        msg = super(SingleLineFormatter, self).format(record)
        time = super(SingleLineFormatter, self).formatTime(record, self.datefmt)
        return '{0}\t{1}\t{2}\t{3}'.format(
            time,
            record.levelno,
            record.name,
            reverseEscape(msg)
        )
  
    def formatException(self, exc_info):
        msg = super(SingleLineFormatter, self).formatException(exc_info)
        return msg
  
    def formatStack(self, stack_info):
        msg = super(SingleLineFormatter, self).formatStack(stack_info)
        return msg

class ColoredStreamHandler(StreamHandler):
    """A stream handler that colors the output.
    
    The color scheme is:
        DEBUG: blue
        INFO: green
        WARNING: yellow
        ERROR: red
        CRITICAL: bold purple
    """
    
    color_scheme = None
    color_terminator = None
    
    def __init__(self, colors, stream=None, color_end='\033[0m'):
        self.color_scheme = colors
        self.color_terminator = color_end
        super(ColoredStreamHandler, self).__init__(stream)
    
    def emit(self, record):
        try:
            msg = self.format(record)
            if record.levelname in self.color_scheme:
                msg = self.color_scheme[record.levelname] + msg + self.color_terminator
            stream = self.stream
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except:
            self.handleError(record)
