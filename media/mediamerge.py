#!/usr/bin/env python3
"""
Simple FFmpeg wrapper to concatenate / merge multiple media files.
"""
import ffmpy
import tempfile
import argparse
import os.path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', help='files to read from (in order)')
    parser.add_argument('--output', '-o', nargs='?', help='sets the output file', default='output.mkv')
    args = parser.parse_args()

    with tempfile.NamedTemporaryFile(delete=False) as tempf:
        # Create a temporary file list in the format described here:
        # https://trac.ffmpeg.org/wiki/Concatenate#demuxer
        file_list = [("file '%s'" % os.path.abspath(f).replace("'", r"\'")).encode() for f in args.files]
        tempf.write(b'\n'.join(file_list))
        tempf.write(b'\n')
        tempf.close()  # close file so ffmpeg can read it

        print(tempf.name, args.output)
        ff = ffmpy.FFmpeg(inputs={tempf.name: '-f concat -safe 0 -auto_convert 1'},
                          outputs={args.output: '-c copy'})
        print("Will run command: %s" % ff.cmd)
        ff.run()
