from sys import path


def main():
    # from m import solve_puzzle
    check_dict = {}
    with open('unit_test_data.txt') as f:
        for sol_row in f.readlines():
            check_dict |= eval(sol_row)

    missing_answers = []
    for y in range(2015, 2026):
        path.append(f'{y}')
        for d in range(1, 26):
            if y == 2025 and d == 13:
                break
            act_ym = f'{y}{d:02}'
            try:
                m = __import__(f'{y}.day_{d:02}')
                answers = eval(f'm.day_{d:02}').solve_puzzle(f'{y}/input/input_{y}{d:02}.txt')
                if act_ym not in check_dict:
                    missing_answers.append('{' + f"'{act_ym}': {answers}" + '}')
                    print(f'\033[93mMissing answer: {act_ym}')
                elif check_dict[f'{act_ym}'] == answers:
                    print(f'\033[0;0mMatching answers: {act_ym} - {answers}')
                else:
                    print(f'\033[91mDifferent answers: {act_ym} - {answers} vs. {check_dict[act_ym]}')
            except Exception as e:
                print(f'\033[91mFail in execution: {y}{d:02} - {e}')
        path.remove(f'{y}')
    print('\033[0;0mMissing answers dicts:')
    for answers_to_add in missing_answers:
        print(answers_to_add)


if __name__ == '__main__':
    main()
