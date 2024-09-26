import marshmallow
from marshmallow import post_load


class ProbelyCLIBaseFiltersSchema(marshmallow.Schema):
    @post_load
    def ignore_unused_filters(self, data, **kwargs):
        """
        All argparse arguments default to None, which means they must be removed.
        This avoids errors when calling the API.
        """
        command_filters = {f: v for f, v in data.items() if v is not None}
        return command_filters

    class Meta:
        # ignores other args that are not filters
        unknown = marshmallow.EXCLUDE
