import argparse
import ntpath
import os
from shutil import copyfile


def list_diff(li1, li2):
    """returns a list with the difference of 2 lists"""
    return list(list(set(li1) - set(li2)) + list(set(li2) - set(li1)))


def get_files_from(location, pattern):
    """returns the files from a folder
    you can specify the type of file given the pattern parameter the extension of the file"""
    files_in_dir = []
    # r=>root, d=>directories, f=>files
    for r, d, f in os.walk(location):
        for item in f:
            if pattern:
                if pattern in item:
                    files_in_dir.append(os.path.join(r, item))
            else:
                files_in_dir.append(os.path.join(r, item))
    return files_in_dir


def copy_files_from_non_found_in_b_to_destination(results, destination):
    """copies the files in results['non_found_in_b'] to the destination"""
    for non_found_in_b in results['non_found_files_in_b'] + results['corrupted_files']:
        print("coping " + non_found_in_b + " ...")
        copyfile(non_found_in_b, os.path.join(destination, ntpath.basename(non_found_in_b)))
        print(non_found_in_b + " completed copy")


def print_compared_sizes(results):
    """prints the contents returned by compare_sizes()"""
    for type_of_result in results:
        if not results[type_of_result]:
            print("There is no " + type_of_result)
        else:
            print(type_of_result)
            for element in results[type_of_result]:
                print('\t' + element)


def compare_sizes(loc_a, loc_b, pattern):
    """Compares sizes of the files in two directories from 2 locations, loc_a and loc_b
    to specify the file type you can use the pattern argument to find by extension
    returns a dictionary:
        copied_files - list of files that are find in both directories
        corrupted_files - list of files that have a different sizes in both directories
        non_found_files_in_a - list of files not found in a but found in b
        non_found_files_in_b - list of files not found in b but found in a
    the lists have the file names found in loc_a except the non_found_files_in_a that are in loc_b"""
    files_in_loc_a = get_files_from(loc_a, pattern)
    files_in_loc_b = get_files_from(loc_b, pattern)
    corrupted_files = []
    copied_files = []
    exists = False
    for file_a in files_in_loc_a:
        basename_file_a = ntpath.basename(file_a)
        for file_b in files_in_loc_b:
            if basename_file_a == ntpath.basename(file_b):
                exists = True
                if os.path.getsize(file_a) != os.path.getsize(file_b):
                    corrupted_files.append(file_a)
                else:
                    copied_files.append(file_a)

            if exists:
                files_in_loc_b.remove(file_b)
                exists = False
                break
    return {
        'copied_files': copied_files,
        'corrupted_files': corrupted_files,
        'non_found_files_in_a': files_in_loc_b,
        'non_found_files_in_b': list_diff(files_in_loc_a, copied_files + corrupted_files)
    }


def delete_files(files):
    for file in files:
        os.remove(file)
        print("File " + file + ' has deleted.')


if __name__ == "__main__":
    # obs_location = '/home/onikenx/Videos/obs/aulas'
    # drive_location = '/home/onikenx/Clouds/OneDrive/apontamentos-de-aula/extras/gravacoesdeaulas/A3S1'
    parser = argparse.ArgumentParser(description='\tVerifyfiles verifies the files in 2 folders\n'
                                                 'the files can have a pattern to be identified\n'
                                                 'this program can also copy and delete after the copy has done.')
    parser.add_argument('loc_a', type=str,
                        help='location a, from where the files are copied')
    parser.add_argument('loc_b', type=str,
                        help='location b, where the files will be copied')
    parser.add_argument('-e', '--expression', type=str,
                        help='expression that will be used to specify the files, '
                             'can be used to especify the extesion of the file')
    parser.add_argument('-c', '--copy', action='store_true',
                        help='copies files from loc_a to loc_b')
    parser.add_argument('-d', '--delete', action='store_true',
                        help='deletes files from folder a that already have been copied correctly')
    parser.add_argument('-i', '--ignore', action='store_true',
                        help='ignores warning when deleting files')
    # parser.add_argument('-s', '--show', action='store_true',
    #                     help='shows information about the files, if done with -c and/or -d it will show before '
    #                          'and after operations')
    args = parser.parse_args()

    # Verifies that the directories exist
    if not os.path.isdir(args.loc_a):
        print("Dir '" + args.loc_a + "' does not exist.")
        exit(1)

    if not os.path.isdir(args.loc_b):
        print("Dir '" + args.loc_b + "' does not exist.")
        exit(1)

    if args.copy:
        results = compare_sizes(args.loc_a, args.loc_b, args.expression)
        junction = results['corrupted_files'] + results['non_found_files_in_b']
        if junction:
            print("Files that gonna be copied:")
            for file in junction:
                print("\t" + file)
            copy_files_from_non_found_in_b_to_destination(results, args.loc_b)
        else:
            print('there is no files to be copied')

    if args.delete:
        results = compare_sizes(args.loc_a, args.loc_b, args.expression)
        if results['copied_files']:
            print("Files that gonna be deleted:")
            for file in results['copied_files']:
                print("\t" + file)
            if args.ignore:
                delete_files(results['copied_files'])
            elif input("Are you really sure you want to delete these copied_files?[y/n]") == 'y':
                delete_files(results['copied_files'])
        else:
            print('there is no files to be deleted')

    if not args.delete and not args.copy:
        results = compare_sizes(args.loc_a, args.loc_b, args.expression)
        print_compared_sizes(results)
