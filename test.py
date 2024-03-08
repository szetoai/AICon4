def fun():
    x = 5


try:
    if "cat" == fun():
        print("oops")
except ValueError as err:
    print(err.args)
    print("what")