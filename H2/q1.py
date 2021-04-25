# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 15:44:39 2021

@author: luyao.li
"""
import numpy as np
y2=0
y4=1

psi12= psi34 =np.array([[1,0.9],[0.9,1]])
psi23=psi35 =np.array([[0.1, 1],[1,0.1]])
phi22 = phi44= np.array([[1,0.1],[0.1,1]])
phi1 =phi3=phi5 =np.array([0.5,0.5])
phi2 =phi22[:,y2]
phi4= phi44[:,y4] 
 

m43= phi4 @ psi34
m53 = phi5 @ psi35
m32=  phi3 @ psi23 * m43 * m53
m21 =  phi2 @ psi12 * m32
b1_tmp= phi1 * m21
b1 =b1_tmp/b1_tmp.sum()

m12= phi1 @ psi12
b2_tmp = phi2 * (m32 * m12)
b2 =b2_tmp/b2_tmp.sum()

m23= phi2 @ psi23 * m12
b3_tmp= phi3  * ( m23 * m43 *m53)
b3 =b3_tmp/b3_tmp.sum() 

m34 =phi3  @ psi34 * m23
b4_tmp= phi4 * m34 
b4= b4_tmp/b4_tmp.sum()

m35= phi3 @ psi35 * (m23 * m43)
b5_tmp= phi5 * m35
b5 =b5_tmp/b5_tmp.sum()
print(b1,b2,b3,b4,b5)

#[0.5 0.5] 
#[0.90171326 0.09828674] 
#[0.15373972 0.84626028]
#[0.01941748 0.98058252] 
#[0.15373972 0.84626028]