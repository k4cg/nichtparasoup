if __name__ == "__main__":
    from sys import stderr, exit
    from os import linesep

    print("No module named nichtparasoup",
          "Did you mean nichtparasoup-server?",
          file=stderr, sep=linesep, end=linesep)
    exit(1)
