import inspect
import sys
from typing import Any, Type, Optional, Union, Dict


def check_param_type(varname: str, vardata: Any, datatype: Type) -> None:
    """ Validate a parameter to ensure it is of the correct type.

        Args:
            varname (str) = The string name of the variable
            vardata (???) = The actual variable of any type
            datatype (???) = The type that we want to confirm

        Raises:
            ValueErr: variable is not of the correct type.
    """
    caller = inspect.stack()[1][3]
    if not isinstance(vardata, datatype):
        err_str = f"TEST-ERROR: {caller}() param {varname} = {vardata} is a not a {datatype}; it is a {type(vardata)}"
        raise ValueError(err_str)


def _get_sst_config_include_file_value(
        include_dict: Dict[str, Union[str, int]],
        include_source: str,
        define: str,
        default: Optional[Union[str, int]] = None,
        data_type: Type = str,
        disable_warning: bool = False,
) -> Optional[Union[str, int]]:
    """ Retrieve a define from an SST Configuration Include File (sst_config.h or sst-element_config.h)
       include_dict (dict): The dictionary to search for the define
       include_source (str): The name of the include file we are searching
       define (str): The define to look for
       default (str|int): Default Return if failure occurs
       data_type (str|int): The data type to return
       disable_warning (bool): Disable the warning if define not found
       :return (str|int): The returned data or default if not found in the dict
       This will raise a SSTTestCaseException if a default is not provided or type
       is incorrect
    """
    if data_type not in (int, str):
        raise RuntimeError(f"Illegal datatype {data_type}")
    check_param_type("include_source", include_source, str)
    check_param_type("define", define, str)
    if default is not None:
        check_param_type("default", default, data_type)
    try:
        rtn_data = include_dict[define]
    except KeyError as exc_e:
        errmsg = f"Reading Config include file {include_source} - Cannot find #define {exc_e}"
        if not disable_warning:
            print(errmsg, file=sys.stderr)
        if default is None:
            raise RuntimeError(exc_e)
        rtn_data = default
    if data_type is int:
        rtn_data = int(rtn_data)
    return rtn_data


def sst_elements_config_include_file_get_value(
    define: str,
    type: Type,
    default: Any = None,
    disable_warning: bool = False
) -> Any:
    """Retrieve a define from the SST Elements Configuration Include File (sst_element_config.h)

    Args:
        define (str): The define to look for
        type (Type): The expected type of the return value
        default (optional): Default Return if failure occurs
        disable_warning (bool): Disable the warning if define not found

    Returns:
        Value for specified define
    """
    return _get_sst_config_include_file_value(test_engine_globals.TESTENGINE_ELEM_CONFINCLUDE_DICT,
                                              "sst_element_config.h", define, default, type, disable_warning)
