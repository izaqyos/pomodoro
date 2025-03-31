# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2024-03-XX

### Changed
- Simplified project structure by removing nested pomodoro directory
- Streamlined conda environment activation script
- Updated README with comprehensive Pomodoro technique explanation
- Improved task management documentation
- Fixed Python module import issues

### Added
- Quick start guide in README
- Detailed task management instructions
- Project screenshot in documentation
- Better development setup instructions

### Fixed
- Module import errors with proper package structure
- Conda environment activation issues
- Documentation structure and clarity
- Package installation process

## [1.1.0] - 2024-03-XX

### Added
- Task management system
  - Create new tasks with name, description, and due date
  - Mark tasks as complete/incomplete
  - Delete tasks
  - Expandable task details
  - Due date tracking with visual indicators
- Improved layout with three-column design
- Task creation form with validation
- Date picker for task due dates
- Visual indicators for task status
- Task detail expansion panels

### Changed
- Updated UI layout to accommodate task management
- Improved visual organization with three-column layout
- Enhanced user feedback for task operations

## [1.0.0] - 2024-03-XX

### Added
- Initial release of Pomodoro Timer
- Streamlit-based user interface
- Real-time date and time display
- Configurable work duration
- Visual progress tracking
- Session completion notifications
- Session statistics in sidebar
- Auto-refresh functionality
- Basic notification system
- Timer controls (Start/Pause, Reset)
- Progress bar for visual feedback
- Celebration animation on completion

### Changed
- Migrated from PyQt6 to Streamlit for better user experience
- Restructured project for better maintainability

### Technical Details
- Implemented session state management
- Added proper package structure
- Created conda environment setup
- Added basic test suite
- Configured development tools (pytest, black, isort)

## [Unreleased]

### Added
- **Real-time Clock**: Added a live clock display (HH:MM:SS) that updates every second
  - Displays the current time with seconds below the date
  - Styled to match the application's design
  - Updates automatically without page refresh

### Changed
- **Improved Timer Format**: Updated the timer to show hours, minutes, and seconds (HH:MM:SS) instead of just minutes and seconds
- **Enhanced Clock Initialization**: Clock now displays the current server time immediately before JavaScript takes over
- **Real-time Timer Updates**: Fixed issue with frozen seconds by implementing JavaScript-based real-time timer updates that don't require page reloads
- **Enhanced Timer Reliability**: Improved timer functionality with persistent window-based variables and better event handling
- **Synchronized Clock and Timer**: Unified the clock and timer JavaScript implementations to ensure consistent updates
- **Improved Element Handling**: Added robust DOM element checks and proper interval management for maximum reliability
- **Debug Information**: Added debug display showing timer status and remaining time for troubleshooting

## [1.1.0] - 2024-03-25

### Added
- **Watch Mode**: Added a watch mode feature that automatically reloads the application when code changes are detected
  - Support in shell script (`run_pomodoro.sh`) with `--watch` or `-w` flag
  - Support in batch file (`run_pomodoro.bat`) with `--watch` or `-w` flag
  - Added a new cross-platform Python script (`run_pomodoro.py`) with watch mode support
  - Updated documentation with watch mode usage examples
- **Custom App Selection**: All runner scripts now accept an optional app filepath parameter
- **Demo App**: Added `test_watch_mode.py` to demonstrate the watch mode feature
- **Debug Mode**: Added `--debug` or `-d` flag to Python runner script

### Changed
- Improved shell script and batch file to check conda environment properly
- Enhanced error handling in all runner scripts
- Updated README with comprehensive instructions for all platforms

## [0.5.0] - 2024-03-20

### Added
- Initial version of the Pomodoro Timer Application
- Basic timer functionality with work and break periods
- Simple task tracking system
- Statistics tracking for completed pomodoros
- Cross-platform support with shell script and batch file
- Conda environment management

### Changed
- First public release 