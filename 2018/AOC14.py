def test_recipes(n_recipes):
    score = [3, 7]
    worker1, worker2 = 0, 1

    for _ in range(30222333): # 10000000000 50222333
        if _ % 864801 == 0:
            print(_, worker1, worker2, len(score))
        score1, score2 = score[worker1], score[worker2]
        new_recipe = str(score1 + score2)
        for r in new_recipe:
            score.append((int(r)))

        worker1 = (worker1 + score[worker1] + 1) % len(score)
        worker2 = (worker2 + score[worker2] + 1) % len(score)
        #worker_position = [(v + score[v] + 1) % len(score) for ix, v in enumerate(worker_position)]

    #return ' '.join([str(s) for s in score[n_recipes:n_recipes+10]])
    return ''.join([str(s) for s in score])

if __name__ == "__main__":
    n_recipes = 864801
    sol1 = test_recipes(864801)
    print(f'PART 1: {sol1[864801:864801+10]}')  # '1611732174'

    sol2 = sol1.find(str(n_recipes)) # 20279772
    print(f'\n PART 2: {sol2}')
