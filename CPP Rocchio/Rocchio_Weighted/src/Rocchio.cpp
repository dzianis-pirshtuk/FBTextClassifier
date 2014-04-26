//============================================================================
// Name        : Rocchio.cpp
// Author      : Noah E. Crocker
// Version     : 2.000001
//============================================================================

#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include <boost/unordered_map.hpp>
using namespace std;
using namespace boost;


struct demoginfo {
	string userid;
	int attribute;
};

void loadData(unordered_map<string, unordered_map<string, double>> &user_status_tf,
		unordered_map<string, int> &user_status_idf,
		vector<demoginfo> &user_demog,
		unordered_map<int, int>& prior) {

	ifstream user_demog_file("../demog_proc.csv");
	if(user_demog_file.bad()){
		cout << "Error opening demog_proc.csv\n";
		exit(1);
	}
	ifstream user_status_tf_file("../user_status_tf_proc.csv");
	if(user_status_tf_file.bad()){
		cout << "Error opening user_status_tf.csv\n";
		exit(1);
	}
	string line;


	//Load demographic data
	cout << "Loading DEMOG info\n";
	while(getline(user_demog_file, line)){
		demoginfo toInsert;
		toInsert.userid = line.substr(0, 32);
		toInsert.attribute = atoi(line.substr(33).c_str());
		user_demog.push_back(toInsert);
		prior[toInsert.attribute] += 1;
		//cout << toInsert.userid << " " << line.substr(33).c_str() << endl;
		//usleep(100000);
	}
	cout << "Done loading DEMOG info\n";

	//Load user status TF values
	cout << "Loading user_status_tf\n";
	int i = 0;
	while(getline(user_status_tf_file, line)){
		string userid = line.substr(0, 32);
		int cnttermidx = line.find_first_of(',', 33);
		int count = atoi(line.substr(33, cnttermidx-33).c_str());
		string term = line.substr(cnttermidx+1);
		//cout << term << endl;
		if(i % 1000000 == 0)
			cout << i << endl;
		++i;
		user_status_tf[userid][term] = log(count+1);
		user_status_idf[term] += 1;
	}

	cout << "Done loading user_status_tf\n";

}

double getScore(unordered_map<string, double> &user_tf, unordered_map<string, double> &repVect,
		unordered_map<string, int> &user_status_idf, double logtrainingSize, double repVectLength,
		int& prior, double probWeight = 0.04){
	double score = 0;
	double userlen = 0;

	for(auto it = user_tf.begin(); it != user_tf.end(); ++it){
		//Here we add in tf-idf for the user (calculated on the fly) and the tf-idf for the repvector (already calculated)
		if(user_status_idf[it->first] == 0)
			continue;
		double userWeight = it->second * (logtrainingSize - log(user_status_idf[it->first]));
		score += userWeight * repVect[it->first];

		//We also keep track of the vector length for the user
		userlen += pow(userWeight, 2);


		//cout << it->first << "\t\t\t" << it->second << "\t\t\t" << user_status_idf[it->first] << "\t\t\t" << userWeight << "\t\t\t" << score << "\t\t\t" << userlen << endl;
		//usleep(250000);
	}

	userlen = sqrt(userlen);
//	cout << "FINAL USER LEN " << userlen << endl;
//
//	//Normalize for length
	//cout << "PRE ADJUSTED SCORE " << score << endl;
	score /= (repVectLength*userlen);
	score = ((1 - probWeight) * score) + (probWeight * exp(log(prior) - logtrainingSize));

	//double invcos = acos(score);
	//invcos *= (1 - exp(log(prior) - logtrainingSize));
	//score = cos(invcos);
//	cout << "UNWEIGHTED SCORE: " << score << endl;
//	score *= prior;
	//cout << "SCORE div " << repVectLength << " * " << userlen <<" = "<< repVectLength*userlen << endl;
	//cout << "WEIGHTED SCORE: " << score << endl;
	//sleep(2);

	return score;
}

