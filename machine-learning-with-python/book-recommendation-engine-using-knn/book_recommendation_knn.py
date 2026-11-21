import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

books = pd.read_csv('books.csv', on_bad_lines='skip')
ratings = pd.read_csv('ratings.csv', on_bad_lines='skip')


def get_recommends(book=''):
    """返回 [书名, [[推荐书名, 距离], ...]]，共 5 本书。"""
    if book not in set(books['title']):
        raise ValueError('unknown book: ' + str(book))

    book_id = books.loc[books['title'] == book, 'book_id'].iloc[0]

    # 用户-图书评分矩阵
    matrix = ratings.pivot_table(index='user_id', columns='book_id', values='rating').fillna(0)
    if book_id not in matrix.columns:
        return [book, []]

    model = NearestNeighbors(n_neighbors=6, metric='cosine').fit(matrix.T.values)
    distances, indices = model.kneighbors(matrix.T.loc[[book_id]].values)

    recommendations = []
    for distance, index in zip(distances[0][1:], indices[0][1:]):
        title = books.loc[books['book_id'] == matrix.columns[index], 'title'].iloc[0]
        recommendations.append([title, float(distance)])

    return [book, recommendations]
