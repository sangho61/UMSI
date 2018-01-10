# gradepredict.py

# get data into program
# return: dictionary with keys: assignment group names,
#                    values: lists of scores

def get_data():
    pass


# identify and drop lowest grades for discussion, homeworks, lecture exercises
# params: a list of scores, number to drop
# returns: list of scores, with the lowest dropped
def drop_lowest_scores(list_of_scores):
    pass

# param: list for a compute_grade
# returns: total for that score


# total all the points
# convert to percentage
# convert to letter grade
def compute_grade(total_scores):
    pass

def test_functions():
    # test drop_lowest_scores
    list1 = [10, 9, 8, 7, 6]
    expected_return1 = [10, 9, 8]
    expected_return2 = [10]
    expected_return3 = 5

    passed = 0
    failed = 0

    if drop_lowest_scores(list1, 2) == expected_return1:
        # test passed
        passed += 1
    else:
        # test failed
        failed += 1
        print('Failed test 1')

    if drop_lowest_scores(list1, 4) == expected_return2:
        # test passed
        passed += 1
    else:
        # test failed
        failed += 1
        print('Failed test 1')

    if compute_grade(list1) == expected_return3:
        # test passed
        passed += 1
    else:
        # test failed
        failed += 1
        print('Failed test 1')

data_dict = get_data()

homework_scores = drop_lowest_scores(data_dict['homeworks'], 2)
lecture_scores = drop_lowest_scores(data_dict["lectures"], 4)
discussion_scores = drop_lowest_scores(data_dict["discussion"], 2)
midterm_scores = data_dic["midterm"]
project_scores = data_dict["projects"]
final_score= data_dict["final_project"]

# compute total scores

# compute_grade
