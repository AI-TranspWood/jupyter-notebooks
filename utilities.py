import ipywidgets as wdg


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

    if type_str.startswith('Int'):
        min_val = type_dct.get('min', None)
        max_val = type_dct.get('max', None)
        if min_val is None or max_val is None:
            return wdg.IntText(
                value=default_value if default_value is not None else 0,
                description=help_str,
                tooltip=help_str,
                required=required,
            )
        else:
            return wdg.IntRangeSlider(
                value=default_value if default_value is not None else (min_val, max_val),
                min=min_val,
                max=max_val,
                description=help_str,
                tooltip=help_str,
                required=required,
            )
    elif type_str.startswith('Float'):
        min_val = type_dct.get('min', None)
        max_val = type_dct.get('max', None)
        if min_val is None or max_val is None:
            return wdg.FloatText(
                value=default_value if default_value is not None else 0.0,
                description=help_str,
                tooltip=help_str,
            )
        else:
            return wdg.FloatSlider(
                value=default_value if default_value is not None else min_val,
                min=min_val,
                max=max_val,
                description=help_str,
                tooltip=help_str,
            )
    elif type_str.startswith('String'):
        return wdg.Text(
            value=default_value if default_value is not None else '',
            description=help_str,
            tooltip=help_str,
        )
    elif type_str.startswith('Bool'):
        return wdg.Checkbox(
            value=default_value if default_value is not None else False,
            description=help_str,
            tooltip=help_str,
        )
    elif type_str.startswith('Choice'):
        choices = type_dct.get('choices', [])
        return wdg.Dropdown(
            options=choices,
            value=default_value if default_value is not None else (choices[0] if choices else None),
            description=help_str,
            tooltip=help_str,
        )
    elif type_str.startswith('Path'):
        return wdg.Text(
            value=str(default_value) if default_value is not None else '',
            description=help_str,
            tooltip=help_str,
        )
    else:
        raise ValueError(f"Unsupported parameter type: {type_str}")


def get_widgets_from_click_function(function: callable) -> dict:
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
        widgets[param_name] = click_param_to_widget(info)

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
            args.append(opt if value else opt_sec)
        else:
            args.append(opt)
            if not info.get('count', False):
                args.append(value_str)

    return args
