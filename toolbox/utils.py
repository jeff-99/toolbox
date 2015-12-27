__author__ = 'jeff'
import random

ADJECTIVES = ["red", "colossal", "rusty", "tiny", "trustworthy", "dirty", "redundant", "cute"]
TOOLS = ["hammer", "screwdriver", "pliers", "saw", "knife", "shovel", "shear"]


def generate_name():
    return random.choice(ADJECTIVES) + "_" + random.choice(TOOLS)