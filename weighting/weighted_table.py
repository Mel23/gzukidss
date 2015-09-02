
#Aug 15 2014
#Code to recalculate vote fractions based on user weights
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

print 'reading file...'
weights=pyfits.open('/data/lucifer1.1/users/galloway/UKIDSS/user_kappa_weights_2.fits')
weight_data=weights[1].data
data = ascii.read("/data/lucifer1.1/users/galloway/UKIDSS/csv/2014-06-15_galaxy_zoo_classifications_ukidss_wrong_votes_removed.csv")

print 'organizing subjects...'
subjects = set(data['subject_id'])
    
    # Now set up the collated classification columns. 
    # Each question has a question number from ukidss-0 to ukidss-11
    # Each of those questions has some number of possible answers a-0, a-1, etc. 
    #   One question = odd features (07) has click boxes where multiple answers can be selected.
    #   This question alone needs to be treated differently than the others.
    # In GZ2/GZH the answer numbers were themselves unique but in Ouroboros they start at a-0 for each question number.
    #
print 'Creating columns for vote fractions...'
    
    # Create column of integer zeros and float zeros
intcolumn = np.zeros(len(subjects),dtype=int)
floatcolumn = np.zeros(len(subjects),dtype=float)
strcolumn = np.array([' ']*len(subjects),dtype='S24')
   #S24=24 character string 
    #c01 = Column(name='num_classifications', format='J', array=floatcolumn)          # c05 = c01, by definition

#format for Columns: D = double precision floating point, J = integer
c01 = Column(name='subject_id', format='A24', array=strcolumn)          # c05 = c01, by definition

c02 = Column(name='t00_smooth_or_features_a0_smooth_frac_weighted_2', format='D', array=floatcolumn)
c03 = Column(name='t00_smooth_or_features_a1_features_frac_weighted_2', format='D', array=floatcolumn)
c04 = Column(name='t00_smooth_or_features_a2_artifact_frac_weighted_2', format='D', array=floatcolumn)
c05 = Column(name='t00_smooth_or_features_count_weighted_2', format='J', array=intcolumn)

c06 = Column(name='t01_disk_edge_on_a0_yes_frac_weighted_2', format='D', array=floatcolumn)
c07 = Column(name='t01_disk_edge_on_a1_no_frac_weighted_2', format='D', array=floatcolumn)
c08 = Column(name='t01_disk_edge_on_count_weighted_2', format='J', array=intcolumn)

c09 = Column(name='t02_bar_a0_bar_frac_weighted_2', format='D', array=floatcolumn)
c10 = Column(name='t02_bar_a1_no_bar_frac_weighted_2', format='D', array=floatcolumn)
c11 = Column(name='t02_bar_count_weighted_2', format='J', array=intcolumn)

c12 = Column(name='t03_spiral_a0_spiral_frac_weighted_2', format='D', array=floatcolumn)
c13 = Column(name='t03_spiral_a1_no_spiral_frac_weighted_2', format='D', array=floatcolumn)
c14 = Column(name='t03_spiral_count_weighted_2', format='J', array=intcolumn)

c15 = Column(name='t04_bulge_prominence_a0_no_bulge_frac_weighted_2', format='D', array=floatcolumn)
c16 = Column(name='t04_bulge_prominence_a1_just_noticeable_frac_weighted_2', format='D', array=floatcolumn)
c17 = Column(name='t04_bulge_prominence_a2_obvious_frac_weighted_2', format='D', array=floatcolumn)
c18 = Column(name='t04_bulge_prominence_a3_dominant_frac_weighted_2', format='D', array=floatcolumn)
c19 = Column(name='t04_bulge_prominence_count_weighted_2', format='J', array=intcolumn)

c20 = Column(name='t05_odd_a0_yes_frac_weighted_2', format='D', array=floatcolumn)
c21 = Column(name='t05_odd_a1_no_frac_weighted_2', format='D', array=floatcolumn)
c22 = Column(name='t05_odd_count_weighted_2', format='J', array=intcolumn)

