import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv(r"C:\\Users\\shivani.padal\\Downloads\\movies_complete.csv", parse_dates=['release_date'])
df['Year'] = df.release_date.dt.year
df['Year'].fillna(0, inplace=True)
df['Year'] = df['Year'].astype(int)
print(df['Year'].head())


# df_best = df[["poster_path", "title", "budget_musd", "revenue_musd",
            #   "vote_count", "vote_average", "popularity"]].copy()

df_best = df[[ "title", "budget_musd", "revenue_musd",
              "vote_count", "vote_average", "popularity"]].copy()

df_best['profit_musd'] = df.revenue_musd.sub(df.budget_musd)
df_best['return'] = df.revenue_musd.divide(df.budget_musd)

# df_best.columns = ['','Title', 'Budget', 'Revenue', 'Votes', 'Average Rating', 'Popularity', 'Profit', 'ROI']

df_best.columns = ['Title', 'Budget', 'Revenue', 'Votes', 'Average Rating', 'Popularity', 'Profit', 'ROI']

df_best.set_index('Title', inplace=True)

df_best.Budget.fillna(0, inplace=True)

df_best.Votes.fillna(0, inplace=True)

print(df_best.head())


def best_worst(df, n, by , ascending=False):
    return df.sort_values(by = by, ascending=ascending).head(n)

#Highest_revenue 
print('-------------Highest Revenue---------------')
print(best_worst(df_best, 5, by= 'Revenue'))

#Highest budget 
print('-------------Highest budget---------------')
print(best_worst(df_best, 5, by='Budget'))

#Lowest Profit 
print('-------------Lowest Profit---------------')
print(best_worst(df_best,5,by='Profit', ascending=True))

#Highest ROI
print('-------------Highest ROI---------------')
df_minbud_50 = df_best[df_best.Budget >= 50]
print(best_worst(df_minbud_50, 5, by='ROI'))


#Lowest ROI 
print('-------------Lowest ROI---------------')
print(best_worst(df_minbud_50, 5, by='ROI', ascending=True))

#Most Votes 
print('-------------Most Votes---------------')
print(best_worst(df_best, 5, by='Votes'))

#Highest rating 
print('-------------Highest Rating---------------')
df_min_vote = df_best[df_best['Average Rating'] >= 10]
print(best_worst(df_min_vote, 5, by='Average Rating'))

#Lowest Rating 
print('-------------Lowest Rating---------------')
print(best_worst(df_min_vote, 5, by ='Average Rating', ascending=True))

#Most Popular 
print('------------Most Popular---------------')
print(best_worst(df_best, 5, by= 'Popularity'))

 
#############################

df_movie = df[['revenue_musd', 'title', 'Year','genres','original_language','runtime', 'spoken_languages', 'cast', 'director', 'vote_average', 'production_companies', 'release_date' ]]
df_movie['revenue_musd'].fillna(0, inplace=True)
# print(df_movie.head(5))

#1. Science Fiction Action Movie with Bruce Willis (sorted from high to low Rating)

generes_cond = df_movie.genres.str.contains('Science Fiction') & df_movie.genres.str.contains('Action')

cast_cond = df_movie.cast.str.contains('Bruce Willis')

print("1.bruce willis")

bruce = df_movie.loc[generes_cond & cast_cond, ['title', 'cast', 'genres', 'vote_average']].sort_values(by='vote_average', ascending=False)

print(bruce.head())

#2. Movies with Uma Thurman and directed by Quentin Tarantino (sorted from short to long runtime)

cast_cond = df_movie.cast.str.contains('Uma Thurman')
director_cond = df_movie['director'] == 'Quentin Tarantino'

print("2.Uma Thurman")
print(df_movie.loc[cast_cond & director_cond, ['title','director', 'cast', 'runtime']].sort_values(by= 'runtime'))


#3. Most Successful Pixar Studio Movies between 2010 and 2015 (sorted from high to low Revenue)

year_cond = (df_movie['Year'] >= 2010) & (df_movie['Year'] <= 2015)
# mask = (df_movie['Year'] > start_date) & (df['date'] <= end_date)

df_movie['revenue_musd'].fillna(False)
# print(df_movie[year_cond])
prd_company = df_movie.production_companies.str.contains('Pixar').fillna(0)
print("3. Pixar Studio Movies")

print(df_movie.loc[year_cond &  prd_company,  ['revenue_musd', 'title', 'vote_average']].sort_values(by='revenue_musd', ascending=False))

# # sort_values(by='vote_average',ascending=False)


# 4.  Action or Thriller Movie with original language English and minimum Rating of 7.5

genres_cond = (df_movie.genres.str.contains('Action')) | (df_movie.genres.str.contains('Thriller'))

org_lan_cond = df_movie.original_language == 'en'

vote_avg_cond = df_movie.vote_average >= 7.5 

# print(df_movie.head(10))

print('4. Action, Thriller, English movie')
print(df_movie.loc[genres_cond & org_lan_cond & vote_avg_cond, ["title",  "genres", "vote_average", 'release_date']].sort_values(by='release_date', ascending=False))


## Are Franchises more successful?
####
df['Franchises'] = df.belongs_to_collection.notna()


#mean revenue 
# print(df.groupby('Franchises').revenue_musd.mean())  

#median Return on Investment
df['ROI'] = df.revenue_musd.div(df.budget_musd)

# print(df.groupby('Franchises').ROI.median())

#mean budget raised 

# print(df.groupby('Franchises').budget_musd.mean())

#mean popularity
# print(df.groupby('Franchises').popularity.mean())

#mean rating
# print(df.groupby('Franchises').vote_average.mean())

##Overall( wecan do above all steps in one step using agg )

print(df.groupby('Franchises').agg({'budget_musd': 'mean',
                              'revenue_musd': 'mean',
                              'vote_average': 'mean',
                              'popularity': 'mean',
                              'ROI': 'median',
                              'vote_count': 'mean'}))


#Most Successful Franchises 

Franchises = df.groupby('belongs_to_collection').agg({'title': 'count',
                              'budget_musd':['count', 'mean'],
                               'revenue_musd' : ['count', 'mean', 'sum'],
                               'vote_average': 'mean'})

# print(Franchises.sort_values(by=('title','count'), ascending=False))

print(Franchises.nlargest(20, ('title','count')))

print(Franchises.nlargest(20, ('revenue_musd','sum')))

# print(Franchises.nlargest(20, ('budget_musd','sum')))


#Most succesful directories : 

directors = df.groupby('director').agg({'title':'count', 'revenue_musd': 'sum', 'vote_average': 'mean'})

print(directors)

print(directors.nlargest(20, ('title')))


print(directors.nlargest(20, ('revenue_musd')))

print(directors.nlargest(20, ('vote_average')))
