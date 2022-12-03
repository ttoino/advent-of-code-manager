# AOC Manager

Hi! This is a CLI that I use to manage my [Advent of Code](https://adventofcode.com) repositories.

It's mostly for personal use and not at all polished.

## Installation

As this is mostly for personal use, and I like always having the most recent version available, I just clone the repository (`git clone https://github.com/ttoino/advent-of-code-manager.git`) and then add an alias to the `main.py` file (`alias aocm='<path/to/this/repo>/main.py'`).

## Usage

Usage can be seen with `aocm -h`.
Options are taken from a `.aocm` file in the working directory, but can be overwritten with flags.
The program must always be ran from the top level directory of the repo (i.e. the one where the folders for each day are).

The session cookie and year are required for most functionalities.

## Functionalities

- `aocm init`

  Sets up a directory so its able to hold an advent of code repository.
  Copies all the template files, fills the README with the available information, and creates a folder for each available day.

- `aocm update`

  Updates the README file with the available information.

- `aocm events`

  Shows all the available events.

- `aocm progress`

  Shows your calendar progress for the current event.

- `aocm submit [day] [part]`

  Runs the program for the desired day and part and submits the result, updating the README with the progress.

- `aocm test [day] [part]`

  Runs the program for the desired day and part.

- `aocm get [day]`

  Creates a folder for the desired day.

## TODO

- Multiple programming language support
- Customizable templates
