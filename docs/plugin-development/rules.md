# ImageCrawler Plugin Development: Rules

* Your ImageCrawler implementation class must inherit `nichtparasoup.core.BaseImageCrawler`.
* Your ImageCrawler must be installable via `pip`.
* Your ImageCrawler must have an [EntryPoint](https://packaging.python.org/specifications/entry-points/)
  called "nichtparasoup_imagecrawler", that links your implementation class.
* Your Plugin should include a folder `examples` that holds at least one _nichtparasoup_ config file.
* Your Plugin should include a `docs` folder that describes all the options/config the implementation class accepts.
