import asyncio
import contextlib
import html
import importlib
import os
import sys
import traceback
from functools import wraps

import ipywidgets as wdg
import rich
from common import STYLE
from IPython.display import display

original_sys_path = sys.path.copy()


async def initialize_with_module(modules: str | list[str], eessi_version: str = None):
    """Initialize the environment using a module load command."""
    if isinstance(modules, str):
        modules = [modules]
    try:
        import module
    except ImportError:
        print('Module system not found. Make sure the required python packages are available in the current environment.')
    else:
        sys.path = original_sys_path
        await module.purge(force=True)

        print('Loading required modules from EESSI...')
        if eessi_version is None:
            eessi_version = os.getenv('REQUIRED_EESSI_VERSION', '2023.06')
        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull):
                await module.load(f'EESSI/{eessi_version}')

        for mod in modules:
            await module.load(mod)

        importlib.invalidate_caches()

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
    from utilities_aiida import get_all_codes

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
    value_type = str
    widget_cls = None
    min_val = None
    max_val = None
    observe = False
    if type_str.startswith('Int'):
        min_val = type_dct.get('min', None)
        max_val = type_dct.get('max', None)
        if min_val is None or max_val is None:
            widget_cls = wdg.Text
        else:
            widget_cls = wdg.IntSlider
            widget_kwargs.update({
                'min': min_val,
                'max': max_val,
                'step': 1,
            })
            observe = True
    elif type_str.startswith('Float'):
        widget_cls = wdg.Text
    elif type_str.startswith('String'):
        widget_cls = wdg.Text
    elif type_str.startswith('Bool'):
        value_type = bool
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
    elif type_str == 'DelimitedList':
        widget_cls = wdg.Text
    else:
        raise ValueError(f"Unsupported parameter type: {type_str}")

    # if min_val is not None:
    #     default_value = default_value if default_value is not None else min_val
    # elif max_val is not None:
    #     default_value = default_value if default_value is not None else max_val
    if default_value is not None:
        widget_kwargs['value'] = value_type(default_value)
    else:
        widget_kwargs['placeholder'] = 'No default value'

    tooltip_wdg = wdg.Button(
        description='?',
        tooltip=help_str,
        disabled=True,
        button_style='info'
    )
    tooltip_wdg.layout.width = '30px'

    # print("-" * 80)
    # print(f"Creating widget for parameter '{name}':")
    # print(f"  Widget class: {widget_cls}")
    # print(f"  Widget kwargs: {widget_kwargs}")
    # print(f"  Parameter info: {param_info}")

    try:
        new_widget = widget_cls(**widget_kwargs)
    except Exception as e:
        print(f"Error creating widget for parameter '{name}':")
        print(f"  Widget class: {widget_cls}")
        print(f"  Widget kwargs: {widget_kwargs}")
        print(f"  Parameter info: {param_info}")
        print(f"  type_dct: {type_dct}")
        print(f"  Exception: {e}")
        raise

    if observe:
        new_widget.modified = False
        def on_value_change(change):
            new_widget.modified = True
        new_widget.observe(on_value_change, names='value')

    new_widget.layout.width = layout_width

    res = wdg.HBox([new_widget, tooltip_wdg])

    return res


