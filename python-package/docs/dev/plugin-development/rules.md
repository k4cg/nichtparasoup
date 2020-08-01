# ImageCrawler Plugin Development: Rules

* Your ImageCrawler implementation class must inherit `nichtparasoup.core.BaseImageCrawler`.
* Your ImageCrawler must be installable via `pip`.
* Your ImageCrawler must require `nichtparasoup>=2.2` or greater.
* Your ImageCrawler must have an [EntryPoint](https://packaging.python.org/specifications/entry-points/)
  with the `group` called "nichtparasoup_imagecrawler".  
  The `name` is the name that should be used in the config.  
  The `object reference` points to your implementation class.
* Your Plugin should include a folder `examples` that holds at least one _nichtparasoup_ config file.
* Your Plugin should include a `docs` folder that describes all the options/config the implementation class accepts.
