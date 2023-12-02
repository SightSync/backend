import os
import subprocess

HOME = os.getcwd()
subprocess.run("mkdir -p gr_dino")
subprocess.run("cd gr_dino/")
subprocess.run("git clone https://github.com/IDEA-Research/GroundingDINO.git")
subprocess.run("cd GroundingDINO")
subprocess.run("git checkout -q 57535c5a79791cb76e36fdb64975271354f10251")
subprocess.run("pip install -q -e .")
os.mkdir(f"{HOME}/gr_dino/weights")
subprocess.run("wget -q https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth")