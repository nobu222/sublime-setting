import sublime, sublime_plugin, re, os.path

class ClassCompletions(sublime_plugin.EventListener):

    def get_completions(self):
        completions = []
        # loop views
        for v in sublime.active_window().views():
            # only css/scss files
            if v.match_selector(0, "source.css, source.scss"):
                # get classnames
                class_names = v.find_by_selector("entity.other.attribute-name.class.css")
                for class_name in class_names:
                    # maybe include more classes
                    words = v.substr(class_name)[1:].split(".")
                    for w in words:
                        snippet = (w+"\t"+os.path.basename(v.file_name()), w)
                        if not snippet in completions:
                            completions.append(snippet)
        completions.sort()
        return (completions, sublime.INHIBIT_WORD_COMPLETIONS)

    def on_query_completions(self, view, prefix, locations):
        # match a css selector
        if view.match_selector(locations[0], "meta.selector.css"):
            point = locations[0] - len(prefix)
            # match if the scope is a class
            if view.substr(sublime.Region(point - 1, point)) == '.':
                return self.get_completions()
        # match an attribute tag
        if view.match_selector(locations[0], "meta.tag string.quoted.double.html"):
            quotes = view.extract_scope(locations[0])
            # match if the scope is a class
            if view.substr(sublime.Region(quotes.a - 6, quotes.a)).endswith("class="):
                return self.get_completions()
