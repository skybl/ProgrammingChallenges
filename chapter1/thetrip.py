def readFile(filename=None):
    lines = [
        '3',
        '10.00',
        '20.00',
        '30.00',
        '4',
        '15.00',
        '15.01',
        '3.00',
        '3.01',
        '0'
    ]

    numberStudents, sum, students = None, None, None
    for line in lines:
        try:
            if numberStudents == None:
                numberStudents = int(line)
                if numberStudents > 1000:
                    raise Exception('Number of students should not exceed 1000', numberStudents)
                sum = 0.0
                students = []
            else:
                value = float(line)
                if value > 10000.00:
                    raise Exception('Amount should not exceed 10000.00', value)

                students.append(value)
                sum += value

                if len(students) == numberStudents:  # End
                    #print 'Students paid ', students
                    split = float('%.2f' %(sum / numberStudents))
                    #print 'Each should pay ', split

                    exchangeTotal = 0
                    for student in students:
                        if student < split:
                            diff = split - student
                            #print 'Should pay ', diff
                            exchangeTotal += diff
                    print exchangeTotal

                    numberStudents = None # reset
        except:
            raise Exception('Tried to read line %s' % (line))

if __name__ == '__main__':
    readFile()