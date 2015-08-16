from brainbehavior.cognitiveatlas import get_expanded_family_dict, get_path_similarity_matrix
from brainbehavior.nlp import get_term_counts, do_stem, get_total_words
from unittest import TestCase
from glob import glob
import pickle
import praw
import pandas
import sys
import os

class RedditTest(TestCase):

    def setUp(self):
        term_pickle = "../brainbehavior/data/cognitiveatlas/behavioraltraits.pkl"
        self.terms = pickle.load(open(term_pickle,"rb"))
        self.stems = do_stem(self.terms)

    def test_reddit(self):

        ### COMBINE COUNTS BY FAMILY ##############################################################
        # Prepare behavioral terms
        pickles = glob("output/*_dict_counts.pkl")
        families = get_expanded_family_dict(unique=True)

        # This is NOT a diagonal matrix, base terms are in rows, family members in columns
        path_similarities = get_path_similarity_matrix()

        for result_file in pickles:
            tmp = pickle.load(open(result_file,"rb"))
            print "Combining family counts for %s" %tmp["disorder"]
            result = tmp["dfcount"]
            # This will be a new matrix with only base terms as column names
            familydf = pandas.DataFrame(index=result.index)
            # Step 2: For each term stem (row), find family based on path similarity
            for stem,data in families.iteritems():
                family = path_similarities[stem][path_similarities[stem] != 0]
                # Create a data frame with just the columns
                column_names = [c for c in family.index if c in result.columns]
                family = family[column_names]
                # if there are no family members
                if family.shape[0] == 0: 
                    familydf[stem] = result[stem]
                # Weight each count by the path similarity, and sum
                else:
                    subset = result[column_names].copy()
                    for col in subset.columns:
                        subset[col] *= family[col]
                    familydf[stem] = subset.sum(axis=1) + result[stem] 
            # Save family data frame to file
            tmp["familydf"] = familydf
            pickle.dump(tmp,open(result_file.replace("dict_counts","dict_counts_family"),"wb"))    

            ### 4. CO-OCCURRENCE ##################################################################
            # Now calculate co-occurrence
            terms = familydf.columns.tolist()

            # Result df will be terms by terms
            df = pandas.DataFrame(columns=terms,index=terms)

            for t in range(0,len(terms)):
                term1 = terms[t]
                print "Calculating co-occurrence for %s" %(term1)
                subset = familydf.loc[familydf[term1]>0]
                number_with_term1 = subset.shape[0]
                if number_with_term1 != 0:
                    for term2 in terms:
                        number_with_term2 = subset[term2].loc[subset[term2]>0].shape[0]
                        pt2_given_t1 = float(number_with_term2) / number_with_term1
                        # [row](probability), [col](given)
                        df.loc[term2,term1] = pt2_given_t1    
                else:
                    df.loc[:,term1] = 0

            df.to_csv("output/%s_co-occurrence.tsv" %tmp["disorder"],sep="\t")
        print "Finished."
        pass
        os.system("Rscript prep_cooccurr_data.R")
    
