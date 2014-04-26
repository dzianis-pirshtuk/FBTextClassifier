FBTextClassifier
================

EECS 498 (Intro. to Information Retrieval) Final Project: Text classification applied to social media


SQL Classifier
==============

The queries in rocchio.sql will build the necessary views to perform classification on gender with 10,000 users. 

After running the setuptables script (with sudo), you can then perform sql-based classification

You can run these queries using psql and PostgreSQL, and they should finish in several hours. The result will be a count of correctly predicted users (out of 1000 test, by default)