def get_widgets_from_click_function(
        function: callable, layout_width: str = '2000px',
        default_panel_name: str = None,
        hide_params: list[str] = None,
        **kwargs
    ) -> tuple[dict, wdg.VBox]:
    """
    Generate ipywidgets for the parameters of a given function.

    Parameters:
    function (callable): The function to generate widgets for.

    Returns:
    tuple[dict, wdg.VBox]: A tuple containing 
        - a dictionary mapping parameter names to their corresponding widgets and 
        - a VBox containing the widgets to be rendered with collapsible .
    """
    hide_params = hide_params or []
    # from pprint import pprint
    # print("^" * 80)
    # print(f"Generating widgets for function: {function}")
    # print(f"{type(function) = }")
    # print(f"{type(function.params[0]) = }")
    # print(f"{function.params[0].__dict__ = }")
    widgets = {}

    panel_widgets = {}

    for param in function.params:

        info = param.to_info_dict()
        param_name = info['name']
        if param_name in hide_params:
            continue  # Skip hidden parameters
        panel_name = getattr(param, 'panel', None)
        ptr = panel_widgets.setdefault(panel_name, [])
        # print(f"Processing parameter: {info['name']}, panel_name: {panel_name}")
        param_name = info['name']
        widget = click_param_to_widget(info, **kwargs)
        widgets[param_name] = widget
        ptr.append(widget)

    default_widgets = panel_widgets.pop(None, [])
    default_widgets += panel_widgets.pop(default_panel_name, [])
    default_vbox = wdg.VBox(default_widgets)

    panel_accordions = []
    for panel_name in panel_widgets.keys():
        panel_widgets_list = panel_widgets[panel_name]
        panel_vbox = wdg.VBox(panel_widgets_list)
        accordion = wdg.Accordion(children=[panel_vbox], titles=[panel_name])
        panel_accordions.append(accordion)

    main_vbox = wdg.VBox([default_vbox] + panel_accordions)

    return widgets, main_vbox

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
        default_value = info.get('default', None)
        widget_box = widgets.get(name, None)
        if widget_box is None:
            continue  # Skip parameters that don't have a corresponding widget
        # widget = widgets[name]
        widget = widget_box.children[0]  # Assuming the first child is the actual input widget
        value = widget.value
        # print(f"Parameter '{name}': type={type_str}, value={value}, default={default_value}")
        value_str = str(value)
        opt = info['opts'][0]
        opt_sec = (info.get('secondary_opts', []) + [None])[0]

        if value == '' and default_value is None:
            # print(f"Skipping parameter '{name}' because it has no value and no default.")
            continue  # Skip empty values with no default
        if (value is True or value is False) and value == default_value:
            # print(f"Skipping parameter '{name}' because it is a boolean and matches the default value.")
            continue  # Skip boolean values that match the default
        if value == default_value:
            # print(f"Skipping parameter '{name}' because it matches the default value.")
            continue  # Skip values that match the default
        if getattr(widget, 'modified', True) is False:
            print(f"Skipping parameter '{name}' because it has not been modified.")
            continue  # Skip unmodified widgets

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

    print(f"Generated command-line arguments from widgets: {args}")
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

def click_cli_widget(
        click_function,
        title: str = None,
        button_description: str = "Run",
        button_running_text: str = "Running...",
        **kwargs
        ) -> tuple[wdg.Widget, wdg.IntText]:
    """Create a widget from a click function, exposing all its parameters as ipywidgets.
    The widget will have a button to execute the function with the current parameter values.
    """
    console = rich.get_console()
    console.is_jupyter = True
    console.width = 140

    button_event_observer: wdg.IntText = wdg.IntText(
        value=0, description='', disabled=True,
    )

    widgets_dct, main_vbox = get_widgets_from_click_function(
        click_function,
        **kwargs
    )

    title = title or click_function.__name__.replace('_', ' ').title()

    title = wdg.HTML(value=f"<hr style=\"height: 5px; background-color: #fcc;\"> <h2>{title}</h2>")

    description = wdg.HTML(f"<div style=\"white-space: pre-wrap;\">{click_function.__doc__}</div>")

    generate_button = wdg.Button(description=button_description, button_style="success")

    output_area = wdg.Output()
    trace_widget = wdg.HTML()
    error_accordion = wdg.Accordion(children=[trace_widget])
    error_accordion.set_title(0, "Exception traceback")
    error_accordion.selected_index = None
    error_accordion.layout.display = "none"

    @widget_button_running(running_text=button_running_text)
    def on_run_button_clicked(b):
        error_accordion.layout.display = "none"
        with output_area:
            output_area.clear_output()
            args = get_click_args_from_widgets(click_function, widgets_dct)
            try:
                click_function(args, standalone_mode=False)
            except Exception as e:
                # Enclose stack trace in an accordion for better visibility and only print the error message in the output area
                error_accordion.layout.display = "block"
                trace_widget.value = (
                    "<pre style='white-space: pre-wrap'>"
                    f"{html.escape(traceback.format_exc())}"
                    "</pre>"
                )
                display(error_accordion)
                print(f"EXCEPTION: {e}")
        button_event_observer.value += 1

    generate_button.on_click(on_run_button_clicked)

    widget = wdg.VBox([title, description, main_vbox, generate_button, output_area])

    return widget, button_event_observer
