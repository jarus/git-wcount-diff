import sys
import subprocess
import re

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


def main():
    if len(sys.argv) < 3:
        print "Usage: %s <commit> <commit>" % sys.argv[0]
        sys.exit(1)
    git_diff = subprocess.Popen(
        "git diff %s %s --word-diff" % (sys.argv[1], sys.argv[2]),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    stdout, stderr = git_diff.communicate()
    if git_diff.returncode > 0:
        print stderr
        sys.exit(2)

    print "Additions: %s Words %s Characters" % count(additions_re, stdout)
    print "Deletions: %s Words %s Characters" % count(deletions_re, stdout)

if __name__ == '__main__':
    main()
