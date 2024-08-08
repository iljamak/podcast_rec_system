import pandas as pd
import numpy as np
import random
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import math
def find_closest_by_category(itunes_id,dataset,top=10):
    def _find_closest_by_category(podcast_id, dataset: pd.DataFrame):
        try:
            code = int(podcast_id)
            row = dataset[dataset['itunes_id'] == code]
            if not row.empty:
                row_index = row.index[0]
            else:
                return None
        except ValueError:
            row = dataset[dataset['podcast_name'].str.contains(podcast_id)]
            if not row.empty:
                row_index = row.index[0]
            else:
                return None

        categories = dataset.loc[row_index, 'categories'].split(",")
        scores = np.zeros(dataset.shape[0])
        for index, podcast in dataset.iterrows():
            if podcast['itunes_id'] != podcast_id:
                categories_outer = podcast['categories'].split(",")
                for c in categories_outer:
                    if c in categories:
                        scores[index] += 1
        return scores

    def _similar_category(scores):
        scores_indexed = [(i,scores[i]) for i in range(len(scores))]
        scores_indexed = sorted(scores_indexed,key=lambda x:x[1],reverse=True)
        return scores_indexed

    def _find_similar_podcasts(dataset,similarity_tuple,top=10,):
        similar = [i[0] for i in similarity_tuple[:top]]
        return dataset.iloc[similar,:]

    scores = _find_closest_by_category(itunes_id,dataset)
    scores_indexed = _similar_category(scores)
    return _find_similar_podcasts(dataset,scores_indexed,top=top)


def get_most_popular(dataset,top=10):
    '''Returns random 10 podcasts from 200 most popular'''
    df = dataset
    df = df.sort_values(by='number_of_reviews',ascending=False,inplace=False)
    df = df[:200]
    lst200 = list(range(200))
    sample = random.sample(lst200,top)
    return df.iloc[sample,:]

def get_sbert_top(dataset,itunes_id,sbert_cos_sim,top=10):
    try:
        code = int(itunes_id)
        row = dataset[dataset['itunes_id'] == code]
        if not row.empty:
            row = row.index[0]
        else:
            row = None
            return None
    except ValueError:
        row = dataset[dataset['podcast_name'].str.contains(itunes_id)]
        if not row.empty:
            row = row.index[0]
        else:
            row = None
            return None
    indexed_embeddings = set((i,sbert_cos_sim[row][i]) for i in range(len(sbert_cos_sim[row])))
    sorted_emb = sorted(indexed_embeddings,key=lambda item:item[1],reverse=True)
    sorted_emb = sorted_emb[:top]
    indices = [sorted_emb[i][0] for i  in range(len(sorted_emb))]
    return dataset.iloc[indices,:]

def get_avg_wiki_emb_top(dataset, itunes_id, cosine_sim_matrix, top=10):
    '''
    Precomputed average embeddings of each podcast are used (To find more: Jupyter Notebook folder)
    Finds closest with cos similarity
    '''
    try:
        code = int(itunes_id)
        row = dataset[dataset['itunes_id'] == code]
        if not row.empty:
            row = row.index[0]
        else:
            row = None
            return None
    except ValueError:
        row = dataset[dataset['podcast_name'].str.contains(itunes_id)]
        if not row.empty:
            row = row.index[0]
        else:
            row = None
            return None

    indexed_embeddings = set((i, cosine_sim_matrix[row][i]) for i in range(len(cosine_sim_matrix[row])))
    sorted_emb = sorted(indexed_embeddings, key=lambda item: item[1], reverse=True)
    sorted_emb = sorted_emb[:top]
    indices = [sorted_emb[i][0] for i in range(len(sorted_emb))]
    return dataset.iloc[indices, :]

def text_to_recommendations(dataset,SBERT_embeddings,input_text,top=10):
    '''computes embedding of users's input and compares it with cos similarity with all podcasts'''
    model = SentenceTransformer('all-MiniLM-L6-v2')
    user_text_emb = model.encode(input_text)
    cosine_similarity_user = []
    for index, embedding in enumerate(SBERT_embeddings):
        cosine_similarity_user.append((index,
                                        cosine_similarity(user_text_emb.reshape(1, -1), embedding.reshape(1, -1))[0][0]))

    cosine_similariry_user = sorted(cosine_similarity_user, key=lambda x: x[1], reverse=True)
    indices = [i[0] for i in cosine_similariry_user[:50]]
    return dataset.iloc[indices,:].sort_values(by='number_of_reviews').iloc[:top,:]


def get_optimal_recommendations(dataset, sbert_cos_sim, itunes_id, top=10):
    '''
        Finds podcasts that share at least one common category and have more than 4 review
        applies SBERT cos similarity (number from 0 to 1) multiplies it by 10
        adds rating and log_20 of number of reviews. 20 reviews +1 point, 400 review +2 points etc
        return top10 by final score
        final_mark = 10*cos_sim + log_20(amount_reviews) + log_40(amount_podcasts) + avg_rating
        '''
    def at_least_one_category(x):
        categories = dataset.iloc[row, :]['categories']
        for i in x['categories'].split(','):
            if i in categories:
                return True
        return False

    def calculate_rating(x):
        ind = x.name
        x['final_rating'] = x['rating'] + math.log(x['number_of_reviews'], 20) + math.log(x['number_of_podcasts'],
                                                                                          40) + 10 * \
                            sbert_cos_sim[row][ind]
        return x

    try:
        code = int(itunes_id)
        row = dataset[dataset['itunes_id'] == code]
        if not row.empty:
            row = row.index[0]
        else:
            row = None
            return None
    except ValueError:
        row = dataset[dataset['podcast_name'].str.contains(itunes_id)]
        if not row.empty:
            row = row.index[0]
        else:
            row = None
            return None
    mask = dataset.apply(at_least_one_category, axis=1)
    filtered_dataset = dataset[mask]
    indices = filtered_dataset.index
    dataset = dataset.iloc[indices, :]
    dataset = dataset[(dataset['number_of_reviews'] > 4) & (dataset['number_of_podcasts'] > 5)]
    dataset = dataset.apply(calculate_rating, axis=1)
    sorted_ds = dataset.sort_values(by="final_rating", ascending=False)
    return sorted_ds.iloc[:top, :]

if __name__ == "__main__": #just testing functionlity
    print(find_closest_by_category(1200361736,'datasets/finalAndRatings.csv',top=10))