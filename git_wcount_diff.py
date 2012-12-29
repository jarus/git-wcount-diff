import sys
import subprocess
import re

files_re = re.compile(r"diff --git a/(.+?) b/.+?")
additions_re = re.compile(r"{\+(.*?)\+}")
deletions_re = re.compile(r"\[-(.*?)-\]")
word_re = re.compile(r"\S*")


def count(regex, source):
    words = 0
    characters = 0
    for match in regex.findall(source):
        for word in word_re.findall(match.decode('utf8')):
            if len(word) == 0:
                continue
            words += 1
            characters += len(word)
    return words, characters


def analyse_file(filename, rev_1, rev_2):
    git_diff = subprocess.Popen(
        'git diff --word-diff %s %s -- "%s"' % (rev_1, rev_2, filename),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    stdout, stderr = git_diff.communicate()
    if git_diff.returncode > 0:
        print stderr
        sys.exit(2)
    return count(additions_re, stdout), count(deletions_re, stdout)


def main():
    if len(sys.argv) < 3:
        print "Usage: %s <commit> <commit>" % sys.argv[0]
        sys.exit(1)

    git_diff = subprocess.Popen(
        "git diff %s %s --name-only" % (sys.argv[1], sys.argv[2]),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    stdout, stderr = git_diff.communicate()
    if git_diff.returncode > 0:
        print stderr
        sys.exit(2)

    files = {}
    for git_file in stdout.splitlines():
        files[git_file] = analyse_file(git_file, sys.argv[1], sys.argv[2])

    for filename, (additions, deletions) in files.items():
        print "File: %s" % filename
        print " - Additions: %s Words %s Characters" % additions
        print " - Deletions: %s Words %s Characters" % deletions

if __name__ == '__main__':
    main()
