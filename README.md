# olto3d - Automatische Digitalisierung von OL-Karten
Converting a orienteering sprint map into 3d (Collada .dae) format

## Setup

* install **pyenv**:
* -> **Linux (apt):** `apt-get install pyenv`
* -> **macOS (Homebrew)** `brew install pyenv `
* `cd [repository (olto3d)]"`
* `pyenv init`
* `pyenv install 3.7.2`
* `pyenv local  3.7.2`
* `python -m pip install pipenv`
* `pipenv install`
* `pipenv run "python file"` / `pipenv shell` -> `python "python file"`
* `pipenv shell`
* `python -m ipykernel install --user --name=olto3d`

## Run
### Run jupyter notebook
* `cd [repository (olto3d)]"`
* `pipenv shell`
* `jupyter notebook` then select src/mapDigitalisation.ipynb then `olto3d` kernel
### Run olto3d
* `cd src`
* `pipenv run python olto3d [numberOfCheckpoints] [input.jpg] [output.dae]`
* Example: `pipenv run python olto3d.py 6 ../ressources/maps/map1.jpg ../output/output.dae`

## Display Collada files

* Download GLC-Viewer (MacOS, Linux, Windows support) from http://www.glc-player.net/