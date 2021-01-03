import os, sys

dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(dir)
grand_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, grand_parent_dir)

from flask_script import Command, Manager, Option

from feedDB import FeedDB
from restaurantDB import RestaurantDB

class dbAdapter(Command):
    option_list = (
        Option('--type', '-T', dest='type', default=None),
    )

    def run(self, type):
        if type=='feed' or type=='f':
            feedDB = FeedDB()
            feedDB.run()
        if type=='restaurant' or type=='r':
            restaurantDB = RestaurantDB()
            restaurantDB.run()
