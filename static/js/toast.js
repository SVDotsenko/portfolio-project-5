/**
 * Toast object for displaying toast messages.
 * @namespace Toast
 */
const Toast = {
    messageTagsMapping: {
        debug: 'text-bg-secondary',
        info: 'text-bg-info',
        success: 'text-bg-success',
        warning: 'text-bg-warning',
        error: 'text-bg-danger'
    },

    params: {
        messageTags: 'info',
        message: 'Hello, world!',
        delay: 20,
        autoHide: true
    },

    paramsToFunction: {
        messageTags: messageTag => Toast.setColor(Toast.messageTagsMapping[messageTag]),
        message: newMessage => Toast.setMessage(newMessage)
    },

    setMessage: message => Toast.params.element.querySelector('.toast-body').innerText = message,

    removePreviousColorClass: () => Array.from(Toast.params.element.classList).forEach(className =>
        className.startsWith('text-bg-') && Toast.params.element.classList.remove(className)),

    setColor: newClass => {
        Toast.removePreviousColorClass();
        Toast.params.element.classList.add(newClass);
    },

    processParameters: (o, f) => Object.keys(f).forEach(k => f[k](o[k])),

    show: () => {
        Toast.processParameters(Toast.params, Toast.paramsToFunction);

        new bootstrap.Toast(Toast.params.element, {
            animation: true,
            autohide: Toast.params.autoHide,
            delay: Toast.params.delay * 1000
        }).show();
    }
};

(typeof module !== 'undefined' && module.exports) && (module.exports = Toast);