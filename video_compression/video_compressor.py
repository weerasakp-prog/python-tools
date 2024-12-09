import subprocess
import os
from pathlib import Path
import json
import time

class VideoCompressor:
    """A class to handle video compression operations using ffmpeg."""
    
    def __init__(self):
        """Initialize the VideoCompressor."""
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv']
        
        # Check if ffmpeg is installed
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            print("Error: ffmpeg is not installed. Please install ffmpeg first.")
            print("On macOS, use: brew install ffmpeg")
            print("On Ubuntu/Debian: sudo apt install ffmpeg")
            print("On Windows, download from: https://ffmpeg.org/download.html")
    
    def get_video_files(self, folder_path):
        """Get all video files from the specified folder."""
        video_files = []
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path) and Path(file).suffix.lower() in self.supported_formats:
                video_files.append(file_path)
        return video_files
    
    def get_file_size_mb(self, file_path):
        """Get the file size in megabytes."""
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    
    def format_time(self, seconds):
        """Format time in seconds to hours:minutes:seconds."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def compress_video(self, input_path):
        """
        Compress a single video file with fast compression settings.
        Returns tuple of (success, details)
        """
        try:
            # Generate output path in the same folder with "_compressed" suffix
            input_path_obj = Path(input_path)
            output_path = input_path_obj.parent / f"{input_path_obj.stem}_compressed{input_path_obj.suffix}"
            
            # Fast compression settings
            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-c:v', 'libx264',
                '-preset', 'veryfast',  # Fast compression
                '-crf', '28',          # Slightly lower quality for smaller size
                '-c:a', 'aac',
                '-b:a', '128k',
                '-y',                  # Overwrite output file if exists
                str(output_path)
            ]
            
            # Execute FFmpeg command
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                return False, f"Error: {process.stderr}"
            
            # Get compression results
            original_size = self.get_file_size_mb(input_path)
            compressed_size = self.get_file_size_mb(output_path)
            reduction = ((original_size - compressed_size) / original_size * 100)
            
            details = {
                'original_size': original_size,
                'compressed_size': compressed_size,
                'reduction': reduction
            }
            
            return True, details
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def batch_compress(self, input_folder):
        """
        Compress all videos in the input folder using fast compression.
        """
        # Validate input folder
        if not os.path.exists(input_folder):
            print(f"Error: Folder '{input_folder}' does not exist")
            return
        
        # Get all video files
        video_files = self.get_video_files(input_folder)
        
        if not video_files:
            print(f"No supported video files found in '{input_folder}'")
            return
        
        print(f"\nFound {len(video_files)} video files to compress")
        print("Starting batch compression...")
        print("=" * 50)
        
        # Statistics
        total_original_size = 0
        total_compressed_size = 0
        successful_compressions = 0
        failed_compressions = 0
        start_time = time.time()
        
        # Process each video
        for index, video_file in enumerate(video_files, 1):
            file_name = os.path.basename(video_file)
            print(f"\nProcessing ({index}/{len(video_files)}): {file_name}")
            
            success, details = self.compress_video(video_file)
            
            if success:
                successful_compressions += 1
                total_original_size += details['original_size']
                total_compressed_size += details['compressed_size']
                
                print(f"✓ Compressed successfully:")
                print(f"  Original size: {details['original_size']:.2f} MB")
                print(f"  Compressed size: {details['compressed_size']:.2f} MB")
                print(f"  Reduction: {details['reduction']:.1f}%")
            else:
                failed_compressions += 1
                print(f"✗ Failed to compress: {details}")
        
        # Print summary
        elapsed_time = time.time() - start_time
        print("\n" + "=" * 50)
        print("Compression Summary:")
        print(f"Total videos processed: {len(video_files)}")
        print(f"Successful compressions: {successful_compressions}")
        print(f"Failed compressions: {failed_compressions}")
        if successful_compressions > 0:
            print(f"Total original size: {total_original_size:.2f} MB")
            print(f"Total compressed size: {total_compressed_size:.2f} MB")
            print(f"Overall reduction: {((total_original_size - total_compressed_size) / total_original_size * 100):.1f}%")
        print(f"Total time: {self.format_time(elapsed_time)}")
        print("=" * 50)

def main():
    """Main function to run the batch video compression."""
    compressor = VideoCompressor()
    
    # Get input folder from user
    input_folder = input("Enter the path to the folder containing videos: ").strip()
    
    # Remove quotes if the user copied a path with quotes
    input_folder = input_folder.strip('"\'')
    
    # Start batch compression
    compressor.batch_compress(input_folder)

if __name__ == "__main__":
    main()