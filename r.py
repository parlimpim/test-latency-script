# import pandas as pd
# data = [['oregon', 'oregon', 1], ['oregon', 'oregon', 2], ['oregon', 'oregon', 3]]
# df = pd.DataFrame(data=data, columns=['backend server location', 'organization data', 'time (secs)'])
# print(df)

def test_2(pim):
    print(pim)

def test(func, **kwang):
    print(kwang)
    func(kwang['pim'])

test(test_2, pim=1, pim2=2)