c23 = Column(name='t06_odd_feature_x0_ring_frac_weighted_2', format='D', array=floatcolumn)
c24 = Column(name='t06_odd_feature_x1_lens_frac_weighted_2', format='D', array=floatcolumn)
c25 = Column(name='t06_odd_feature_x2_disturbed_frac_weighted_2', format='D', array=floatcolumn)
c26 = Column(name='t06_odd_feature_x3_irregular_frac_weighted_2', format='D', array=floatcolumn)
c27 = Column(name='t06_odd_feature_x4_other_frac_weighted_2', format='D', array=floatcolumn)
c28 = Column(name='t06_odd_feature_x5_merger_frac_weighted_2', format='D', array=floatcolumn)
c29 = Column(name='t06_odd_feature_x6_dustlane_frac_weighted_2', format='D', array=floatcolumn)
c30 = Column(name='t06_odd_feature_a0_discuss_frac_weighted_2', format='D', array=floatcolumn)
c31 = Column(name='t06_odd_feature_count_weighted_2', format='J', array=intcolumn)

c32 = Column(name='t07_rounded_a0_completely_round_frac_weighted_2', format='D', array=floatcolumn)
c33 = Column(name='t07_rounded_a1_in_between_frac_weighted_2', format='D', array=floatcolumn)
c34 = Column(name='t07_rounded_a2_cigar_shaped_frac_weighted_2', format='D', array=floatcolumn)
c35 = Column(name='t07_rounded_count_weighted_2', format='J', array=intcolumn)

c36 = Column(name='t08_bulge_shape_a0_rounded_frac_weighted_2', format='D', array=floatcolumn)
c37 = Column(name='t08_bulge_shape_a1_boxy_frac_weighted_2', format='D', array=floatcolumn)
c38 = Column(name='t08_bulge_shape_a2_no_bulge_frac_weighted_2', format='D', array=floatcolumn)
c39 = Column(name='t08_bulge_shape_count_weighted_2', format='J', array=intcolumn)

c40 = Column(name='t09_arms_winding_a0_tight_frac_weighted_2', format='D', array=floatcolumn)
c41 = Column(name='t09_arms_winding_a1_medium_frac_weighted_2', format='D', array=floatcolumn)
c42 = Column(name='t09_arms_winding_a2_loose_frac_weighted_2', format='D', array=floatcolumn)
c43 = Column(name='t09_arms_winding_count_weighted_2', format='J', array=intcolumn)

c44 = Column(name='t10_arms_number_a0_1_frac_weighted_2', format='D', array=floatcolumn)
c45 = Column(name='t10_arms_number_a1_2_frac_weighted_2', format='D', array=floatcolumn)
c46 = Column(name='t10_arms_number_a2_3_frac_weighted_2', format='D', array=floatcolumn)
c47 = Column(name='t10_arms_number_a3_4_frac_weighted_2', format='D', array=floatcolumn)
c48 = Column(name='t10_arms_number_a4_more_than_4_frac_weighted_2', format='D', array=floatcolumn)
c49 = Column(name='t10_arms_number_a5_cant_tell_frac_weighted_2', format='D', array=floatcolumn)
c50 = Column(name='t10_arms_number_count_weighted_2', format='J', array=intcolumn)

c51 = Column(name='t11_discuss_a0_yes_frac_weighted_2', format='D', array=floatcolumn)
c52 = Column(name='t11_discuss_a1_no_frac_weighted_2', format='D', array=floatcolumn)
c53 = Column(name='t11_discuss_count_weighted_2', format='J', array=intcolumn)
    
