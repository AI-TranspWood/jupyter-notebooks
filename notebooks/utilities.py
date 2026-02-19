from functools import wraps

import ipywidgets as wdg
from common import STYLE
from utilities_aiida import get_all_codes


def click_param_to_widget(
        param_info: dict,
        override_defaults: dict = None,
        code_map: dict = None,
        layout_width: str = '700px',
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
                'step': 1,
            })
    elif type_str.startswith('Float'):
        widget_cls = wdg.FloatText
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

        codes = get_all_codes()
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

    tooltip_wdg = wdg.Button(
        description='?',
        tooltip=help_str,
        disabled=True,
        button_style='info'
    )
    tooltip_wdg.layout.width = '30px'

    new_widget = widget_cls(**widget_kwargs)
    new_widget.layout.width = layout_width

    res = wdg.HBox([new_widget, tooltip_wdg])

    return res


def get_widgets_from_click_function(
        function: callable, layout_width: str = '2000px',
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
        value = widget.children[0].value
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

def widget_button_running(
        running_style: str = 'success',
        running_text: str = 'Running...',
        running_icon: str = 'spinner fa-spin',
        running_disabled: bool = True,
    ):
    """Decorator for on_click handlers to set button state to running while the function is executing.
    Resets the button state after the function finishes, even if an error occurs.
    
    Args:
        running_style (str): Button style to use while running.
        running_text (str): Button text to use while running.
        running_icon (str): Button icon to use while running.
        running_disabled (bool): Whether to disable the button while running.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(button):
            original_style = button.button_style
            original_text = button.description
            original_icon = button.icon
            original_state = button.disabled

            button.button_style = running_style
            button.description = running_text
            button.icon = running_icon
            button.disabled = running_disabled

            res = None
            try:
                res = func(button)
            finally:
                button.button_style = original_style
                button.description = original_text
                button.icon = original_icon
                button.disabled = original_state
            return res
        return wrapper
    return decorator
