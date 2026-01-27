import ipywidgets as wdg

try:
    from aiida import load_profile, orm
except ImportError:
    WITH_AIIDA = False
else:
    WITH_AIIDA = True
    try:
        load_profile()
    except Exception:
        print("Could not load AiiDA profile. Please ensure AiiDA is properly configured.")
        WITH_AIIDA = False

STYLE = {'description_width': '150px', 'width': '400px'}

def click_param_to_widget(param_info: dict) -> wdg.Widget:
    """Generate ipywidgets for a given parameter info dictionary.

    Args:
        param_info (dict): Parameter information dictionary.

    Returns:
        wdg.Widget: Corresponding ipywidget.
    """
    name = param_info['name']
    default_value = param_info.get('default', None)
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
        min_val = type_dct.get('min', None)
        max_val = type_dct.get('max', None)
        if min_val is None or max_val is None:
            widget_cls = wdg.FloatText
        else:
            widget_cls = wdg.FloatSlider
            widget_kwargs.update({
                'min': min_val,
                'max': max_val,
            })
    elif type_str.startswith('String'):
        widget_cls = wdg.Text
    elif type_str.startswith('Bool'):
        widget_cls = wdg.Checkbox
    elif type_str.startswith('Choice'):
        widget_cls = wdg.Dropdown
        choices = type_dct.get('choices', [])
        widget_kwargs.update({
            'options': choices,
        })
    elif type_str.startswith('Path'):
        widget_cls = wdg.Text
    elif type_str == 'Code':
        if not WITH_AIIDA:
            raise ImportError("AiiDA is required to create a Code widget.")
        widget_cls = wdg.Dropdown
        qb = orm.QueryBuilder()
        qb.append(orm.Code)
        codes = [_[0] for _ in qb.all()]
        codes_str = [f'{code.label}@{code.computer.label}' for code in codes]
        widget_kwargs.update({
            'options': codes_str,
            'value': None
        })
    else:
        raise ValueError(f"Unsupported parameter type: {type_str}")


    if min_val is not None:
        default_value = default_value if default_value is not None else min_val
    elif max_val is not None:
        default_value = default_value if default_value is not None else max_val

    widget_kwargs['value'] = default_value

    return widget_cls(**widget_kwargs)


def get_widgets_from_click_function(function: callable, layout_width: str = '400px') -> dict:
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
        widget = click_param_to_widget(info)
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

    #     # print("Parameter:", name, "   Value:", value_str)
    #     print(f"Parameter: {name:>30s}   Value_str: {value_str:>10s}  Opt: {str(opt):>15s}  Opt_sec: {str(opt_sec):>15s}")

    # print(args)

    return args
