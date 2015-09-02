import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from collections import Counter
#from pymongo import MongoClient


from astropy.io import fits as pyfits
from astropy.io.fits import Column
from astropy.io import ascii

#Aug 4 2014 - Code to weight user's votes based on consistency
#First create table of consistency values for each user
#Second count vote fractions and multiply fraction by user's weight
#Create new table with weighted vote fractions

#This code will be run more than once, so log iterations:
#1st iteration - use unweighted vote table 
data = ascii.read("/data/lucifer1.1/users/galloway/UKIDSS/csv/2014-06-15_galaxy_zoo_classifications_ukidss_wrong_votes_removed.csv", 'b')
votes=pyfits.open('/data/lucifer1.1/users/galloway/UKIDSS/weighting/ukidss_classifications_collated_weighted_1_with_headers_for_code.fits')
vf=votes[1].data
users=list(set(data['user']))

strcolumn=np.array([' ']*len(users),dtype='S50')
floatcolumn=np.zeros(len(users),dtype=float)

c1 = Column(name='user', format='A50', array=strcolumn)   
c2 = Column(name='weight', format='D', array=floatcolumn)   

weightcols=pyfits.new_table([c1,c2])
weight_table=pyfits.new_table(weightcols.columns)

def get_kappa(usersanswer,allanswers,X,N_answers):
    kappa=[]
    for j in range(0,N_answers):
        if usersanswer=='a-%i' % j:
            kappa.append(allanswers['ukidss-%i;a-%i' % (X,j)][0])
        else:
            kappa.append(1-allanswers['ukidss-%i;a-%i' % (X,j)][0])
    return(sum(kappa)/len(kappa))


for i,u in enumerate(users):
    if i % 1000==0:
        print i, datetime.datetime.now().strftime('%H:%M:%S.%f')
    weight_table.data.field('user')[i]=u
    this_user=(data['user']==u)



    kappa_this_user=[]
    for row in data[this_user]:
        these_votes=(vf['subject_id']==row['subject_id'])
        vf_tv=vf[these_votes]
        if row['ukidss-0']!=' ':
            kappa_this_user.append(get_kappa(row['ukidss-0'],vf_tv,0,3))
        if row['ukidss-1']!=' ':
            kappa_this_user.append(get_kappa(row['ukidss-1'],vf_tv,1,2))
        if row['ukidss-2']!=' ':
            kappa_this_user.append(get_kappa(row['ukidss-2'],vf_tv,2,2))
        if row['ukidss-3']!=' ':
            kappa_this_user.append(get_kappa(row['ukidss-3'],vf_tv,3,2))
        if row['ukidss-4']!=' ':
            kappa_this_user.append(get_kappa(row['ukidss-4'],vf_tv,4,4))
        if row['ukidss-5']!=' ':
            kappa_this_user.append(get_kappa(row['ukidss-5'],vf_tv,5,2))
        if row['ukidss-7']!=' ':
            kappa_this_user.append(get_kappa(row['ukidss-7'],vf_tv,7,3))
        if row['ukidss-8']!=' ':
            kappa_this_user.append(get_kappa(row['ukidss-8'],vf_tv,8,3))
        if row['ukidss-9']!=' ':
            kappa_this_user.append(get_kappa(row['ukidss-9'],vf_tv,9,3))
        if row['ukidss-10']!=' ':
            kappa_this_user.append(get_kappa(row['ukidss-10'],vf_tv,10,6))
    try:
        weight_table.data.field('weight')[i]=sum(kappa_this_user)/len(kappa_this_user)
    except ZeroDivisionError:
        pass

weight_table.writeto('userweights_2.fits',clobber=True)





