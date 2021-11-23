# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 21:18:20 2021

@author: VV
"""

airlines_splitted = []

try:
    airlines = open("airlines.txt", "r")
    airlines_list = airlines.readlines()
    for n in range (len(airlines_list)):
        airlines_splitted.append(airlines_list[n].split(","))    
        airlines_splitted[n][-1] = airlines_splitted[n][-1].rstrip('\n')
        
except IOError:
    print("Error!")      
finally:
    airlines.close()  
    
    airlines_D = input("Enter airline miles are on: ") 
    airlines_A = input("Enter goal airline: ")
    
    flag = 0    
    for i in range (len(airlines_splitted)):
        if airlines_D == airlines_splitted[i][0]:
            flag = flag + 1
            for j in range (len(airlines_splitted[i])):
                if airlines_A == airlines_splitted[i][j]:
                    print("There is a partnership between these airlines!\n")
                    flag = flag + 1
                    path_size = j+1
                    break                    
            if(flag==1):    
                print("Unfortunately, There isn't a partnership between these airlines.")  
                flag = flag + 1
            path_no = i    
            break
        
    if(flag==0):            
        print("There isnt '"+str(airlines_D)+"' in the list")
    elif(flag==2):
        print("path:")
        for n in range (path_size):
            print(str(n+1)+")"+str(airlines_splitted[path_no][n]))
                          




