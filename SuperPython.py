import sublime
import sublime_plugin


class PythonSuperComplete(sublime_plugin.EventListener):

    def find_closest_scope(self, view, scope, target, min_indent, max_row):
        """Search closest scope upper than current."""
        matches = view.find_by_selector(scope)
        matches = [m for m in matches
                   if (self.get_indent(view, m) < min_indent
                       and max_row > self.get_row(view, m))]
        return matches[-1]

    def get_indent(self, view, region):
        """Get size of indentation for 'region'.

        Returns:
            int: Size of indentation for 'region'

        """
        line = view.substr(view.line(region))
        return sum(self.tab_size if space == '\t' else 1
                   for space in line.replace(line.lstrip(), ''))

    def get_row(self, view, region):
        """Get number of first row for 'region'.

        Returns:
            int: Number of first row for 'region'

        """
        return view.rowcol(region.begin())[0]

    def on_activated(self, view):
        settings = view.settings()
        self.prefix = settings.get('superpython.prefix', 'super')
        self.style = settings.get('superpython.style', 'short')
        self.tab_size = settings.get('tab_size')

    def on_query_completions(self, view, prefix, locations):
        if prefix != self.prefix:
            return

        point = locations[0]
        if not view.match_selector(point, 'source.python'):
            # Work only in python source
            return

        target = sublime.Region(point, point)
        indent = self.get_indent(view, target)
        if indent == 0:
            # We are on the top of indent hierarchy level. Do nothing.
            return

        row = self.get_row(view, target)
        try:
            fn_args_region = self.find_closest_scope(
                view, 'meta.function.parameters.python', target, indent, row)
            fn_region = self.find_closest_scope(
                view, 'entity.name.function.python', target, indent, row)

            fn_indent = self.get_indent(view, fn_region)
            cls_region = self.find_closest_scope(
                view, 'entity.name.class.python', target, fn_indent, row)
        except IndexError:
            # We could't find some scope
            return

        cls_row = self.get_row(view, cls_region)
        fn_row = self.get_row(view, fn_region)
        if cls_row > fn_row:
            # Our current position in class, but not in function
            return

        cls_name = view.substr(cls_region)
        fn_args = view.substr(fn_args_region)
        fn_args = fn_args.strip('()')
        fn_name = view.substr(fn_region)

        args_self = fn_args
        args_other = ''
        if ',' in fn_args:
            args_self, args_other = fn_args.split(',', 1)

        if args_self not in ('cls', 'self'):
            # our function is staticmethod
            args_other = fn_args
            args_self = cls_name

        args_other = args_other.strip()
        args_other_index = 2
        replacement = 'super(${{1:{cls_name}}}, {args_self})'
        if self.style == 'short':
            replacement = 'super()'
            args_other_index = 1
        replacement += '.{fn_name}(${{{args_other_index}:{args_other}}})'
        replacement = replacement.format(cls_name=cls_name,
                                         args_self=args_self, fn_name=fn_name,
                                         args_other=args_other,
                                         args_other_index=args_other_index)

        return [(self.prefix, replacement)]
