# Taiyo Hayes, tjhayes@usc.edu
# ITP 216, Fall 2022
# Section: 32081
# Assignment 3
# Description: Find all above average Robert De Niro Movies

# read in the deniro file, then separate out and return the header and the movies as lists
def file_reader(fileName="deniro.csv"):
    # initialize empty list for the movies
    dataList = []
    with open(fileName, 'r') as f_in:
        # read in the header and process/format
        header = f_in.readline()
        headerList = header.strip().split(', ')
        # for every line after the first one, process and format each line into a list
        for line in f_in:
            dataList.append(line.strip().split(', ', 2))
    f_in.close()
    # return the 2 lists
    return headerList, dataList

# calculate the mean score of each deniro movie, given a list of the scores (ints)
def calculate_mean(scoreList):
    # initialize the sum to zero
    totalScore = 0
    # for every score in the list, add it to the sum
    for score in scoreList:
        totalScore += score
    # sum divided by the number of items gives the average
    return totalScore / len(scoreList)

# use the mean to identify each movie that is above average, and add it to a list
def find_movies_above_score(movies, mean):
    # initialize list for the above average movies
    goodMovies = []
    # for each movie, check if the score is above the mean; if so, add it to the new list
    for movie in movies:
        if float(movie[1]) > mean:
            goodMovies.append(movie)
    return goodMovies

def main():
    # get the header list and movie list
    header, data = file_reader()
    # initialize a list to to hold the score of each movie
    scoreList = []
    # for each movie in the movie list, add its score to the score list
    for movie in data:
        scoreList.append(int(movie[1].strip()))
    # pass in the list of scores to get the score average
    mean = calculate_mean(scoreList)
    # pass in the list of all movies and the movie score average to get the list of all above average movies
    goodMovies = find_movies_above_score(data, mean)

    # output the proper messages to the user given the findings in the code
    print("I love Robert Deniro")
    print("The average Rotten Tomatoes score for his movies is " + str(mean) + ".")
    print("Of", len(data), "movies,", len(goodMovies), "are above average.")
    print("Here they are:")
    print("\t\t" + header[0] + "\t\t" + header[1] + "\t\t" + header[2])
    for goodMovie in goodMovies:
        print("\t\t" + goodMovie[0] + "\t\t" + goodMovie[1].strip() + "\t\t" + goodMovie[2])

if __name__ == '__main__':
    main()
