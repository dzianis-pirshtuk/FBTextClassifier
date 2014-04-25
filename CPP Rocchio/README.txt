To build, just run make

###############################################################################
Python Preprocessor: PyTokenSorter

Provided user_status and user_demog are extracted into the "CPP Rocchio"
folder, the preprocessor will generate the user status term frequency file
and the user demog file for the target variable (set at the top of the
preprocessor)

This implementation will load roughly 7GB of data, and run in 30 minutes to
1 hour 20 minutes (depending on the options used)

NOTE: when running on the age attribute, you need to change the demog_file
parsing to put them into groups to get the prediction accuracies in our paper

###############################################################################
Rocchio classifiers: Rocchio_raw and Rocchio_weighted

After the preprocessor is run, Rocchio_raw and Rocchio_weighted will run
10-fold cross validation on the processed datasets and print to STD out.

These implementations will load roughly 12GB of data (good luck running this on
CAEN...) and run in 6 minutes each.