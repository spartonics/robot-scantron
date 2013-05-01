#!/usr/bin/env python2

from scantron import *

data = [
    Field('auton_high', 'Auton High', int),
    Field('auton_mid', 'Auton Mid', int),
    Field('auton_low', 'Auton Low', int),
    Field('high', 'High', int),
    Field('mid', 'Mid', int),
    Field('low', 'Low', int),
    Field('pyramid', 'Pyramid', int),
    Field('missed', 'Missed', int),
    Field('fouls', 'Fouls', int),
    Field('tech_fouls', 'Tech fouls', int),
    Field('defense', 'Defense', bool),
    Field('pickup', 'Pickup', bool),
    Field('noshow', 'Noshow', bool),
    Field('brokedown', 'Brokedown', bool),
    Field('dq', 'DQ', bool),
]

st = Scantron('form.pdf', spacing=0.5)
st.populate(data)
st.save()
