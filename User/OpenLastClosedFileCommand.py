import sublime, sublime_plugin
import os

last_closed_file_path = sublime.packages_path() + "/User/last_closed_file.path"
last_closed_file_max = 10

def get_history():
   f = open(last_closed_file_path, "rb")
   history = f.readlines()
   f.close()

   return history

def save_history(history):
   f = open(last_closed_file_path, "wb")
   f.write("\n".join(map(str, history)))
   f.close()

class OpenLastClosedFileCommand(sublime_plugin.WindowCommand):
   def run(self):
      if os.path.exists(last_closed_file_path):
         history = get_history()

         if len(history) > 0:
            self.window.open_file(history.pop().strip())
            save_history(history)

class OpenLastClosedFileEvent(sublime_plugin.EventListener):
   def on_close(self, view):
      if view.file_name() != None:
         history = get_history()

         history.append(view.file_name())
         if len(history) >last_closed_file_max:
            history = history[-last_closed_file_max:]

         save_history(history)