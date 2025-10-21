#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 22:29:55 2024
Pymon skeleton game
Please make modifications to all the classes to match with requirements provided in the assignment spec document
@author: dipto
@student_id : 
@highest_level_attempted (P/C/D/HD):

- Reflection:
- Reference:
"""

from Operation import Operation
import sys
                    
if __name__ == '__main__':
    operation = Operation()
    try:
        # for i in range(1, len(sys.argv)):
        #     if sys.argv[i] == '-o' and i + 1 < len(sys.argv):
        #         orders_file = sys.argv[i + 1]
        #     elif sys.argv[i] == '-g' and i + 1 < len(sys.argv):
        #         guests_file = sys.argv[i + 1]
        #     elif sys.argv[i] == '-p' and i + 1 < len(sys.argv):
        #         products_file = sys.argv[i + 1]
        #     elif not sys.argv[i] in ["-o","-g","-p"] and sys.argv[i].startswith("-"):
        #         print("This program have no ",sys.argv[i]," there's only -g for guest_file , -p for product_file , -o for order_file")

        operation.setup()
        operation.start_game()
    except Exception as e:
        print(e)
