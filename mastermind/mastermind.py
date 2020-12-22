
def respond_to_guess(guess, target):
    '''
    Parameters:
        guess: a valid combination (list of colors)
        target: a valid combination
        
    Returns:
        Number of correct positions
        Number of incorrect positions
    
    '''
    n = len(guess)
    to_check = []
    correct = 0
    incorrect = 0
    
    # Compute correct positions
    for i in range(n):
        if guess[i] == target[i]:
            correct += 1
        else:
            to_check.append(i)
    
    # Compute incorrect positions
    to_check_guess = to_check[:]
    to_check_target = to_check[:]
    for i_color in to_check_target:
    while(to_check_target):
        print(i_color, len(to_check))
        target_color = target[i_color]
        for index_i, j_color in enumerate(to_check_guess):
            if target_color == guess[j_color]:
                incorrect += 1
                # to_check.pop(index_i)
                break
    
        
    return correct, incorrect
    
    
def test():
    guess_target_test_values = [
        # ([1, 2, 3, 4], [1, 2, 3, 4]),
        # ([1, 2, 4, 3], [1, 2, 3, 4]),
        # ([1, 2, 2, 2], [1, 2, 3, 4]),
        # ([1, 4, 2, 2], [1, 2, 3, 4]),
        # ([1, 4, 2, 2], [1, 2, 2, 4]),
        # ([1, 4, 4, 2], [1, 2, 2, 4]),
        ([1, 4, 3, 2], [1, 2, 2, 4]),
        ([2, 4, 3, 2], [1, 2, 2, 4]),
    ]
    
    
    for guess, target in guess_target_test_values:
        print(guess, target, respond_to_guess(guess, target))
    
    
if __name__ == '__main__':
    test()
    