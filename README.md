# buildAdjMatrix
Takes a large adjacency matrix containing all ROIs and creates a smaller matrix with just the ROIs of interest
Inputs/Arguments:
-	npyfile : big adjacency matrix with all ROIs
-	roifile: csv file containing the list of all ROIs
-	targetroi: csv file containing list of target ROIs
-	sessionfile: file containing information regarding sessions. Must have column names ‘grid’, ‘timepoint’ and ‘group’

EXAMPLE WITH SPROVIDED SAMPLE DATA:

#instantiate BulildAdjMatrix.py with inputs
>> bam = BuildAdjMatrix('big_matrix.npy', 'all_rois.csv', 'yeo17_rois.csv', 'test_sessions.csv')

#load files
>> bam.load_files()

#Extract target adjacency matrix (resulting matrix should havr 17 rois)
>> data = bam.retrieve_target_matrix()
