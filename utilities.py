from contextlib import contextmanager

import ipywidgets as wdg

from common import AIIDA_PROFILE, STYLE

try:
    from aiida import load_profile, orm
except ImportError:
    WITH_AIIDA = False
else:
    WITH_AIIDA = True

@contextmanager
def with_aiida_profile(profile_name: str):
    """Context manager to check if AiiDA is setup with a profile available.

    Args:
        profile_name (str): Name of the AiiDA profile to switch to.
    """
    if not WITH_AIIDA:
        raise ImportError("AiiDA is not available.")
    try:
        load_profile(profile_name)
        yield
    except Exception as e:
        raise RuntimeError(f"Could not load AiiDA profile '{profile_name}': {e}")
    finally:
        pass

def click_param_to_widget(
        param_info: dict,
        override_defaults: dict = None,
        code_map: dict = None,
    ) -> wdg.Widget:
    """Generate ipywidgets for a given parameter info dictionary.

    Args:
        param_info (dict): Parameter information dictionary.

    Returns:
        wdg.Widget: Corresponding ipywidget.
    """
    override_defaults = override_defaults or {}
    code_map = code_map or {}

    name = param_info['name']
    default_value = param_info.get('default', None)
    # Apply override if provided
    default_value = override_defaults.get(name, default_value)
    help_str = param_info.get('help', name) or name
    type_dct = param_info['type']
    type_str = type_dct['param_type']
    required = param_info.get('required', False)

    widget_kwargs = {
        # 'value': default_value,
        'description': name,
        'tooltip': help_str,
        'style': STYLE,
        'required': required,
    }
    widget_cls = None
    min_val = None
    max_val = None
    if type_str.startswith('Int'):
        min_val = type_dct.get('min', None)
        max_val = type_dct.get('max', None)
        if min_val is None or max_val is None:
            widget_cls = wdg.IntText
        else:
            widget_cls = wdg.IntRangeSlider
            widget_kwargs.update({
                'min': min_val,
                'max': max_val,
            })
    elif type_str.startswith('Float'):
        widget_cls = wdg.FloatText
        # min_val = type_dct.get('min', None)
        # max_val = type_dct.get('max', None)
        # if min_val is None or max_val is None:
        #     widget_cls = wdg.FloatText
        # else:
        #     widget_cls = wdg.FloatSlider
        #     widget_kwargs.update({
        #         'min': min_val,
        #         'max': max_val,
        #     })
    elif type_str.startswith('String'):
        widget_cls = wdg.Text
    elif type_str.startswith('Bool'):
        widget_cls = wdg.Checkbox
    elif type_str.startswith('Choice'):
        widget_cls = wdg.Select
        choices = type_dct.get('choices', [])
        widget_kwargs.update({
            'options': choices,
        })
    elif type_str.startswith('Path'):
        widget_cls = wdg.Text
    elif type_str == 'Code':
        widget_cls = wdg.Dropdown

        with with_aiida_profile(AIIDA_PROFILE):
            qb = orm.QueryBuilder()
            qb.append(orm.Code)
            codes = [_[0] for _ in qb.all()]
        codes_str = [f'{code.label}@{code.computer.label}' for code in codes]
        value = None
        for code in codes:
            expected = code_map.get(name, None)
            # print('Expected code for', name, ':', expected, ' - checking code:', code.label)
            if expected is not None and code.label == expected:
                value = f'{code.label}@{code.computer.label}'
                break
        widget_kwargs.update({
            'options': codes_str,
        })
        default_value = value
    else:
        raise ValueError(f"Unsupported parameter type: {type_str}")


    if min_val is not None:
        default_value = default_value if default_value is not None else min_val
    elif max_val is not None:
        default_value = default_value if default_value is not None else max_val

    widget_kwargs['value'] = default_value

    return widget_cls(**widget_kwargs)


def get_widgets_from_click_function(
        function: callable, layout_width: str = '600px',
        **kwargs
    ) -> dict:
    """
    Generate ipywidgets for the parameters of a given function.

    Parameters:
    function (callable): The function to generate widgets for.

    Returns:
    dict: A dictionary mapping parameter names to their corresponding widgets.
    """
    params_infos = [p.to_info_dict() for p in function.params]
    widgets = {}

    for info in params_infos:
        param_name = info['name']
        widget = click_param_to_widget(info, **kwargs)
        widget.layout.width = layout_width
        widgets[param_name] = widget
    return widgets

def get_click_args_from_widgets(function: callable, widgets: dict) -> list:
    """
    Generate command-line arguments from ipywidgets for a given function.

    Parameters:
    function (callable): The function to generate arguments for.
    widgets (dict): A dictionary mapping parameter names to their corresponding widgets.

    Returns:
    list: A list of command-line arguments.
    """
    params_infos = [p.to_info_dict() for p in function.params]
    args = []

    for info in params_infos:
        type_dct = info['type']
        type_str = type_dct['param_type']
        name = info['name']
        widget = widgets[name]
        value = widget.value
        value_str = str(value)
        opt = info['opts'][0]
        opt_sec = (info.get('secondary_opts', []) + [None])[0]

        if info['param_type_name'] == 'argument':
            args.append(value_str)
        elif type_str == 'Bool':
            if value:
                args.append(opt)
            elif opt_sec is not None:
                args.append(opt_sec)
        else:
            args.append(opt)
            if not info.get('count', False):
                args.append(value_str)

    return args
