from os import environ
import yaml

envmap = {
  'model': "SPACY_MODEL",
  'pattern': "SCUB_EXTRA_PATTERN"
}
defaults = {
  'model': "de_dep_news_trf",
  'pattern': ""
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
    if self.store and name in self.store:
      return self.store[name]
    if name in defaults:
      return defaults[name]
    return ''
