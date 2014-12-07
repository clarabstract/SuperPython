import sublime
import sublime_plugin


class PythonSuperComplete(sublime_plugin.EventListener):

    def on_activated(self, view):
        settings = view.settings()
        self.tab_size = settings.get('tab_size')

    def on_query_completions(self, view, prefix, locations):
        if 'source.python' not in view.scope_name(locations[0]):
            # Work only in python source
            return
        if prefix not in ('super', 'supe'):
            return

        target = sublime.Region(locations[0], locations[0])
        indent = self._get_indent(view, target)
        if indent == 0:
            # We are on the top of indent hierarchy level. Do nothing.
            return
        current_row = self._get_row(view, target)
        try:
            fn_region = self._find_closest_scope(view, 'entity.name.function.python', target, indent, current_row)
            args_region = self._find_closest_scope(view, 'meta.function.parameters.python', target, indent, current_row)
            fn_indent = self._get_indent(view, fn_region)
            # search class scope with lower indentation level than founded function
            cls_region = self._find_closest_scope(view, 'entity.name.type.class.python', target, fn_indent, current_row)
        except IndexError:
            # We could't find some scope
            return

        cls_row = self._get_row(view, cls_region)
        fn_row = self._get_row(view, fn_region)
        if fn_row < cls_row:
            # Our current position in class, but not in function
            return

        fn_name = view.substr(fn_region)
        cls_name = view.substr(cls_region)
        args = view.substr(args_region)

        if ',' in args:
            self_name, other_args = args.split(',', 1)
        else:
            self_name = args
            other_args = ''

        return [('auto-super()', 'super(%s, %s).%s(${1:%s})' % (
            cls_name, self_name, fn_name, other_args.strip()))]

    def _find_closest_scope(self, view, scope, target, min_indent, max_row):
        # use last found scope upper than current line and with smaller indentation level
        matches = view.find_by_selector(scope)
        matches = [m for m in matches if self._get_indent(view, m) < min_indent and max_row > self._get_row(view, m)]
        return matches[-1]

    def _get_indent(self, view, region):
        line = view.substr(view.line(region))
        return sum([self.tab_size if s == '\t' else 1 for s in line.replace(line.lstrip(), '')])

    def _get_row(self, view, region):
        return view.rowcol(region.begin())[0]
