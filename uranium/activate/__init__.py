def generate_activate_this(uranium):
    """
    generate a text block which should be injected into an activate_this script.
    """
    return (
        _generate_environment_variables(uranium)
    )


ENV_TEMPLATE = """
import os
""".strip()


def _generate_environment_variables(uranium):
    content = ENV_TEMPLATE
    for name, value in uranium.environment.items():
        content += "\nos.environ['{name}'] = '{value}'".format(
            name=name, value=value
        )

    return content
