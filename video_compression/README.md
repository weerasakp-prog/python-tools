# Video Compression Tool

This tool provides a simple way to compress multiple video files in a folder using FFmpeg. It uses fast compression settings to reduce file sizes while maintaining reasonable quality.

## Prerequisites

1. Python 3.x installed on your system
2. FFmpeg installed on your system

### Installing FFmpeg

- **macOS** (using Homebrew):
  ```bash
  brew install ffmpeg
  ```

- **Ubuntu/Debian**:
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

- **Windows**:
  1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
  2. Extract the downloaded file
  3. Add the FFmpeg `bin` folder to your system's PATH environment variable

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/weerasakp-prog/python-tools.git
   ```

2. Navigate to the video compression directory:
   ```bash
   cd python-tools/video_compression
   ```

## Usage

1. Run the script:
   ```bash
   python video_compressor.py
   ```

2. When prompted, enter the full path to the folder containing your videos.

3. The script will:
   - Scan the folder for supported video files (.mp4, .avi, .mov, .mkv)
   - Compress each video using fast compression settings
   - Save compressed videos in the same folder with '_compressed' suffix
   - Show progress and results for each file
   - Display a summary when complete

## Features

- Batch processing of multiple videos
- Fast compression preset for quick processing
- Maintains original files
- Supports multiple video formats
- Detailed progress and summary information
- Error handling for each video

## Output

The tool will create compressed versions of your videos in the same folder:
```
input_folder/
    ├── video1.mp4
    ├── video1_compressed.mp4
    ├── video2.mp4
    ├── video2_compressed.mp4
    └── ...
```

## Compression Settings

The tool uses the following FFmpeg settings:
- Codec: H.264
- Preset: veryfast (for quick compression)
- CRF: 28 (balance between quality and file size)
- Audio: AAC 128k

## Error Handling

- The tool will skip unsupported file formats
- Each video is processed independently
- Failed compressions won't stop the batch process
- Detailed error messages are provided

## Notes

- Original files are preserved
- Compressed files are created with '_compressed' suffix
- Processing time depends on video size and hardware
- Make sure you have enough disk space for compressed files