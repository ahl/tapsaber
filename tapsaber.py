#!/usr/bin/env python

# BLINKA_FT232H=1

import time
import json
import miniaudio
import board
import digitalio
import sys


def main():
    white = digitalio.DigitalInOut(board.C1)
    black = digitalio.DigitalInOut(board.C0)
    black.direction = digitalio.Direction.OUTPUT
    black.value = True
    white.direction = digitalio.Direction.OUTPUT
    white.value = True

    def tap(v):
        tnext = time.time()
        value = False
        white.value = value
        value = not value
        time.sleep(0)
        for t in v:
            tnext += t / 1000
            while time.time() < tnext:
                pass
            white.value = value
            value = not value
            time.sleep(0)

    def left():
        tap([17.7 + 16.2, 2 + 0.05, 2, 2, 4, 2, 2, 2, 2])

    def right():
        tap([17.7 + 16.2, 2 + 0.05, 2, 2, 4, 2, 2, 2, 4])

    if len(sys.argv) != 2:
        print('Usage: %s <song dir>' % sys.argv[0], file=sys.stderr)
        sys.exit(2)

    song = sys.argv[1]

    print('starting...')

    infof = open(song + '/info.dat', 'r')
    info = json.loads(infof.read())

    bpm = info['_beatsPerMinute']

    sets = list(filter(lambda dbs:
                       dbs['_beatmapCharacteristicName'] == 'Standard',
                       info['_difficultyBeatmapSets']))
    beatmaps = sets[0]['_difficultyBeatmaps']
    beatmaps.sort(key=lambda beatmap: beatmap['_difficultyRank'], reverse=True)
    print(beatmaps[0]['_difficulty'])

    levelf = open(song + '/' + beatmaps[0]['_beatmapFilename'], 'r')
    level = json.loads(levelf.read())

    notes = level['_notes']
    notes.sort(key=lambda note: note['_time'])

    stream = miniaudio.stream_file(song + '/' + info['_songFilename'])
    device = miniaudio.PlaybackDevice()

    i = 0

    override = False
    cooldown = False

    device.start(stream)
    start = time.time()
    while i < len(notes):
        now = time.time()
        tapped = False
        while i < len(notes) and now >= start + 60 / bpm * notes[i]['_time']:
            lr = notes[i]['_type']
            tt = notes[i]['_time']
            i += 1
            if lr != 0 and lr != 1:
                continue
            print("%10.4f %10.4f %s %s" %
                  (time.time() - start, tt, lr, '*' if tapped else ' '))
            if not tapped or override:
                if lr == 0:
                    left()
                else:
                    right()
                if cooldown:
                    time.sleep(0.03)
                tapped = True
        time.sleep(0.001)
    # Let the song finish.
    time.sleep(1)
    device.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:
        raise
