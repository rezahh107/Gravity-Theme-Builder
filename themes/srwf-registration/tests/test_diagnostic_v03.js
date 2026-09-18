'use strict';

const assert = require('assert');
const api = require('../diagnostic/assets/runtime-diagnostic.js');

function classList(names) {
    const list = names.slice();
    list.contains = (name) => list.includes(name);
    return list;
}

function computed(overrides = {}) {
    return new Proxy({
        getPropertyValue: (name) => overrides[name] || '',
        ...overrides
    }, {
        get(target, prop) {
            return prop in target ? target[prop] : '';
        }
    });
}

function element(tag, classes = [], overrides = {}) {
    const el = {
        tagName: tag.toUpperCase(),
        id: overrides.id || '',
        classList: classList(classes),
        children: overrides.children || [],
        parentElement: overrides.parentElement || null,
        nextElementSibling: overrides.nextElementSibling || null,
        multiple: Boolean(overrides.multiple),
        disabled: Boolean(overrides.disabled),
        required: Boolean(overrides.required),
        style: overrides.style || { getPropertyValue: () => '', getPropertyPriority: () => '' },
        hasAttribute: (name) => Boolean(overrides.attributes && Object.prototype.hasOwnProperty.call(overrides.attributes, name)),
        getAttribute: (name) => overrides.attributes ? overrides.attributes[name] : null,
        getBoundingClientRect: () => overrides.rect || ({ x: 0, y: 0, width: 200, height: 52 }),
        querySelectorAll: overrides.querySelectorAll || (() => []),
        querySelector: overrides.querySelector || (() => null),
        closest: overrides.closest || (() => null),
        matches: overrides.matches || (() => false)
    };
    Object.defineProperty(el, 'value', { get() { throw new Error('private control data accessed'); } });
    Object.defineProperty(el, 'textContent', { get() { throw new Error('displayed text accessed'); } });
    Object.defineProperty(el, 'innerText', { get() { throw new Error('displayed text accessed'); } });
    Object.defineProperty(el, 'files', { get() { throw new Error('file identity accessed'); } });
    return el;
}

const view = {
    getComputedStyle: (el) => el._computed || computed()
};

let forbiddenOptionAccess = 0;
const options = new Proxy({ length: 950 }, {
    get(target, prop) {
        if (prop === 'length') return target.length;
        forbiddenOptionAccess += 1;
        throw new Error('option descendants were enumerated');
    },
    ownKeys() {
        forbiddenOptionAccess += 1;
        throw new Error('option collection enumerated');
    }
});

const control = element('div', ['ts-control']);
control._computed = computed({ height: '39.5px', minInlineSize: 'auto' });
const dropdown = element('div', ['ts-dropdown']);
const wrapper = element('div', ['ts-wrapper'], {
    querySelectorAll: (selector) => selector === '.ts-control' ? [control] : selector === '.ts-dropdown' ? [dropdown] : []
});
const source = element('select', ['gfield_select', 'tomselected', 'ts-hidden-accessible'], { id: 'input_11_30' });
source.options = options;
source.tomselect = { wrapper };

const dropArea = element('div', ['gpfup__droparea']);
dropArea._computed = computed({ borderRadius: '0px', height: '96px' });
const gpfup = element('div', ['gpfup', 'gpfup--strict'], {
    querySelectorAll: (selector) => selector === '.gpfup__droparea' ? [dropArea] : []
});
const uploadRoot = element('div', ['gform_fileupload_multifile'], {
    id: 'gform_multifile_upload_11_208',
    children: [gpfup]
});
gpfup.parentElement = uploadRoot;

const target = element('div', ['gform-theme', 'gform-theme--framework', 'srwf-registration-theme_wrapper'], { id: 'gform_wrapper_11' });
const footer = element('div', ['gform-footer', 'gform_footer']);
const form = element('form', ['srwf-registration-theme'], { id: 'gform_11', parentElement: target });
footer.parentElement = form;
const submit = element('button', ['gform_button', 'button'], {
    id: 'gform_submit_button_11',
    parentElement: footer,
    attributes: { type: 'submit' },
    closest: (selector) => selector.includes('.gform-footer') ? footer : null,
    matches: (selector) => selector.includes('.button') || selector.includes('.gform_button')
});
submit._computed = computed({
    inlineSize: '115px',
    '--gf-local-display': 'inline-flex',
    '--gf-local-width': 'auto',
    '--gf-local-min-width': 'auto',
    '--gf-local-max-width': ''
});

const normalInputs = Array.from({ length: 99 }, () => element('input', []));
target.querySelectorAll = (selector) => {
    if (selector === 'input, select, textarea, button') return [source].concat(normalInputs);
    if (selector === 'select.tomselected, select.ts-hidden-accessible') return [source];
    if (selector === 'button[type="submit"].gform_button, input[type="submit"].gform_button') return [submit];
    if (selector === '.gform_fileupload_multifile, .ginput_container_fileupload, .gform_drop_area') return [uploadRoot];
    if (selector === '.gpfup') return [gpfup];
    if (selector === '.gform_title' || selector === '.gfield--type-section .gsection_title' || selector === '.gfield') return [];
    if (selector === '.gform_validation_errors, .gfield_error, [aria-invalid="true"]') return [];
    return [];
};
target.contains = () => false;
target.querySelector = () => form;

