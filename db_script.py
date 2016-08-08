# -*- coding: utf-8 -*-
"""
Created on Thu Aug 04 17:15:47 2016

@author: raoumer
"""

import sqlite3
import os

conn = sqlite3.connect('docclf.sqlite')
conn.text_factory = str
c = conn.cursor()
#c.execute('CREATE TABLE docclf_db(content TEXT, category INTEGER, date TEXT)')

example1 = "Hockey is a family of sports in which two teams play against each other by trying to maneuver a ball or a puck into the opponent's goal using a hockey stick. In many areas, one sport (typically field hockey or ice hockey) is generally referred to simply as hockey. Sport (UK) or sports (US) are all forms of usually competitive physical activity or games which,through casual or organised participation, aim to use, maintain or improve physical ability and skills while providing enjoyment to participants, and in some cases, entertainment for spectators.Usually the contest or game is between two sides, each attempting to exceed the other. Some sports allow a tie game; others provide tie-breaking methods, to ensure one winner and one loser. A number of such two-sided contests may be arranged in a tournament producing a champion. Many sports leagues make an annual champion by arranging games in a regular sports season, followed in some cases by playoffs. Hundreds of sports exist, from those between single contestants, through to those with hundreds of simultaneous participants, either in teams or competing as individuals. In certain sports such as racing, many contestants may compete, each against all with one winner."
c.execute("INSERT INTO docclf_db(content, category, date) VALUES(?, ?, DATETIME('now'))", (example1, 2))

example2 = "Politics is the process of making uniform decisions applying to all members of a group. More narrowly, it refers to achieving and exercising positions of governance — organized control over a human community, particularly a state. Furthermore, politics is the study or practice of the distribution of power and resources within a given community (a usually hierarchically organized population) as well as the interrelationship(s) between communities. Politics presents one of the ten function systems of modern societies."
c.execute("INSERT INTO docclf_db(content, category, date) VALUES(?, ?, DATETIME('now'))", (example2, 4))

conn.commit()
conn.close()