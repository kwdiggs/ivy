#!/usr/bin/env python3
import sys
import os
import fileinput
import re

version_no = '1.0.0'

resource_file = os.path.join(os.environ['HOME'], '.ivyrc')
option_list = ['about', 'check', 'erase', 'help', 'list', 'new', 'rewrite', 'uncheck', 'write']
work_items = []


def about(*args):
    print('ivy ' + version_no + ' by Keenan Diggs\nContribute! https://github.com/kwdiggs/ivy')


def check(*args):
    name = 'uncheck' if args[0] is False else 'check'
    substring = '( )' if args[0] is False else '(x)'
    capture_string = '(x)' if args[0] is False else '( )'

    item_number = check_int(sys.argv[2], name)

    if item_number is None:
        return None

    if check_list_position(item_number):
        regex = re.compile('^' + re.escape(capture_string))
        item = work_items[item_number - 1]
        for line in fileinput.input(resource_file, inplace=1):
            line = line.replace(item, regex.sub(substring, item))
            print(line, end='')


def check_list_position(pos):
    if (pos < 1) or (pos > len(work_items)):
        print('There is no item at position ' + str(pos) + '.')
        return False

    return True


def create(*args):
    if len(work_items) >= 6:
        print("The Ivy Lee method dictates that no more than 6 items shall be on the list.")
        print("Please ensure that you have chosen 6 items with the truly highest importance.")
        return None

    item = sys.argv[2].strip()

    if item:
        ivy_rc = open(resource_file, 'a')
        ivy_rc.write('( ) ' + item + '\n')
        ivy_rc.close()
    else:
        print('Attempted to add item to list, but an invalid item was given.')
        print('Please add items using the form: ivy write \"example todo item\" (in quotes)')


def delete(*args):
    item_number = check_int(sys.argv[2], 'erase')

    if item_number is None:
        return None

    work_items.remove(item_number - 1)
    write_list_to_file()


def check_int(number, name, description='', final_clause=''):
    try:
        return int(number)
    except ValueError:
        print(name + ' usage: ivy ' + name + ' <num>' + description
              + ', where <num> is an integer representing an item\'s position in the list' + final_clause)
        return None


def insert(*args):
    def check_int_lambda(integer):
        return check_int(integer, 'put', ' <num2>', ' and <num2> is the position to move it to')

    if len(sys.argv) < 4:
        print('Too few arguments')
        check_int_lambda('incorrect number of argument, show usage')
        return None

    old_position = check_int_lambda(sys.argv[2])
    if not old_position:
        return None

    new_position = check_int_lambda(sys.argv[3])
    if not new_position:
        return None

    item = work_items.pop(old_position - 1)
    work_items.insert(new_position - 1, item)
    write_list_to_file()


def invalid_option(option):
    print('Invalid option \'' + option + '\'. Please select one of: ')
    print(option_list)


def options(option):
    return {
        'about': about,
        'check': check,
        'erase': delete,
        'help': print_tutorial,
        'list': show,
        'new': truncate_list,
        'put': insert,
        'rewrite': update,
        'uncheck': uncheck,
        'write': create,
    }.get(option, invalid_option)(option)


def print_tutorial(*args):
    print('>>>>>>>>>> ivy usage guide <<<<<<<<<<\n-------------------------------------')
    print('|-> ivy project info:\t ivy about')
    print('|-> marking items done:\t ivy check <num> => where <num> is an item\'s position in the list')
    print('|-> deleting an item:\t ivy erase <num> => where <num> is an item\'s position in the list')
    print('|-> this dialog:\t ivy help')
    print('|-> viewing the list:\t ivy list')
    print('|-> deleting all items:\t ivy new')
    print('|-> rewriting items:\t ivy rewrite <num> "new item description" '
          '=> where <num> is an item\'s position in the list.')
    print('|-> reordering items:\t ivy put <num> <num2>, '
          'where <num> is the position of the item to be moved and <num2> is the position to move it to')
    print('|-> marking items todo:\t ivy uncheck <num> => where <num> is an item\'s position in the list')
    print('|-> adding new items:\t ivy write \"text description of work item\" => with quoted text')


def show(*args):
    if len(work_items) is 0:
        print('No items have been written yet.')
        return None

    for i, item in enumerate(work_items):
        item = '{0}. {1}'.format(i + 1, item)
        sys.stdout.write(item)


def truncate_list(*args):
    open(resource_file, 'w').close()


def uncheck(*args):
    check(False)


def update(*args):
    def check_int_lambda(integer):
        return check_int(integer, 'rewrite', ' "new item description"')

    item_number = check_int_lambda(sys.argv[2])

    if item_number is None or check_list_position(item_number) is False:
        return None

    if len(sys.argv) < 4:
        check_int_lambda('new item not given, print correct usage')
        return None

    old_item = work_items[item_number - 1]
    new_item = sys.argv[3].strip()
    prefix = re.compile('\( \) |\(x\) ').search(old_item).group()
    for line in fileinput.input(resource_file, inplace=1):
        line = line.replace(old_item, prefix + new_item + '\n')
        print(line, end='')


def write_list_to_file():
    with open(resource_file, 'w') as ivy_rc:
        for item in work_items:
            ivy_rc.write(item)


def main():
    if not os.path.isfile(resource_file):
        open(resource_file, 'w').close()

    with open(resource_file) as ivy_rc:
        for line in ivy_rc:
            work_items.append(line)

    try:
        options(sys.argv[1])
    except IndexError:
        print('Command required. Please enter a command in the form: ivy <x>, '
              'where <x> is one of:\n' + str(option_list))


# so it begins
main()
