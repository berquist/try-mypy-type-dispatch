import inspect
from typing import Any, Dict, Optional, Type, TypeVar, Union
from warnings import warn


T = TypeVar("T", str, int)


def check_param_type(*, varname: str, vardata: Any, datatype: Type[Any]) -> None:
    """Validate a parameter to ensure it is of the correct type.

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
    *,
    include_dict: Dict[str, Union[str, int]],
    include_source: str,
    define: str,
    data_type: Type[T],
    default: Optional[T] = None,
    disable_warning: bool = False,
) -> T:
    """Retrieve a define from an SST Configuration Include File (sst_config.h or sst-element_config.h)
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
    check_param_type(varname="include_source", vardata=include_source, datatype=str)
    check_param_type(varname="define", vardata=define, datatype=str)
    if default is not None:
        check_param_type(varname="default", vardata=default, datatype=data_type)
    try:
        rtn_data = include_dict[define]
    except KeyError as exc_e:
        errmsg = f"Reading Config include file {include_source} - Cannot find #define {exc_e}"
        if not disable_warning:
            warn(errmsg, stacklevel=1)
        if default is None:
            raise RuntimeError(exc_e)  # noqa: B904
        rtn_data = default
    return data_type(rtn_data)


_INCLUDE_DICT: Dict[str, Union[int, str]] = {"hello": "world", "answer": 42}


def sst_elements_config_include_file_get_value(
    *,
    define: str,
    type: Type[T],  # noqa: A002
    default: Optional[T] = None,
    disable_warning: bool = False,
) -> T:
    """Retrieve a define from the SST Elements Configuration Include File (sst_element_config.h)

    Args:
        define (str): The define to look for
        type (Type): The expected type of the return value
        default (optional): Default Return if failure occurs
        disable_warning (bool): Disable the warning if define not found

    Returns:
        Value for specified define
    """
    return _get_sst_config_include_file_value(
        include_dict=_INCLUDE_DICT,
        include_source="sst_element_config.h",
        define=define,
        default=default,
        data_type=type,
        disable_warning=disable_warning,
    )


def sst_elements_config_include_file_get_value_int(
    define: str, default: Optional[int] = None, disable_warning: bool = False
) -> int:
    """Retrieve a define from the SST Elements Configuration Include File (sst_element_config.h)

    Args:
        define (str): The define to look for
        default (int): Default Return if failure occurs
        disable_warning (bool): Disable logging the warning if define is not found

    Returns:
        (int) The returned data or default if not found in the include file

    Raises:
        SSTTestCaseException: if type is incorrect OR no data AND default
                              is not provided
    """
    warn(
        "sst_elements_config_include_file_get_value_int() is deprecated and will be removed in future versions of SST. \
         Use sst_elements_config_include_file_get_value() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _get_sst_config_include_file_value(
        include_dict=_INCLUDE_DICT,
        include_source="sst_element_config.h",
        define=define,
        default=default,
        data_type=int,
        disable_warning=disable_warning,
    )


def sst_elements_config_include_file_get_value_str(
    define: str, default: Optional[str] = None, disable_warning: bool = False
) -> str:
    """Retrieve a define from the SST Elements Configuration Include File (sst_element_config.h)

    Args:
        define (str): The define to look for
        default (str): Default Return if failure occurs
        disable_warning (bool): Disable logging the warning if define is not found

    Returns:
        (str) The returned data or default if not found in the include file

    Raises:
        SSTTestCaseException: if type is incorrect OR no data AND default
                              is not provided
    """
    warn(
        "sst_elements_config_include_file_get_value_str() is deprecated and will be removed in future versions of SST. \
         Use sst_elements_config_include_file_get_value() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _get_sst_config_include_file_value(
        include_dict=_INCLUDE_DICT,
        include_source="sst_element_config.h",
        define=define,
        default=default,
        data_type=str,
        disable_warning=disable_warning,
    )
