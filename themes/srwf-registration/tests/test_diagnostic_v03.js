'use strict';
const assert = require('assert');
const api = require('../diagnostic/assets/runtime-diagnostic.js');

function classList(names) {
    const list = names.slice();
    list.contains = (name) => list.includes(name);
    return list;
}

function element(tag, classes) {
    const el = {
        tagName: tag.toUpperCase(), id: '', classList: classList(classes || []),
        multiple: false, disabled: false, required: false, children: [], parentElement: null,
        hasAttribute: () => false, getAttribute: () => null,
        getBoundingClientRect: () => ({ x: 0, y: 0, width: 200, height: 52 }),
        querySelectorAll: () => [], querySelector: () => null, closest: () => null,
        matches: () => false
    };
    Object.defineProperty(el, 'value', { get() { throw new Error('private control data accessed'); } });
    Object.defineProperty(el, 'textContent', { get() { throw new Error('displayed text accessed'); } });
    Object.defineProperty(el, 'innerText', { get() { throw new Error('displayed text accessed'); } });
    return el;
}

const style = new Proxy({ getPropertyValue: () => '', getPropertyPriority: () => '' }, {
    get(target, prop) { return prop in target ? target[prop] : ''; }
});
const view = { getComputedStyle: () => style };

let forbiddenOptionAccess = 0;
const options = new Proxy({ length: 950 }, {
    get(target, prop) {
        if (prop === 'length') return target.length;
        forbiddenOptionAccess += 1;
        throw new Error('option descendants were enumerated');
    },
    ownKeys() { forbiddenOptionAccess += 1; throw new Error('option collection enumerated'); }
});

const source = element('select', ['gfield_select', 'tomselected', 'ts-hidden-accessible']);
source.id = 'input_11_30';
source.options = options;
const wrapper = element('div', ['ts-wrapper', 'gfield_select', 'single', 'rtl']);
const control = element('div', ['ts-control']);
control.getBoundingClientRect = () => ({ x: 0, y: 0, width: 840, height: 39.5 });
const dropdown = element('div', ['ts-dropdown']);
wrapper.querySelectorAll = (selector) => selector === '.ts-control' ? [control] : selector === '.ts-dropdown' ? [dropdown] : [];
source.tomselect = { wrapper };

const droparea = element('div', ['gpfup__droparea']);
droparea.getBoundingClientRect = () => ({ x: 0, y: 0, width: 840, height: 96 });
const gpfup = element('div', ['gpfup', 'gpfup--strict', 'gform-theme__no-reset--children']);
gpfup.querySelectorAll = (selector) => selector === '.gpfup__droparea' ? [droparea] : [];

const target = element('div', ['gform-theme', 'gform-theme--framework', 'srwf-registration-theme_wrapper']);
target.querySelectorAll = (selector) => {
    if (selector === 'input, select, textarea, button') return Array.from({ length: 100 }, (_, i) => i === 0 ? source : element('input', []));
    if (selector === 'select.tomselected, select.ts-hidden-accessible') return [source];
    if (selector === '.gpfup') return [gpfup];
    if (selector === '.gfield') throw new Error('fixture collector failure');
    return [];
};
target.contains = () => false;

const failures = [];
const consumers = api.collectConsumers(target, { activeElement: null }, view, failures);
assert.strictEqual(consumers.normalControls.length, api.BUDGETS.normalControls, 'normal control budget not enforced');
assert.strictEqual(consumers.normalControls[0].optionCount, 950, 'aggregate option count missing');
assert.strictEqual(consumers.enhancedSelects.length, 1, 'Tom Select collector starved after large select');
assert.strictEqual(consumers.enhancedSelects[0].associations.length, 1, 'Tom Select association not captured');
assert.strictEqual(consumers.enhancedSelects[0].associations[0].controls.length, 1, 'visible Tom Select control not captured');
assert.strictEqual(consumers.fileUploadProConsumer.state, 'RUNTIME_PROVEN', 'GPFUP presence not promoted from proven class');
assert.strictEqual(consumers.fileUploadProConsumer.roots[0].dropareas.length, 1, 'GPFUP drop area presentation not captured');
assert.strictEqual(consumers.fieldSignatures.length, 0, 'failed collector did not use bounded fallback');
assert.ok(failures.some((item) => item.collector === 'fieldSignatures'), 'collector failure not isolated/reported');
assert.strictEqual(consumers.persianGravityConsumer.state, 'NOT_PROVEN');
assert.strictEqual(forbiddenOptionAccess, 0, 'option descendants were accessed');

const submit = element('button', ['gform_button', 'button']);
submit.matches = (selector) => selector === '.gform-theme--framework .gform_button';
const ruleStyle = {
    getPropertyValue: (property) => property === 'inline-size' ? 'var(--gf-local-width)' : '',
    getPropertyPriority: () => ''
};
const docForCascade = {
    styleSheets: [{ ownerNode: { id: 'gravity_forms_theme_framework-css', href: 'https://example.test/gf.css' }, cssRules: [{ selectorText: '.other, .gform-theme--framework .gform_button', style: ruleStyle }] }],
    baseURI: 'https://example.test/'
};
const cascade = api.collectMatchedCascade(submit, docForCascade, view);
assert.strictEqual(cascade.matchedRules.length, 1, 'matched cascade branch not captured');
assert.strictEqual(cascade.matchedRules[0].selectorBranch, '.gform-theme--framework .gform_button', 'collector stored wrong selector branch');
assert.strictEqual(cascade.matchedRules[0].declarations['inline-size'].declared, 'var(--gf-local-width)');

const appended = [];
const buttonDoc = {
    getElementById: () => null,
    createTextNode: (s) => ({ nodeType: 3, data: s }),
    createElement: () => ({ style: {}, setAttribute() {}, appendChild(node) { this.child = node; }, addEventListener() {} }),
    body: { appendChild(node) { appended.push(node); } }
};
const downloadControl = api.ensureDownloadControl(buttonDoc, {});
assert.ok(downloadControl, 'download control unavailable');
assert.strictEqual(downloadControl.id, 'gtb-srwf-download-report');
assert.strictEqual(appended.length, 1, 'download control not appended');

console.log('PASS: diagnostic v0.3 bounded/privacy-safe/runtime-consumer fixture');