frac_dict = {
        'ukidss-0':{
            'a-0':'t00_smooth_or_features_a0_smooth_frac_weighted_2',
            'a-1':'t00_smooth_or_features_a1_features_frac_weighted_2',
            'a-2':'t00_smooth_or_features_a2_artifact_frac_weighted_2',
            'count':'t00_smooth_or_features_count_weighted_2'
         }
        ,
        'ukidss-1':{
            'a-0':'t01_disk_edge_on_a0_yes_frac_weighted_2',
            'a-1':'t01_disk_edge_on_a1_no_frac_weighted_2',
            'count':'t01_disk_edge_on_count_weighted_2'
        }
        ,
        'ukidss-2':{
            'a-0':'t02_bar_a0_bar_frac_weighted_2',
            'a-1':'t02_bar_a1_no_bar_frac_weighted_2',
            'count':'t02_bar_count_weighted_2'
        }
        ,
        'ukidss-3':{
            'a-0':'t03_spiral_a0_spiral_frac_weighted_2',
            'a-1':'t03_spiral_a1_no_spiral_frac_weighted_2',
            'count':'t03_spiral_count_weighted_2'
        }
        ,
        'ukidss-4':{
            'a-0':'t04_bulge_prominence_a0_no_bulge_frac_weighted_2',
            'a-1':'t04_bulge_prominence_a1_just_noticeable_frac_weighted_2',
            'a-2':'t04_bulge_prominence_a2_obvious_frac_weighted_2',
            'a-3':'t04_bulge_prominence_a3_dominant_frac_weighted_2',
            'count':'t04_bulge_prominence_count_weighted_2'
        }
        ,
        'ukidss-5':{
            'a-0':'t05_odd_a0_yes_frac_weighted_2',
            'a-1':'t05_odd_a1_no_frac_weighted_2',
            'count':'t05_odd_count_weighted_2'
        }
        ,
        'ukidss-6':{
            'x-0':'t06_odd_feature_x0_ring_frac_weighted_2',
            'x-1':'t06_odd_feature_x1_lens_frac_weighted_2',
            'x-2':'t06_odd_feature_x2_disturbed_frac_weighted_2',
            'x-3':'t06_odd_feature_x3_irregular_frac_weighted_2',
            'x-4':'t06_odd_feature_x4_other_frac_weighted_2',
            'x-5':'t06_odd_feature_x5_merger_frac_weighted_2',
            'x-6':'t06_odd_feature_x6_dustlane_frac_weighted_2',
            'a-0':'t06_odd_feature_a0_discuss_frac_weighted_2',
            'count':'t06_odd_feature_count_weighted_2'
        }
        ,
        'ukidss-7':{
            'a-0':'t07_rounded_a0_completely_round_frac_weighted_2',
            'a-1':'t07_rounded_a1_in_between_frac_weighted_2',
            'a-2':'t07_rounded_a2_cigar_shaped_frac_weighted_2',
            'count':'t07_rounded_count_weighted_2'
        }
        ,
        'ukidss-8':{
            'a-0':'t08_bulge_shape_a0_rounded_frac_weighted_2',
            'a-1':'t08_bulge_shape_a1_boxy_frac_weighted_2',
            'a-2':'t08_bulge_shape_a2_no_bulge_frac_weighted_2',
            'count':'t08_bulge_shape_count_weighted_2'
        }
        ,
        'ukidss-9':{
            'a-0':'t09_arms_winding_a0_tight_frac_weighted_2',
            'a-1':'t09_arms_winding_a1_medium_frac_weighted_2',
            'a-2':'t09_arms_winding_a2_loose_frac_weighted_2',
            'count':'t09_arms_winding_count_weighted_2'
        }
        ,
        'ukidss-10':{
            'a-0':'t10_arms_number_a0_1_frac_weighted_2',
            'a-1':'t10_arms_number_a1_2_frac_weighted_2',
            'a-2':'t10_arms_number_a2_3_frac_weighted_2',
            'a-3':'t10_arms_number_a3_4_frac_weighted_2',
            'a-4':'t10_arms_number_a4_more_than_4_frac_weighted_2',
            'a-5':'t10_arms_number_a5_cant_tell_frac_weighted_2',
            'count':'t10_arms_number_count_weighted_2'
        }
        ,
        'ukidss-11':{
            'a-0':'t11_discuss_a0_yes_frac_weighted_2',
            'a-1':'t11_discuss_a1_no_frac_weighted_2',
            'count':'t11_discuss_count_weighted_2'
        }
}
    
    
classifications = pyfits.new_table([c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35,c36,c37,c38,c39,c40,c41,c42,c43,c44,c45,c46,c47,c48,c49,c50,c51,c52,c53])

