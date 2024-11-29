# Vimposer

Vimposer is a hackable, keyboard-controlled terminal MIDI editor. Essentially, its goal is to be Vim, but for music.

This repository is a demo version - it will require much refactoring to perform at an adequate speed, but it is usable.

If you have questions or would like to contribute to this project, email me at lewis.thornberry@christendom.edu.

## Installation
```
sudo apt install fluidsynth
git clone https://github.com/joeythornberry/vimposer-py
cd vimposer-py
```

## Usage
```
./pose new.mid
```

## Controls (can be edited in config/config.py)
`A`,`F`,`S`,`D` : Create a new note before, after, above, or below the cursor note

`a`,`f`,`s`,`d` : Move the cursor to a different note

`h`,`l`,`j`,`k` : Move the current cursor note

`H`,`L`,`J`,`K` : Move the viewport

`i` : Make the cursor note shorter

`o` : Make the cursor note longer

`x` : Delete the cursor note

_If the above commands follow a number, they will be performed that number of times: for example, `5o` will lengthen the current note by 5 divisions._

`W` : Save

`Q` : Quit (remember to save first)

`<Space>` : Start playback (remember to save first)

`<Esc>` : Stop playback and reset current command

`tn` : Create a new track

`tj`, `tk` : Change the current track

`tx` : Delete the current track

`<number>I` : Set the MIDI instrument of the current track to `<number>`

`<number>V` : Set the velocity of the current track to `<number>`

`<number>T` : Set the tempo of the MIDI file to `<number>`

## Soundfonts
This project uses Fluidsynth to play MIDI sounds. Fluidsynth relies on Soundfont files, which provide sets of instruments for Fluidsynth to use. Vimposer will use the Soundfont stored in the "soundfont" file. The current default Soundfont is the Roland SC-55.
