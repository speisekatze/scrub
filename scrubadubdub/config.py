from os import environ
import yaml

envmap = {
  'model': "SPACY_MODEL",
  'replace': "SCRUB_REPLACEMENT",
  'pattern': "SCRUB_EXTRA_PATTERN",
  'entity_label': "SCRUB_LABEL"
}
defaults = {
  'model': "de_core_news_lg",
  'replace': "[ZENSIERT]",
  'pattern': "",
  'entity_label': ["PER"]
}

class config:
  store = {}
  conffile = ""

  def load_yaml(self, file):
    with open(file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
      
  def __init__(self, file):
    self.store = self.load_yaml(file)

  def get(self, name):
    if name in envmap:
      e = environ.get(envmap[name])
      if e is not None:
        return e
    if self.store and name in self.store['scrub']:
      return self.store['scrub'][name]
    if name in defaults:
      return defaults[name]
    return ''
