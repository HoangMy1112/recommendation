import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from numpy.linalg import norm

class MatrixFactorization:
    def __init__(self, data_frame, K=3, lamda=0.01, gamma=0.0007, steps=100):
        self.sample_pivot = data_frame.pivot(index='UserID', columns='PlaceID', values='Rating').fillna(0)
        self.user_list = list(self.sample_pivot.index)
        self.product_list = list(self.sample_pivot.columns)
        self.R = coo_matrix(self.sample_pivot.values)
        self.K = K
        self.lamda = lamda
        self.gamma = gamma
        self.steps = steps
        self.P = None
        self.Q = None

    def _error(self):
        ratings = self.R.data
        rows = self.R.row
        cols = self.R.col
        e = 0 
        for ui in range(len(ratings)):
            rui = ratings[ui]
            u = rows[ui]
            i = cols[ui]
            if rui > 0:
                e += (rui - np.dot(self.P[u, :], self.Q[:, i]))**2 + \
                     self.lamda * (norm(self.P[u, :])**2 + norm(self.Q[:, i])**2)
        return e

    def train(self):
        M, N = self.R.shape
        self.P = np.random.rand(M, self.K)
        self.Q = np.random.rand(self.K, N)

        for step in range(self.steps):
            for ui in range(len(self.R.data)):
                rui = self.R.data[ui]
                u = self.R.row[ui]
                i = self.R.col[ui]
                if rui > 0:
                    eui = rui - np.dot(self.P[u, :], self.Q[:, i])
                    self.P[u, :] += self.gamma * 2 * (eui * self.Q[:, i] - self.lamda * self.P[u, :])
                    self.Q[:, i] += self.gamma * 2 * (eui * self.P[u, :] - self.lamda * self.Q[:, i])
            rmse = np.sqrt(self._error() / len(self.R.data))
            if rmse < 0.5:
                break
            print(f'Step {step+1}, RMSE: {rmse}')

    def predict(self):
        all_user_ratings = np.dot(self.P, self.Q)
        return pd.DataFrame(np.round(all_user_ratings, 2), columns=self.product_list, index=self.user_list)

if __name__ == "__main__":
    df = pd.read_csv('./sample.csv')
    mf = MatrixFactorization(df, K=3, gamma=0.0007, lamda=0.01, steps=100)
    mf.train()
    predictions = mf.predict()
    user_id = 'A10KH8EN77ZKWH'
    top_five = predictions.loc[user_id].sort_values(ascending=False).head(5)
    print(f"Top 5 recommendations for user '{user_id}':", top_five)

# import pandas as pd
# import numpy as np

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# class CollaborativeFiltering:
#     def __init__(self, data_frame):
#         self.matrix_df = data_frame.pivot_table(index=["UserID"], columns=["PlaceID"], values="Rating")
#         self.matrix_df.fillna(0, inplace=True)
#         self.item_similarity = cosine_similarity(self.matrix_df.T)

#     def get_item_based_recommendations(self, user_id, top_n=5):
#         user_idx = self.matrix_df.index.get_loc(user_id)

#         user_ratings = self.matrix_df.iloc[user_idx].values

#         weighted_sum = np.dot(self.item_similarity, user_ratings) / self.item_similarity.sum(axis=1)

#         not_rated_indices = user_ratings == 0

#         recommendations = np.argsort(weighted_sum[not_rated_indices])[::-1][:top_n]

#         recommended_product_ids = self.matrix_df.columns[recommendations].tolist()

#         return recommended_product_ids

# if __name__ == "__main__":
#     df = pd.read_csv('./sample.csv');

#     model = CollaborativeFiltering(df)

#     recommendations = model.get_item_based_recommendations('A10E3QH2FQUBLF')
#     print("Recommendations for user 'A10E3QH2FQUBLF':", recommendations)