subjDB = pyfits.new_table(classifications.columns)
questions = ['ukidss-%i' % j for j in np.arange(len(frac_dict))]
questions.remove('ukidss-6')
#sys.exit('lol')
#questions = ['col%i' % j+6 for j in np.arange(len(frac_dict))]
#questions.remove('col12')
#questions=['col6','col7','col8', 'col9','col10','col11','col13','col14','col15','col16','col17']
dupsubjects=[] #get list of subjects which have duplicates for reference
for idx,s in enumerate(subjects):

    if idx % 1000 == 0:
        print idx, datetime.datetime.now().strftime('%H:%M:%S.%f')

        # Find each classification for this subject
    this_subj = (data['subject_id'] == s)

    subjDB.data.field('subject_id')[idx] = s

    #Find duplicats (cases where the same user classifies a subject more than once)
    users=[]
    dup=[]
#create list of users for each subject
    for row in data[this_subj]:
        users.append(row[2])
#determine if a user appears twice
    for person in set(users):
        if users.count(person)>1:
            dup.append(person)
#redefine data[this_subj] because reasons
    data_this_subj=data[this_subj]
#if any duplicates are found, mask data from user's ealier classification(s)
    if len(dup)>0:
        dupsubjects.append(s)
        for person in dup:
            dates=(data_this_subj['user']==person)
            latestdate=max(data_this_subj[dates]['created_at'])
            for i,row in enumerate(data_this_subj):
                #if the user is a duplicate person *and* the classification date is not the latest date option, mask the row
                if row['user']==person and row['created_at']<latestdate:
                    data_this_subj.remove_row(i)
    
        # Loop over each question in the tree and record count, vote fractions
    for row in data_this_subj:
        for i,q in enumerate(questions):
            ctr = Counter(data_this_subj[q].compressed())
            thisuserweight=(weight_data['user']==row['user'])
            N_total = np.sum(ctr.values())-ctr['0']
            subjDB.data.field(frac_dict[q]['count'])[idx] = N_total
            for key in ctr.keys():
                if row[q]==key:
                    try:
                        subjDB.data.field(frac_dict[q][key])[idx] += weight_data[thisuserweight]['userweight'][0]/float(N_total) if N_total > 0 else 0.
                    except KeyError:
                        pass

     #    Question 6 (odd features) is treated differently, since more than one answer can be selected
    
    ctr6 = Counter(data_this_subj['ukidss-6'].compressed())
    N_total = np.sum(ctr6.values())-ctr['0']
    subjDB.data.field(frac_dict['ukidss-6']['count'])[idx] = N_total
    for key in ctr6.keys():
         strkey = str(key)
         splitkey = strkey.split(';')
         if len(splitkey) > 1:
             for sk in splitkey:
                 try:
                     subjDB.data.field(frac_dict['ukidss-6'][sk])[idx] += ctr6[strkey]/float(N_total) if N_total > 0 else 0.
                 except KeyError:
                     pass
         else:
             try:
                 subjDB.data.field(frac_dict['ukidss-6'][key])[idx] = ctr6[key]/float(N_total) if N_total > 0 else 0.
             except KeyError:
                 pass
      

print 'Finished looping over classifications'
    
    # Write final data to FITS file
subjDB.writeto('ukidss_classifications_collated_weighted_2.fits',clobber=True)

