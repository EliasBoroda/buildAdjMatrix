# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 13:31:14 2020

@author: Elias
"""

import numpy as np
import csv
import argparse

        
class BuildAdjMatrix:
    
    
    def __init__(self, npyfile, roifile, targetroi, sessionfile,
                 verbosity=1):

        # the npy file containing the raw 3d correlation files for each session
        self.npy_file = npyfile
        
        # file with names of the ROIs in the order they are in the npy file
        # header: 
        self.ROI_label_file = roifile
        
        # file with matrix containing target roi names?
        self.target_roi = targetroi

        # file containing info on each session in the npy file
        # Participant,Timepoint,Group,Processing Deriv
        # header: 
        self.session_file = sessionfile
        
        # default is set to 1
        self.verbosity = verbosity
        
    def check_header(self, filename, fieldlist):
        # checks if header from csv file contains the fields in the fieldlist
        # returns True if all fields are present
       
        try: 
            with open(filename,'rt')as fileobj:        
                        
                # read in first row
                reader = csv.reader(fileobj)
                header = reader.__next__()
                # close file
                fileobj.close()
                
                # check whether each of the fields is present in header
                for field in fieldlist:
                    if field not in header:
    
                        if self.verbosity >= 0:
                            print('Error: In csv file: ', filename, 'field not found: ', field)
                            print('Header from file: ', header)
    
                        return False
            
                return True
        
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            exit(1)
            
    def load_ROI_file(self):
            # read in the ROI label csv file, want an indexed array and a
            # dictionary for label lookup of the index
    
            # returns True if successful or False if not
            
            # check if header contains the fields
            fieldlist = ['roi']
            if not self.check_header(self.ROI_label_file, fieldlist):
                    return False
                
            with open(self.ROI_label_file,'rt')as f:
                       
                self.ROI_raw = csv.reader(f)
                #print(self.ROI_raw)
                next(self.ROI_raw)  # skip the header in the csv file
                
                # roi list
                self.ROIlist = []
                
                # roi dictionary
                self.ROIdict = {}
                index = 0
                
                for row in self.ROI_raw:
                    #pass
                    if self.verbosity > 1:
                        print(row)
                    # append to list
                    self.ROIlist.append(row[0])
                    # append to dictionary with update
                    self.ROIdict[row[0]] = index
                    
                    index = index + 1 # increment the index
                
                if self.verbosity > 0:
                    print('all roi file entries', len(self.ROIlist))
    
                #print(self.ROIdict)
                #print(self.ROIdict['CEREBELLUM_LEFT']) # print index
            
            return True    
    
    def load_target_ROI_file(self):
        # read in the ROI label csv file, want an indexed array and a
        # dictionary for label lookup of the index

        # returns True if successful or False if not
        
        # check if header contains the fields
        fieldlist = ['roi']
        if not self.check_header(self.target_roi, fieldlist):
                return False
            
        with open(self.target_roi,'rt')as f:
                   
            self.target_ROI_raw = csv.reader(f)
            #print(self.ROI_raw)
            next(self.target_ROI_raw)  # skip the header in the csv file
            
            # roi list
            self.target_ROIlist = []
            
            # roi dictionary
            self.target_ROIdict = {}
            
            for roi in self.target_ROI_raw:
                #pass
                if self.verbosity > 1:
                    print(roi)
                # append to list
                self.target_ROIlist.append(roi[0])
                
                # append to dictionary with update
                #self.target_ROIdict[roi[0]] = index
                
                #index = index + 1 # increment the index
            
            for roi in range(len(self.target_ROIlist)):
                
                roi_label = self.target_ROIlist[roi]
                roi_idx = self.ROIdict.get(roi_label)
                
                self.target_ROIdict.update({roi_label : roi_idx})
                
            
            if self.verbosity > 0:
                print('target roi file entries', len(self.target_ROIlist))

            #print(self.ROIdict)
            #print(self.ROIdict['CEREBELLUM_LEFT']) # print index
        
        return True 
    
    def load_session_file(self):
        # read in the session  file
        
        # TODO - consider rewrite using csv.DictReader

        # check if header contains the fields
        fieldlist = ['grid', 'timepoint', 'group']
        if not self.check_header(self.session_file, fieldlist):
                return False
        
        with open(self.session_file,'rt')as f:
            
            self.session_raw = csv.reader(f)
            
            next(self.session_raw)  # skip the header in the csv file
            
            self.sessions = []
            
            # for each row create a dictionary item and append to list
            
            for row in self.session_raw:
                #pass
                # print(row[0], row[1])
                # load data into a dictionary
                tempDict = {}
                tempDict = {'ID': row[0], 'TP': row[1],'GRP': row[2]}
                #print(tempDict['ID'])
                self.sessions.append(tempDict)
                
        if self.verbosity > 0:
            print('session file entries', len(self.sessions))
            
        return True
    
    def load_files(self):
        # load all the data files
        
        # read in the raw 3d correlation matrix, adjacency matrix for 
        # each session (3rd dimension)
        try:
            self.rawcorr = np.load(self.npy_file)
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            exit(1)
        
        # tip in spyder if you want to see all objects present in your 
        # namespace, you need to go to the menu
        # Tools > Preferences > Variable Explorer
        # and turn off the option called
        # Exclude unsupported data types
        
        # check if returns true or false
        
        if not self.load_ROI_file():
            # error in reading file
            return False
        
        if not self.load_target_ROI_file():
            return False
        
        if not self.load_session_file():
            return False
        

        return True
    
    def retrieve_corr(self, index_a, index_b, session):
        # retrieve correlations for the target roi
        values = self.rawcorr[index_a, index_b, session]
        return values
    
    def create_output_header(self):
        # create the output beader from the session and connections info
        # the first three elements are extracted from the session
        # returns a list 
        
        # get the three session labels
        hdrlist = list(self.sessions[0].keys())
        hdrlist.append('ROI')
        
        self.sessionkeys = hdrlist
        
        # now add each of the connection labels
        for item in self.target_ROIlist:
            # first element in list is the connection label
            hdrlist.append(item)
            
            return hdrlist    
    
    def retrieve_target_matrix(self):
        
        #setup matrix with the right dimentions for output [roi x roi x sessions]
        self.target_matrix = np.zeros((len(self.target_ROIlist),
                                      len(self.target_ROIlist), 
                                      len(self.sessions)))
        
        #first loop for sessions
        for session in range(len(self.sessions)):
            
            #second loop for column roi
            for roi_c in range(len(self.target_ROIlist)):
                
                roi_label = self.target_ROIlist[roi_c]
                col_idx = self.ROIdict.get(roi_label)
                
                #third loop for pulling values from all rows in that column
                for roi_r in range(len(self.target_ROIlist)):
                    
                    roi_label = self.target_ROIlist[roi_r]
                    row_idx = self.ROIdict.get(roi_label)
                
                    corr = self.rawcorr[col_idx, row_idx, session]
                    
                    self.target_matrix[roi_c, roi_r, session] = corr
        
        #replace 1s with 0s for self-self correlations
        np.place(self.target_matrix,self.target_matrix == 1, [0])
        #make target matrix with abs vals
        #self.target_matrix_abs = np.absolute(self.target_matrix)
        
        return self.target_matrix

##ARG PARSE
if __name__ == "__main__":
# main section of code
            
    # parser code
    parser = argparse.ArgumentParser()
    
    parser.add_argument("npyfile", 
                        help="npy file with correlation data")
    parser.add_argument("roifile", 
                        help="roi csv file")
    parser.add_argument("targetroi", 
                        help="list of target roi's in csv file")
    parser.add_argument("sessionfile", 
                        help="session csv file containing subjectid, timepont")
    parser.add_argument("-v", "--verbosity",
                        help="increase output verbosity")
    parser.add_argument("-t", "--test", action="store_true",
                        help="special testing flag for developer")
    args = parser.parse_args()
    
if args.test:
    # use test arguments 
    args.npyfile = 'big_matrix.npy'
    args.roifile = 'all_rois.csv'
    args.targetroi = 'yeo17_rois.csv'
    args.sessionfile = "sessions_20190129.csv"
    
# specify default value for args.verbosity if not set
# args are of type string
if not args.verbosity:
    args.verbosity = '1'
    
# create a dataset object, providing file arguments
bam = BuildAdjMatrix(args.npyfile, args.roifile, args.targetroi,
                args.connectfile, verbosity=int(args.verbosity))
        

print(bam.npy_file)

# load the files
if bam.load_files():
    
    data = bam.retrieve_target_matrix
    
    