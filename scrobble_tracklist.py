#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lastpy as lp
import sys
import time
import progressbar as pb

print('Please make sure the tracklist has been formatted by the following rules:')
print('    - All fields are separated by a tab character')
print('    - First line has the fields: Tracklist artist, tracklist name')
print('    - All subsequent lines have: Time, artist, track name')
print('    - Until last.fm supports multiple artists on a track, only one artist per track')
print('    - Don\'t worry too much about feat./ft./whatever, they\'re all inconsistent anyway')
print('    - For mashups, keep both artist names in the artist fields, e.g. X vs. Y')
print('        - Make sure the mashuper is in the track title (e.g. X vs. Y - Z (A mashup))')
print('')

tl_fname = sys.argv[1]
key='lir9n1GGzrtR5pRbNSXM88dZUfkaC6Y-'

def get_sec(s):
    parts = s.split(':')
    if len(parts) == 1:
        return int(parts[0])
    elif len(parts) == 2:
        return int(parts[0])*60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0])*60*60 + int(parts[1])*60 + int(parts[2])

def t_str(t):
    t_min = t // 60
    t_sec = t % 60
    return '%02d:%02d' % (t_min, t_sec)

with open(tl_fname) as f:
    first_line = f.readline()[:-1]
    first_line = first_line.split('\t')
    tl_artist = first_line[0]
    tl_name = first_line[1]

    print('You are listening to {} by {}'.format(tl_name, tl_artist))

    n = 0
    for line in f:
        if line[0] != '#':
            line = line[:-1].split('\t')

            t = get_sec(line[0])
            artist = line[1]
            track = line[2]

            if n > 0:
                t_track = t - last_t
                with pb.ProgressBar(
                    max_value=t_track,
                    suffix='{variables.time} / ' + t_str(t_track),
                    variables={'time': t_str(0)},
                    widgets=[pb.widgets.Bar(marker=pb.widgets.AnimatedMarker(markers='|', fill='-'), left='{} - {} |'.format(last_artist, last_track), right='| ')]
                ) as bar:
                    for i in range(t_track-1):
                        bar.update(i, time=t_str(i))
                        time.sleep(1)

                if last_track != '-':
                    lp.scrobble(last_track, last_artist, tl_name, tl_artist, key)
                else:
                    exit()

            n += 1

            #print('Now playing: {} - {}'.format(artist, track))

            lp.nowPlaying(track, artist, tl_name, tl_artist, key)
            last_artist = artist
            last_track = track
            last_t = t

    #time.sleep(t-last_t)
    #lp.scrobble(last_track, last_artist, tl_name, tl_artist, key)
