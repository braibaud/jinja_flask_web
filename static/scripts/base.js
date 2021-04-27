const animationDuration = 300;

$.ajaxSetup(
    {
        crossDomain: true,
        xhrFields:
        {
            withCredentials: true
        }
    });

function __action(
    url,
    data = null,
    verb = null,
    timeout = null)
{
    return $.ajax(
        {
            url: url,
            type: (verb != null ? verb : 'POST'),
            async: true,
            data: JSON.stringify(data != null ? data : {}),
            processData: true,
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            timeout: (timeout != null ? timeout : 30) * 1000
        });
}

function __baseAction(
    url,
    verb = null,
    timeout = null)
{

    return $.ajax(
        {
            url: url,
            type: (verb != null ? verb : 'POST'),
            async: true,
            timeout: (timeout != null ? timeout : 30) * 1000
        });
}

function getCookie(cname)
{
    let name = cname + '=';
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');

    for (let i = 0; i < ca.length; i++)
    {
        let c = ca[i];

        while (c.charAt(0) == ' ')
        {
            c = c.substring(1);
        }

        if (c.indexOf(name) == 0)
        {
            return c.substring(name.length, c.length);
        }
    }

    return '';
}

function escapeSimpleQuotes(str)
{
    if (str == null)
    {
        return null;
    }

    return str.replace("'", "\\'");
}

function escapeDoubleQuotes(str)
{
    if (str == null)
    {
        return null;
    }

    return str.replace('"', '\\"');
}

function htmlEncode(str)
{
    if (str == null)
    {
        return null;
    }

    return str.replace(
        /[\u00A0-\u9999<>\&]/gim,
        function (i)
        {
            return '&#' + i.charCodeAt(0) + ';';
        });
}

function isNullOrWhiteSpace(str)
{
    return ((str == null) || (str.match(/^ *$/) !== null));
}

function toggleVisibility(element)
{
    $('#' + element).toggle(animationDuration);
}

function getExceptionMessages(
    result,
    exception)
{
    if (result == null)
    {
        result = '';
    }

    if (exception != null)
    {
        if (typeof (exception) == 'string')
        {
            result = exception;
        }
        else if (typeof (exception) == 'object')
        {
            result = result + exception.Message + '<br />';

            if (exception.ExceptionType == 'System.AggregateException')
            {
                exception = exception.ExceptionDetail;
            }

            result = getExceptionMessages(
                result,
                exception.InnerException);
        }
    }

    return result;
}

function hideElement(element)
{
    $(element).hide(animationDuration);
}

function showElement(element)
{
    $(element).show(animationDuration);
}

function hideInfoArea(name)
{
    hideElement(`#{name}_area`);
}

function showInfoArea(name)
{
    showElement(`#{name}_area`);
}

function setInfoArea(
    name,
    title,
    message,
    type)
{
    let text = getExceptionMessages(
        null,
        message);

    if ((text != null) &&
        (text.length > 0))
    {
        $(`#{name}_area_title`).html(title);
        $(`#{name}_area_text`).html(text);
        $(`#{name}_area`).removeClass('bg-danger');
        $(`#{name}_area`).removeClass('bg-warning');
        $(`#{name}_area`).removeClass('bg-success');
        $(`#{name}_area`).removeClass('bg-info');
        $(`#{name}_area`).addClass('bg-' + type);

        showInfoArea(name);
    }
    else
    {
        hideInfoArea(name);
    }
}

function hideInfoMessage()
{
    hideInfoArea('message');
}

function showInfoMessage()
{
    showInfoArea('message');
}

function setInfoMessage(
    title,
    message,
    type)
{
    setInfoArea('message', title, message, type);
}

function documentReady(
    func)
{
    var previous = document.ready;

    if (typeof document.ready != 'function')
    {
        document.ready = func;
    }
    else
    {
        document.ready = function ()
        {
            if (previous)
            {
                previous();
            }

            func();
        }
    }
}

function setElementState(
    element,
    enabled)
{
    if (element != null)
    {
        if (enabled)
        {
            element.removeAttr('disabled');
        }
        else
        {
            element.attr('disabled', 'disabled');
        }
    }
}

function isChecked(
    elementId)
{
    return ($('#' + elementId + ':checkbox:checked').length > 0);
}

function getSelectedValueAsBool(
    elementId)
{
    let result = null;
    let element = $('#' + elementId);

    if (element != null)
    {
        let value = Math.floor(element.val());

        result = (value == 1) ? true : false;
    }

    return result;
}

function getSelectedValueAsInt(
    elementId)
{
    let selected = null;
    let element = $('#' + elementId);

    if (element != null)
    {
        selected = Math.floor(element.val());
    }

    return selected;
}

function getSelectedValueAsFloat(
    elementId)
{
    let selected = null;
    let element = $('#' + elementId);

    if (element != null)
    {
        selected = parseFloat(element.val());
    }

    return selected;
}

function getSelectedValueAsString(
    elementId)
{
    let selected = null;
    let element = $('#' + elementId);

    if (element != null)
    {
        selected = element.val();
    }

    return selected;
}

function replacePlaceholder(
    text,
    placeholder,
    value)
{
    let currentText = text;
    let newText = text;

    do
    {
        currentText = newText;
        newText = currentText.replace('$$' + placeholder + '$$', value);
    }
    while (currentText != newText)

    return newText;
}

function changeStateOfElements(
    source,
    element,
    enabled)
{
    $('a, input, button, div', element).each(
        function ()
        {
            if (source.attr('id') != $(this).attr('id'))
            {
                changeElementState(
                    $(this),
                    enabled);
            }
        });
}

function changeElementState(
    element,
    enabled)
{
    if (element != null)
    {
        let tag = element.prop('tagName').toLowerCase();

        if (tag == 'a')
        {
            if (isNullOrWhiteSpace(element.data('href')))
            {
                element.data('href', element.attr('href'))
            }

            if (enabled)
            {
                element.attr('href', element.data('href'));

                element.removeClass('font-italic');
                element.removeClass('text-muted');
            }
            else
            {
                element.removeAttr('href');

                element.addClass('font-italic');
                element.addClass('text-muted');
            }
        }
        else if ((tag == 'input') ||
                 (tag == 'button'))
        {
            element.prop('disabled', !enabled);
        }
        else if (tag == 'div')
        {
            let drop = element.data('acceptdrop');

            if (!isNullOrWhiteSpace(drop))
            {
                if (enabled)
                {
                    element.show();
                }
                else
                {
                    element.hide();
                }
            }
        }
    }
}

window.onerror = function (msg, url, lineNo, columnNo, error)
{
    try
    {
        var parts = msg.split(":");

        setInfoMessage(
            parts[0],
            parts[1],
            "danger");
    }
    catch (err)
    {
        setInfoMessage(
            "Unexpected Error",
            msg,
            "danger");
    }

    return false;
};
