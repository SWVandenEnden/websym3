# Graphical interface Symbolic Expression 3

A graphical (web) user interface to the Python module Symbolic Expression 3 (symexpress3)

## Installation
Download of make a git clone of WebSym3
```
git clone https://github.com/SWVandenEnden/websym3.git
```
Go to the project root directory and update or install dependencies: 
``` 
pip install -r requirements.txt
```

## Usage
Start graphical user interface
```
python websym3.py
```
This start the default browser and open the local web page http://localhost:8003/math/index.html

### Configuration file
The websym3.ini in the same directory as websym3.py will be used as a configuration file.
Syntax:
```
[Path]
data=<directory>         # Directory user data, default <root>/data
javascript=<directory>   # Directory javascript files, default <root>/javascript
style=<directory>        # Directory css style files, default <root>/style
template=<directory>     # Directory template files, default <root>/template
[Server]
port=<number>            # Port number web server, default 8003
[Start]
url=<url>                # Automatic open url, default http://localhost:{port}/math/index.html
autoopenurl=<True/False> # Enable or disable automatic start url, default True
```

### Command line
To see all the command line options (help)
```
python websym3.py -h
```
