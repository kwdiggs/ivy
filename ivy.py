#!/usr/bin/env python3
import sys
import os
import re

version_no = '1.0.1'

resource_file = os.path.join(os.environ['HOME'], '.ivyrc')
work_items = []


# file io.
def write_list_to_file():
    with open(resource_file, 'w') as ivy_rc:
        for item in work_items:
            ivy_rc.write(item)


def read_list_from_file():
    with open(resource_file, 'r') as ivy_rc:
        for line in ivy_rc:
            work_items.append(line)


# application reference.
def about():
    print('ivy ' + version_no + ' by Keenan Diggs\nContribute! https://github.com/kwdiggs/ivy')


def help():
    print('>>>>>>>>>> ivy usage guide <<<<<<<<<<\n-------------------------------------')
    print('|-> ivy project info:\t ivy about')
    print('|-> marking items done:\t ivy check <num>, where <num> is an item\'s position in the list')
    print('|-> deleting an item:\t ivy erase <num>, where <num> is an item\'s position in the list')
    print('|-> this dialog:\t ivy help')
    print('|-> viewing the list:\t ivy list')
    print('|-> deleting all items:\t ivy new')
    print('|-> rewriting items:\t ivy rewrite <num> "new item description"'
          ', where <num> is an item\'s position in the list.')
    print('|-> reordering items:\t ivy put <num> <num2>, '
          'where <num> is the position of an item and <num2> is the position to move it to')
    print('|-> marking items todo:\t ivy uncheck <num>, where <num> is an item\'s position in the list')
    print('|-> adding new items:\t ivy write \"text description of work item\", with quoted text')


# ivy list operations.
# [C]reate
def write():
    if len(work_items) >= 6:
        print("The Ivy Lee method dictates that no more than 6 items shall be on the list.")
        print("Please ensure that you have chosen 6 items with the truly highest importance.")
        return

    item = sys.argv[2].strip()

    if item:
        work_items.append('( ) ' + item + '\n')
        write_list_to_file()
    else:
        print('Attempted to add item to list, but an invalid item was given.')
        print('Please add items using the form: ivy write \"example todo item\" (in quotes)')


# [R]ead
def print_items():
    if len(work_items) is 0:
        print('No items have been written yet.')
        return

    for i, item in enumerate(work_items):
        item = '{0}. {1}'.format(i + 1, item)
        sys.stdout.write(item)


# [U]pdate
def rewrite():
    def to_int_lambda(integer):
        return to_int(integer, 'rewrite', ' "new item description"')

    item_number = to_int_lambda(sys.argv[2])

    if item_number is None:
        return

    if not index_exists(item_number - 1):
        print('There is no item at position ' + str(item_number))
        return

    if len(sys.argv) < 4:
        to_int_lambda('new item not given, print correct usage')
        return

    old_item = work_items[item_number - 1]

    item = sys.argv[3].strip()
    prefix = re.compile('\( \) |\(x\) ').search(old_item).group()

    work_items[item_number - 1] = prefix + item + '\n'
    write_list_to_file()


def move():
    def to_int_lambda(integer):
        return to_int(integer, 'put', ' <num2>', ' and <num2> is the position to move it to')

    if len(sys.argv) < 4:
        print('Too few arguments.')
        to_int_lambda('incorrect number of argument, show usage')
        return

    old_position = to_int_lambda(sys.argv[2])
    if not old_position:
        return

    if not index_exists(old_position - 1):
        print('No item at position ' + str(old_position))
        return

    new_position = to_int_lambda(sys.argv[3])
    if not new_position:
        return

    item = work_items.pop(old_position - 1)
    work_items.insert(new_position - 1, item)
    write_list_to_file()


def uncheck():
    check(False)


def check(*args):
    name = 'uncheck' if args[0] is False else 'check'
    substring = '( )' if args[0] is False else '(x)'
    capture_string = '(x)' if args[0] is False else '( )'

    item_number = to_int(sys.argv[2], name)

    if item_number is None:
        return

    if not index_exists(item_number - 1):
        print('No item at position ' + str(item_number))
        return

    regex = re.compile('^' + re.escape(capture_string))

    item = work_items[item_number - 1]
    item = item.replace(item, regex.sub(substring, item))

    work_items[item_number - 1] = item
    write_list_to_file()


# [D]elete
def new_list():
    open(resource_file, 'w').close()


def erase():
    item_number = to_int(sys.argv[2], 'erase')

    if item_number is None:
        return

    if not index_exists(item_number - 1):
        print('There is no item at position ' + str(item_number) + '.')
        return

    work_items.pop(item_number - 1)
    write_list_to_file()


# utility functions
def index_exists(index):
    return (index >= 0) and (index < len(work_items))


def to_int(number, name, description='', final_clause=''):
    try:
        return int(number)
    except ValueError:
        print(name + ' usage: ivy ' + name + ' <num>' + description
              + ', where <num> is an integer representing an item\'s position in the list' + final_clause)
        return


def sort_options_keys():
    sorted_options = list(options)
    sorted_options.sort()
    return sorted_options


options = {
    'about': about,
    'check': check,
    'erase': erase,
    'help': help,
    'list': print_items,
    'move': move,
    'new': new_list,
    'rewrite': rewrite,
    'uncheck': uncheck,
    'write': write,
}


def main():
    if not os.path.isfile(resource_file):
        new_list()
    else:
        read_list_from_file()

    try:
        option = sys.argv[1]
    except IndexError:
        print('Command required. Please enter a command in the form: ivy <x>, where <x> is one of:\n'
              + str(sort_options_keys()))
        exit(1)

    try:
        command = options[option]
    except KeyError:
        print('\'' + option + '\' is not a recognized command. Commands are:\n' + str(sort_options_keys()))
    else:
        command(True) if option == 'check' else command()


# so it begins
main()
