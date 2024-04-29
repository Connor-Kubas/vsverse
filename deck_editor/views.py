from django.shortcuts import render
# from .view_directory.DisplayView import *
# import view_directory.DisplayView
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
# sys.path.insert(0, '.austoaehsuoeth/')
# print(sys.path)
# exit()
from view_directory import DisplayView
