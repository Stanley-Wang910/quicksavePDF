import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer
import os
import argparse

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, watch_dir, debounce=5, pause_duration=30):
        self.watch_dir = watch_dir
        self.timer = None
        self.debounce = debounce  # seconds
        self.pause_duration = pause_duration
        self.is_paused = False
        print("Initializing FileChangeHandler...")

    def on_modified(self, event):
        print(f'{event.src_path} has been modified.')
        if self.is_paused:
            print("Currently paused.")
            return

        file_name = os.path.basename(event.src_path)
        if file_name.endswith('.docx'): # and ('Resume' in file_name or 'CV' in file_name)
            print(f'File {event.src_path} matches criteria.')
            if self.timer:
                self.timer.cancel()
            self.timer = Timer(self.debounce, self.convert_to_pdf, args=(event.src_path,))
            self.timer.start()
        else:
            print(f'File {event.src_path} does not match criteria. Ignoring...')

    def convert_to_pdf(self, docx_path):
        print(f'Converting {docx_path} to PDF...')
        subprocess.run(['python', 'quicksave.py', docx_path])
        print(f'Converted {docx_path} to PDF.')

        self.is_paused = True
        print(f'Pausing for {self.pause_duration} seconds...')
        time.sleep(self.pause_duration)
        self.is_paused = False
        print('Resuming...')
        
def watch_files(watch_dir, watch_duration):
    event_handler = FileChangeHandler(watch_dir)
    observer = Observer()
    observer.schedule(event_handler, path=watch_dir, recursive=False)
    observer.start()
    print(f'Watching {watch_dir} for changes for {watch_duration} seconds...')

    def stop_observer():
        observer.stop()
        print('Observer stopped due to timeout')

    stop_timer = Timer(watch_duration, stop_observer)
    stop_timer.start()

    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Watch a directory for changes and convert to PDF.')
    parser.add_argument('watch_dir', type=str, help='Directory to watch for .docx files')
    parser.add_argument('--watch_duration', type=int, default=3600, help='Duration to watch the directory (in seconds)')
    
    args = parser.parse_args()
    watch_dir = os.path.abspath(args.watch_dir)
    watch_duration = args.watch_duration
    
    watch_files(watch_dir, watch_duration)
