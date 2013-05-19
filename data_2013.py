#!/usr/bin/env python2

from scantron import ScantronField

data = [
    ScantronField('auton_high', 'Auton High', int),
    ScantronField('auton_mid', 'Auton Mid', int),
    ScantronField('auton_low', 'Auton Low', int),
    ScantronField('high', 'High', int),
    ScantronField('mid', 'Mid', int),
    ScantronField('low', 'Low', int),
    ScantronField('pyramid', 'Pyramid', int),
    ScantronField('missed', 'Missed', int),
    ScantronField('fouls', 'Fouls', int),
    ScantronField('tech_fouls', 'Tech fouls', int),
    ScantronField('defense', 'Defense', bool),
    ScantronField('pickup', 'Pickup', bool),
    ScantronField('noshow', 'Noshow', bool),
    ScantronField('brokedown', 'Brokedown', bool),
    ScantronField('dq', 'DQ', bool),
]
