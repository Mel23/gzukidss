import params
import numpy as np
import math

#-------------------------------------------------------------------------------
'''List the functions (and their respective inverses)'''

def f_logistic(x, k, c):
    # Function to fit the data bin output from the raw plot function
    L = (1 + np.exp(c))
    r = L / (1.0 + np.exp(-k * x + c))
    return r


def f_exp_pow(x, k, c):
    # Function to fit the data bin output from the raw plot function
    r = np.exp(-k * (-x) ** c)
    return r


def i_f_logistic(y, k, c):
    # inverse of f_logistic
    L = (1 + np.exp(c))
    x = -(np.log(L / y - 1) - c) / k
    return x


def i_f_exp_pow(y, k, c):
    # inverse of f_exp_pow
    ok = k > 0
    x = np.zeros_like(y) - np.inf
    x[ok] = -(-np.log(y[ok]) /k[ok] )**(1.0/c[ok])
    return x
#-------------------------------------------------------------------------------
'''This dictionary lists all of the functions and bounds to be used in the
to fit the data'''

function_dictionary = {}
function_dictionary['func'] = {0: f_logistic,
                               1: f_exp_pow,
                               #2: f_inv
                               }

function_dictionary['bounds'] = {0: params.logistic_bounds,
                                 1: params.exponential_bounds
                                 #2: params.inverse_bounds,
                                 }

function_dictionary['p0'] = {0: [3,-3],
                             1: [2,1],
                             #2: [1,1]
                             }

function_dictionary['i_func'] = {0: i_f_logistic,
                                 1: i_f_exp_pow
                                 #2:None
                                 }

function_dictionary['label'] = {0: 'logistic',
                                1: 'exp. power'
                                #2:'inverse'
                                 }
#-------------------------------------------------------------------------------
'''Make a dictionary of questions, answers, and which questions precede others
'''

# List of questions in order:
q = ['t00_smooth_or_features'
     ,'t01_disk_edge_on'
     ,'t02_bar'
     ,'t03_spiral'
     ,'t04_bulge_prominence'
     ,'t05_odd'
     ,'t07_rounded'
     ,'t06_odd_feature'
     ,'t08_bulge_shape'
     ,'t09_arms_winding'
     ,'t10_arms_number']

# Labels for each of the questions (for plotting):
label_q = ['Smooth or features'
     ,'Edge on'
     ,'Bar'
     ,'Spiral'
     ,'Bulge prominence'
     ,'Anything odd'
     ,'Roundedness'
     ,'Odd features'
     ,'Bulge shape'
     ,'Arm winding'
     ,'Arm number']

# Answers for each of the questions in turn:
a = [['a0_smooth','a1_features','a2_artifact']
     ,['a0_yes','a1_no']
     ,['a0_bar','a1_no_bar']
     ,['a0_spiral','a1_no_spiral']
     ,['a0_no_bulge','a1_just_noticeable','a2_obvious','a3_dominant']
     ,['a0_yes','a1_no']
     ,['a0_completely_round','a1_in_between','a2_cigar_shaped']
     ,['x0_ring','x1_lens','x2_disturbed','x3_irregular','x4_other','x5_merger','x6_dust_lane']
     ,['a0_rounded','a1_boxy','a2_no_bulge']
     ,['a0_tight','a1_medium','a2_loose']
     ,['a0_1','a1_2','a2_3','a3_4','a4_more_than_4','a5_cant_tell']]

# Answer labels (for plotting):
label_a = [['Smooth','Features','Artifact']
     ,['Yes','No']
     ,['Yes','No']
     ,['Yes','No']
     ,['None','Noticeable','Obvious','Dominant']
     ,['Yes','No']
     ,['Round','In between','Cigar shaped']
     ,['Ring','Lens/Arc','Disturbed','Irregular','Other','Merger','Dust lane']
     ,['Rounded','Boxy','None']
     ,['Tight','Medium','Loose']
     ,['1','2','3','4','5+','??']]

# 'Previously answered questions' for each question in turn:
pre_q = [None
         ,[0]
         ,[0,1]
         ,[0,1]
         ,[0,1]
         ,None
         ,[0]
         ,[5]
         ,[0,1]
         ,[0,1,3]
         ,[0,1,3]]

# Required answers for each previously answered question:
pre_a = [None
         ,[1]
         ,[1,1]
         ,[1,1]
         ,[1,1]
         ,None
         ,[0]
         ,[0]
         ,[1,0]#this was [1,1] in original file - mistake! have to answer 'yes' to edgeon question. 
         ,[1,1,0]
         ,[1,1,0]]

#-------------------------------------------------------------------------------
'''Put all of this together in a single dictionary called "questions" '''

questions = {}

for s in range(len(q)):
    
    if pre_q[s] is not None:
        pq = [q[v] for v in pre_q[s]] 
    else:
        pq = None
    
    questions[q[s]] = {'answers': a[s]
                       ,'answerlabels': label_a[s]
                       ,'questionlabel': label_q[s]
                       ,'pre_questions': pq}
    
    if pre_a[s] is not None:
        pa_array = [questions[q[v]]['answers'] 
		    for v in pre_q[s]]
        answer_arrays = [pa_array[v] 
			 for v in range(len(pre_a[s]))]
        answer_indices = [pre_a[s][v] 
			  for v in range(len(pre_a[s]))]
        pa = [answer_arrays[v2][answer_indices[v2]] 
	      for v2 in range(len(answer_indices))]
 
    else:
        pa = None # if there are no previous questions
    
    questions[q[s]].update({'pre_answers': pa})
