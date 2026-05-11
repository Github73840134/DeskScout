# DeskScout Extension Help
import argparse
__args__ = None
parser = argparse.ArgumentParser("help","help [topic]","gives help on built in functions")
parser.add_argument("topic")




def run():
	args = parser.parse_args(__args__)
	print(args)