# AniSub (alpha ver.)

A tool for processing anime subtitles.  
It takes an `mkv` file as input, processes the subtitles and adds an additional subtitles track.

## Usage
### GUI
`anisub`  
### CLI
`anisub --ignore-gooey <file.mkv>`  
For more options: `anisub --ignore-gooey -h`  

## Features:
### Character name order
Change character names order (western <-> eastern).  
i.e. Naruto Uzumako <-> Uzumaki Naruto.
  
How it's done:
* Automatically detects the anime name (you can also supply it yourself if it fails to detect)
* Fetches all known characters from [myanimelist] (new sources can be easily added)
* Switches the name order.


[myanimelist]: https://myanimelist.net/
