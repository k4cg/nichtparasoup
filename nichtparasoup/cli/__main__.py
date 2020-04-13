import sys

from nichtparasoup.cli.main import main

sys.argv[0] = sys.executable + ' -m ' + __package__
sys.exit(main())