function cssStyle(values) {
    return {
        getPropertyValue: (name) => values[name] || '',
        getPropertyPriority: () => ''
    };
}

const hostRule = {
    selectorText: '.gform-theme.gform-theme--framework.gform_wrapper .button:where(:not(.gform-theme__disable))',
    style: cssStyle({ 'inline-size': 'var(--gf-local-width)', 'min-inline-size': 'var(--gf-local-min-width)' })
};
const themeRule = {
    selectorText: 'head:has(#gravity_forms_theme_framework-css) + body .gform-theme--framework.gform-theme.srwf-registration-theme_wrapper .gform-footer .gform_button',
    style: cssStyle({ 'inline-size': '100%' })
};
const hostOwner = { id: 'gravity_forms_theme_framework-css', href: 'https://example.test/gravity-forms-theme-framework.min.css' };
const themeOwner = { id: 'srwf-registration-theme-css', href: 'https://example.test/srwf-registration.css' };
const documentObject = {
    baseURI: 'https://example.test/form',
    activeElement: null,
    styleSheets: [
        { ownerNode: hostOwner, href: hostOwner.href, cssRules: [hostRule] },
        { ownerNode: themeOwner, href: themeOwner.href, cssRules: [themeRule] }
    ],
    querySelectorAll: () => []
};

const consumers = api.collectConsumers(target, documentObject, view);
assert.strictEqual(consumers.normalControls.length, api.BUDGETS.normalControls, 'normal control budget not enforced');
assert.strictEqual(consumers.normalControls[0].optionCount, 950, 'aggregate option count missing');
assert.strictEqual(consumers.enhancedSelects.length, 1, 'Tom Select collector starved after large select');
assert.strictEqual(consumers.enhancedSelects[0].associations.length, 1, 'Tom Select association not captured');
assert.strictEqual(consumers.enhancedSelects[0].associations[0].controls.length, 1, 'visible Tom Select control not captured');
assert.strictEqual(forbiddenOptionAccess, 0, 'option descendants were accessed');
assert.strictEqual(consumers.fileUploadProConsumer.state, 'RUNTIME_PROVEN', 'GPFUP consumer was not recognized');
assert.strictEqual(consumers.fileUploadProConsumer.roots[0].strictMode, true, 'GPFUP strict mode missing');
assert.strictEqual(consumers.fileUploadProConsumer.roots[0].dropAreas.length, 1, 'GPFUP drop area presentation missing');
assert.strictEqual(consumers.persianGravityConsumer.state, 'NOT_PROVEN');
assert.strictEqual(consumers.submitLayout.length, 1, 'Submit layout collector missing');
assert.strictEqual(consumers.submitLayout[0].matchedCascade.resolvedCustomProperties['--gf-local-width'], 'auto');
assert.ok(consumers.submitLayout[0].matchedCascade.matchedRules.some((rule) => rule.declarations['inline-size']), 'host inline-size cascade evidence missing');
assert.ok(consumers.submitLayout[0].matchedCascade.themeForward.matchedRules.some((rule) => rule.declarations['inline-size']), 'theme-forward Submit rule missing');

const failingTarget = element('div', ['gform-theme--framework', 'srwf-registration-theme_wrapper']);
failingTarget.querySelectorAll = (selector) => {
    if (selector === 'input, select, textarea, button') throw new Error('collector fixture failure');
    return [];
};
failingTarget.contains = () => false;
const isolated = api.collectConsumers(failingTarget, documentObject, view);
assert.deepStrictEqual(isolated.normalControls, [], 'failed collector did not fail closed');
assert.ok(isolated.collectorFailures.some((entry) => entry.collector === 'normalControls'), 'collector failure was not isolated/reported');
assert.deepStrictEqual(isolated.enhancedSelects, [], 'later collector did not continue after failure');

const bodyChildren = [];
let clickHandler = null;
function uiElement(tag) {
    return {
        tagName: tag.toUpperCase(),
        id: '',
        style: {},
        parentNode: null,
        setAttribute: () => {},
        appendChild: () => {},
        addEventListener: (name, handler) => { if (name === 'click') clickHandler = handler; },
        click: () => {}
    };
}
const uiDocument = {
    readyState: 'complete',
    body: {
        appendChild: (node) => {
            node.parentNode = uiDocument.body;
            bodyChildren.push(node);
        },
        removeChild: (node) => {
            const index = bodyChildren.indexOf(node);
            if (index >= 0) bodyChildren.splice(index, 1);
        }
    },
    documentElement: null,
    createElement: uiElement,
    createTextNode: (text) => ({ nodeType: 3, data: text }),
    getElementById: () => null,
    querySelectorAll: (selector) => {
        if (selector === '.gform-theme--framework.srwf-registration-theme_wrapper') throw new Error('target collection failed');
        return [];
    },
    styleSheets: []
};
const uiView = { console: { info: () => {} } };
const button = api.install(uiDocument, uiView);
assert.ok(button, 'download control was not created');
assert.strictEqual(button.id, 'gtb-srwf-runtime-diagnostic-download');
assert.strictEqual(typeof clickHandler, 'function', 'download control has no click handler');
clickHandler();
assert.ok(bodyChildren.includes(button), 'download control disappeared after collection failure');
assert.strictEqual(uiView.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03.collectorFailures[0].collector, 'targets', 'failed run did not report target collector safely');

console.log('PASS: diagnostic v0.3 bounded/privacy-safe/failure-isolated fixture');
