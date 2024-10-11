# Changelog

## [0.2.0] - 2024-10-11

### Added

- This changelog
- The number of steps and time it has taken to solve the level is now saved
- Now saves and loads the elapsed game time in the game save file
- A new menu has been added to select the level of the selected file, and under it is shown the time and steps in which it was completed, or the text "No score" if the selected level was not completed
- Added metadata to the startup script, new in [Pyxel 2.2.2](https://github.com/kitao/pyxel/blob/main/CHANGELOG.md#222)

### Changed

- The positions of several of the sprites have been changed so that they are all on the same line.
- Several variables have been declared for the game states
- Now when you select Start, the list of official levels is displayed directly. The Select file option was added, which shows if there are more files with levels in the folder levels

### Fixed

- Fixed not loading the number of steps when loading the game
- Fixed a problem when setting permissions for the saves folder

## [0.1.0] - 2024-09-27

### Changed

- First release

[0.2.0]: https://github.com/son-link/ticoban-pyxel/compare/v.0.1.0...v.0.2.0