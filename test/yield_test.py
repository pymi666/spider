#!python3
# -*- coding: utf-8 -*-
i = 0
def foo(i):
    print ("start")
    while True:
        i += 1
        yield i
        print("end")


g = foo(i)
print (next(g))
print ("....")
print (next(g))
print ("....")
print (next(g))

