#!/usr/bin/env python3

import re

def main(arguments):
	config=dict()
	positional=[]
	pattern=re.compile(r"(?:-(?:b|h|x|p|v|V)|--(?:bins|help|positive|version))(?:=.*)?$")
	consuming,needing,wanting=None,0,0
	attached_value=None
	while len(arguments) and arguments[0]!="--":
		if consuming is not None:
			if config[consuming] is None:
				config[consuming]=arguments.pop(0)
			else:
				config[consuming].append(arguments.pop(0))
			needing-=1
			wanting-=1
			if wanting==0:
				consuming,needing,wanting=None,0,0
		elif pattern.match(arguments[0]):
			option = arguments.pop(0).lstrip('-')
			if '=' in option:
				option,attached_value=option.split('=',1)
			if option=="bins":
				if attached_value is not None:
					config["bins"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["bins"]=None
					consuming,needing,wanting="bins",1,1
			elif option=="help":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "help"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["help"]=True
			elif option=="positive":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "positive"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["positive"]=True
			elif option=="version":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "version"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["version"]=True
			elif option=="b":
				if attached_value is not None:
					config["bins"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["bins"]=None
					consuming,needing,wanting="bins",1,1
			elif option=="h":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "help"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["help"]=True
			elif option=="x":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "help"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["help"]=True
			elif option=="p":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "positive"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["positive"]=True
			elif option=="v":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "version"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["version"]=True
			elif option=="V":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "version"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["version"]=True
		else:
			positional.append(arguments.pop(0))
	if needing>0:
		message=(
			f'unexpected end while parsing "{consuming}"'
			f' (expected {needing} values)'
		)
		raise ValueError(message) from None
	for argument in arguments[1:]:
		positional.append(argument)
	return config,positional

if __name__=="__main__":
	import sys
	cfg,pos = main(sys.argv[1:])
	cfg = {k:v for k,v in cfg.items() if v is not None}
	if len(cfg):
		print("Options:")
		for k,v in cfg.items():
			print(f"{k:20} = {v}")
	if len(pos):
		print("Positional arguments:", ", ".join(pos))
