import os

raw_directory = '/home/julius/ScienceBowl/ScienceBowlFormat/raw'
new_directory = '/home/julius/ScienceBowl/ScienceBowlFormat/new'


def get_new_filename(short_filename):
    short_to_long = {
        'astr': 'astronomy',
        'genr': 'general_science',
        'biol': 'biology',
        'chem': 'chemistry',
        'phys': 'physics',
        'ersc': 'earth_and_space_science',
    }
    if short_filename in short_to_long.keys():
        return short_to_long[short_filename]
    else:
        return 'unknown'


def main():
    cwd = os.getcwd()
    for raw_file in os.listdir(raw_directory):
        os.chdir(raw_directory)
        correct_choices = [
            'a)',
            'b)',
            'c)',
            'd)',

        ]
        wrong_choices = {
            'w)': 'a.',
            'x)': 'b.',
            'y)': 'c.',
            'z)': 'd.',
        }
        wrong_answers = {
            'W': 'A',
            'X': 'B',
            'Y': 'C',
            'Z': 'D',
        }
        raw_filename = os.fsdecode(raw_file)
        if raw_filename.endswith(".txt"):
            short_filename = raw_filename[3:7]
            new_filename = get_new_filename(short_filename) + '.rtf'
            new_lines = [
                'Science Bowl ' + get_new_filename(short_filename).capitalize() + '\n',
                '\n',
                'Multiple Choice\n',
                '\n'
            ]
            counter = 1
            with open(file=raw_filename, mode='r', errors='ignore') as raw:
                between = False
                is_not_mc = False
                for raw_line in raw:  # select relevant lines
                    mid_line = raw_line
                    if mid_line.startswith(' '):
                        mid_line = mid_line[1:]
                    if mid_line == '\n':
                        continue

                    new_line = mid_line
                    if mid_line[:2] != 'z)' and mid_line[:2] != 'd)' and new_lines[-1][:2] == 'c.':
                        new_lines.append('d. none of the above\n')



                    if mid_line[:2] in correct_choices and not is_not_mc:
                        new_line = mid_line[:1] + '.' + mid_line[2:]
                        if new_line[:2] == 'a.':
                            new_lines[-1] = new_lines[-1] + '\n'
                        if new_line[2] != ' ':
                            new_line = new_line[:2] + ' ' + new_line[2:]
                        is_not_mc = False
                        between = False
                    elif mid_line[:2] in wrong_choices.keys() and not is_not_mc:
                        new_line = wrong_choices[mid_line[:2]] + mid_line[2:]
                        if new_line[:2] == 'a.':
                            new_lines[-1] = new_lines[-1] + '\n'
                        if new_line[2] != ' ':
                            new_line = new_line[:2] + ' ' + new_line[2:]
                        is_not_mc = False
                        between = False
                    elif mid_line.startswith('ANSWER:'):
                        if is_not_mc:
                            new_line = ''
                        else:
                            if mid_line[8] in wrong_answers.keys():
                                new_line = 'ANS: ' + wrong_answers[mid_line[8]] + '\n'
                            else:
                                new_line = 'ANS:' + mid_line[7:9] + '\n'
                            new_line = new_line + 'TOP: ' + short_filename.upper() + '\n'
                        is_not_mc = False
                        between = False
                    elif 'Short Answer:' in mid_line or 'True-False:' in mid_line:
                        new_line = ''
                        is_not_mc = True
                    elif mid_line.startswith(short_filename.upper()) and 'Short Answer:' not in mid_line and \
                            'True-False:' not in mid_line and 'Multiple Choice:' not in mid_line:
                        new_line = ''
                        is_not_mc = True
                    elif mid_line.startswith(short_filename.upper()):
                        new_line = str(counter) + '. ' + mid_line[26:-2]
                        counter += 1
                        between = True
                    elif is_not_mc:
                        new_line = ''
                    elif between:
                        new_line = mid_line[:-2]
                    else:
                        new_line = ''
                    if new_line != ' ':
                        new_lines.append(new_line)
            os.chdir(new_directory)
            if counter <= 250:
                with open(new_filename, 'w+') as new:
                    new.writelines(new_lines)
            else:
                top_lines = new_lines[:4]
                questions = new_lines[4:]

                count = 1
                for num in range(len(questions)):
                    if questions[num].startswith(str(count) + '. '):
                        dot = questions[num].find('.')
                        number = questions[num][:dot]
                        remainder = int(number) % 250
                        if remainder == 0:
                            remainder += 250
                        questions[num] = str(remainder) + questions[num][dot:]
                        count += 1

                cutoffs = []
                limit = 1
                for num in range(len(questions)):
                    if questions[num].startswith('1. '):
                        cutoffs.append(num)
                        limit += 1
                cutoffs.append(len(questions) - 1)

                index = 0
                chunks = counter // 250 + 1
                for chunk in range(chunks):
                    chunk_filename = new_filename[:-4] + str(chunk+1) + '.rtf'
                    start = cutoffs[index]
                    end = cutoffs[index+1]
                    with open(chunk_filename, 'w+') as new:
                        new.writelines(top_lines)
                        new.writelines(questions[start:end])
                    index += 1
    os.chdir(cwd)


if __name__ == '__main__':
    main()
