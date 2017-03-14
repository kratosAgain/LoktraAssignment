#!/usr/bin/python
import sys
import argparse

letters = "acdegilmnoprstuw"

def hash(s):
    h = 7
    for i in range(0,len(s)):
        try:
            h = (h*37 + letters.index(s[i]))
        except ValueError:
            print("character/s is/are not in the letters list \nAborting ...")
            return
    return h

def reverse(hashed):

    original_string = ""
    try:
        temp = long(hashed)
    except Exception as e:
        print("Something went wrong, you entered an invalid value \nBye Bye ...")
        return

    flag = 0
    while temp > 7:
        flag = 0;
        for i in range(0,len(letters)):
            # As letter's char index was added in hash function, we check by removing them one by one
            # until it is divisible by 37
            if (temp-i)%37 == 0:
                #We are starting from end so appending the values at the start of the string
                original_string = letters[i]+original_string;
                temp = (temp-i)/37
                flag=1
                break
        if flag == 0:
            print("Something went wrong, you entered an invalid value \nBye Bye ...")
            return;
    return original_string





if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('function',help=" H for hashing,R for reverse hashing")
    args.add_argument('hash_string',help="<enter string to process here> ")

    args_list = args.parse_args()

    try:
        if args_list.function == 'H':
            ans = hash(args_list.hash_string)
            if ans:
                print(("Hashed Value for {} is {}").format(args_list.hash_string,ans))

        if args_list.function == 'R':
            ans = reverse(args_list.hash_string)
            if ans:
                print(("UnHashed Value for {} is {}").format(args_list.hash_string, ans))


    except ValueError:
        args.print_help()