int nIteration(unordered_map<string, unordered_map<string, double>> &user_status_tf,
		unordered_map<string, int> &user_status_idf,
		vector<demoginfo> &user_demog,
		int lbTest,
		int ubTest,
		unordered_map<int, unordered_map<string, double>> &repVect,
		unordered_map<int, int>& prior) {

	double logtrainingSize = log(user_demog.size() - (ubTest- lbTest));
	int numCorrect = 0;

	cout << "    [*] Subtracting TEST IDF from TRAINING IDF\n";
	cout << "    [*] Subtracting TF of TEST from REPVECTOR" << endl;
	//cout << lbTest << " " << ubTest << endl;
	for(int i = lbTest; i < ubTest; ++i){
		//cout << i << " " << user_demog[i].userid << endl;
		//if(i % 10000 == 0)
		//	cout << i - lbTest << " " << ubTest - lbTest<<  endl;
		for(auto it = user_status_tf[user_demog[i].userid].cbegin(); it != user_status_tf[user_demog[i].userid].cend(); ++it){
			//cout << it->first << endl;
			--user_status_idf[it->first];
			repVect[user_demog[i].attribute][it->first] -= it->second;
		}
		--prior[user_demog[i].attribute];
	}

	cout << "    [*] Multiplying TRAINING IDF into training vectors" << endl;
	unordered_map<int, double> repVectLengths;
	for(auto vect = repVect.begin(); vect != repVect.end(); ++vect){
		//For each distinct attribute value
		//int i = 0;
		for(auto vectTF = vect->second.begin(); vectTF != vect->second.end(); ++vectTF){
			//For each term associated with that attribute value, multiply in the IDF
			if(user_status_idf[vectTF->first] == 0 || log(user_status_idf[vectTF->first]) == logtrainingSize)
				continue;
			vectTF->second *= logtrainingSize - log(user_status_idf[vectTF->first]);
			if(!isfinite(vectTF->second)){
				cout << "A REP VECTOR WENT NAN: " << vectTF->first << endl;
				exit(1);
			}
			//usleep(100000);
			repVectLengths[vect->first] += pow(vectTF->second, 2);
		}
		repVectLengths[vect->first] = sqrt(repVectLengths[vect->first]);
	}


	cout << "    [*] Attempting to classify testing fold" << endl;
	unordered_map<int, int> numPredictions;
	for(int i = lbTest; i < ubTest; ++i){
		if(i % 10000 == 0)
			cout << i << endl;
		double maxSim = -1;
		int prediction = -1;
		//cout << "AcTUAL: " << user_demog[i].gender << endl;
		for(auto it = repVect.begin(); it != repVect.end(); ++it){
			double sim = getScore(user_status_tf[user_demog[i].userid], it->second, user_status_idf, logtrainingSize, repVectLengths[it->first], prior[it->first]);
			if(!isfinite(sim)){
				cout << "A PREDICTION WENT NAN, USER: " << i << endl;
				//exit(1);
			}
			//cout << it->first << " " << sim << endl;
			if(sim > maxSim){
				maxSim = sim;
				prediction = it->first;
			}
		}
		//cout << endl;
		numPredictions[prediction] += 1;
		if(prediction == user_demog[i].attribute)
			numCorrect +=1;
		//sleep(1);
	}

	cout << "PREDICTION SUMMARY: " << endl;
	for(auto it = numPredictions.cbegin(); it != numPredictions.cend(); ++it){
		cout << "attr: " << it->first << " num: " << it->second << endl;
	}


	cout << "    [*] Dividing IDF out of training vectors" << endl;
	for(auto vect = repVect.begin(); vect != repVect.end(); ++vect){
		//For each distinct attribute value
		//int i = 0;
		for(auto vectTF = vect->second.begin(); vectTF != vect->second.end(); ++vectTF){
			//if(i++ % 10000 == 0)
			//	cout << i-1 << endl;
			if(user_status_idf[vectTF->first] == 0 || log(user_status_idf[vectTF->first]) == logtrainingSize)
				continue;
			vectTF->second /= logtrainingSize - log(user_status_idf[vectTF->first]);
		}
	}

	cout << "    [*] Restoring TRAINING IDF\n";
	//Now we add the IDF back in
	for(int i = lbTest; i < ubTest; ++i){
		//cout << i << " " << user_demog[i].userid << endl;
		//if(i % 10000 == 0)
		//	cout << i - lbTest << " " << ubTest - lbTest<<  endl;
		for(auto it = user_status_tf[user_demog[i].userid].cbegin(); it != user_status_tf[user_demog[i].userid].cend(); ++it){
			//cout << it->first << endl;
			++user_status_idf[it->first];
			repVect[user_demog[i].attribute][it->first] += it->second;
		}
		++prior[user_demog[i].attribute];
	}

	return numCorrect;

}

int main() {

	//Load the data
	unordered_map<string, unordered_map<string, double>> user_status_tf;
	unordered_map<string, int> user_status_idf;
	vector<demoginfo> user_demog;
	unordered_map<int, int> prior;
	loadData(user_status_tf, user_status_idf, user_demog, prior);


	//Perform N-Fold validation
	int numFolds;
	//cout << "Please enter number of folds" << endl;
	//cin >> numFolds;
	numFolds = 10;
	int foldSize = user_demog.size() / numFolds;
	cout << "Fold size: " << foldSize << endl;

	cout << "[+] Preping REPVECTORs\n";
	unordered_map<int, unordered_map<string, double>> repVect;
	for(int i = 0; i < foldSize*numFolds; ++i){
		if(i % 10000 == 0)
			cout << i << " " << user_demog.size() << endl;
		for(auto it = user_status_tf[user_demog[i].userid].cbegin(); it != user_status_tf[user_demog[i].userid].cend(); ++it){
			repVect[user_demog[i].attribute][it->first] += it->second;
			//cout << user_demog[i].attribute << endl << it->first << endl <<it->second << endl;
		}
	}


	int totalCorrect = 0;
	for(int i = 0; i < numFolds; ++i) {
		cout << "[+] Iteration " << i+1 << " of " << numFolds << endl;
		int numCorrectThisRound = nIteration(user_status_tf, user_status_idf, user_demog, i*foldSize, (i+1)*foldSize, repVect, prior);
		cout << "    [*] " << numCorrectThisRound << " / " << foldSize << " = " << (float) numCorrectThisRound/foldSize << endl;
		totalCorrect += numCorrectThisRound;
	}


	cout << "\n[+] DONE: " << totalCorrect << "/" << foldSize*numFolds << " = " << (float)totalCorrect/(foldSize*numFolds) << endl;


	return 0;
}
