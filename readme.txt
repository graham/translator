The purpose of translator is to make building up a localization easy.

It has a basic process.


  1. Build up a root.py (at this point only python is supported, but I
  plan on allowing other languages as an output at some point)
      Root.py basically is just a dict (hash) of your keys and
      translateables.

      d = { 'hello_world':"Hello World!"}

  2. Choose the languages you want to translate to:
      t = TranslationRoot("root") # module name
      t.translate_to_module('en') # exported to export/en.py
      t.translate_to_module('es') # exported to export/es.py

      All exported modules contain a "Excluded" dict that you can use
      to make in place updates that will not be changed when you re-export.


  
