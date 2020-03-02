#!/usr/bin/python3

from urizen.core.feature import Feature

# Dungeon features

feature_blood_covered = type('feature_blood_covered', (Feature,), {
    'feature_type': None,
    'symbol': '*',
    'bg_color': '#000000',
    'fg_color': '#FF0000',
    'pixel_color': '#FF0000',
    'sprite': None,
    'tags': []
})
