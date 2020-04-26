#!/usr/bin/python3

from urizen.core.actor import Actor


actor_player_default_male = type('actor_player_default_male', (Actor,), {
    'actor_type': 'player',
})

actor_player_default_female = type('actor_player_default_female', (Actor,), {
    'actor_type': 'player',
})