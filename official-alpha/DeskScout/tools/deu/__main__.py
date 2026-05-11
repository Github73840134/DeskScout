import argparse,json,os,sys
from importlib import util as imputil
sys.path.insert(0,os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'app','libs'))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'app','mods'))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'app'))


parser = argparse.ArgumentParser("deu",description="DeskScout Extension Utility",add_help=False)
parser.add_argument("action")
parser.add_argument('args',nargs=argparse.REMAINDER, help="arguments",default="")
args = parser.parse_args()
print(args)
if args.action:
	actions = json.load(open(os.path.join(os.path.dirname(__file__),'actions.json')))
	for i in actions:
		if i == args.action:
			exec(f"import {actions[i]} as Applet")
			Applet.__args__ = args.args
			Applet.run()
