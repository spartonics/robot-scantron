robot-scantron
==============

Helpers for generating, scanning, and parsing scantron PDFs.

The code is tailored for FRC scouting. It can be adapted for other things, but
at the moment there are some hard-coded things

Intent
------

This project is intended to replace Spartonic's current scantron generation
and scanning programs. We are aiming to satisfy the following goals:

 * Unified application/library to generate and parse the scantrons
 * Cross-platform code so that anyone can run this for competitions
 * Easy hooks to do further things with the parsed scantrons
 
For Spartonics, this data will be used to make more informed decisions during
matches and alliance selections.

Status
------

Unfortunately, this project is still in its infancy. The majority of things
are not yet working. The intent is to finish this for the 2014 FRC season.
