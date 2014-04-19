import bisect
import sublime, sublime_plugin

def _find_closest_scope(view, scope, target):
    matches = view.find_by_selector(scope)
    closest_insrt = bisect.bisect_left(matches, target)
    return view.substr(matches[closest_insrt - 1])

class SuperComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if prefix == 'super' or prefix == 'supe' \
                and 'source.python' in view.scope_name(locations[0]):

            target = sublime.Region(locations[0], locations[0])
            fn_name =  _find_closest_scope(
                view, 'entity.name.function.python', target)
            cls_name = _find_closest_scope(
                view, 'entity.name.type.class.python', target)

            args = _find_closest_scope(
                view, 'meta.function.parameters.python', target)

            self_name, other_args = args.split(',', 1)

            return [('auto-super()', 'super(%s, %s).%s(${1:%s})' % (
                cls_name, self_name, fn_name, other_args.strip()))]




