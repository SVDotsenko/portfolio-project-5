/**
 * @fileoverview Unit tests for the Toast module.
 * @module ToastTest
 */

/**
 * Mock implementation of the Toast class.
 * @constructor
 */
const Toast = require('./toast.js');

function MockToast() {
    this.show = jest.fn();
}

global.bootstrap = {
    Toast: MockToast
};

describe('Toast', () => {
    beforeEach(() => {
        document.body.innerHTML = '<div id="toast"><div class="toast-body"></div></div>';
        Toast.params.element = document.getElementById('toast');
    });

    test('should set message correctly', () => {
        Toast.setMessage('Test message');
        expect(Toast.params.element.querySelector('.toast-body').innerText).toBe('Test message');
    });

    test('should remove previous color class correctly', () => {
        Toast.params.element.classList.add('text-bg-info');
        Toast.removePreviousColorClass();
        expect(Toast.params.element.classList.contains('text-bg-info')).toBeFalsy();
    });

    test('should set color correctly', () => {
        Toast.setColor('text-bg-warning');
        expect(Toast.params.element.classList.contains('text-bg-warning')).toBeTruthy();
    });

    test('should process parameters correctly', () => {
        const mockParams = {
            messageTags: 'success',
            message: 'Test message'
        };
        Toast.processParameters(mockParams, Toast.paramsToFunction);
        expect(Toast.params.element.querySelector('.toast-body').innerText).toBe('Test message');
        expect(Toast.params.element.classList.contains('text-bg-success')).toBeTruthy();
    });

    test('should show toast correctly', () => {
        const mockToastInstance = new MockToast();
        jest.spyOn(mockToastInstance, 'show');
        global.bootstrap.Toast = jest.fn(() => mockToastInstance);
        Toast.show();
        expect(mockToastInstance.show).toHaveBeenCalled();
    });
});