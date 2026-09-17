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
        querySelectorAll: () => [], closest: () => null
    };
    Object.defineProperty(el, 'value', { get() { throw new Error('private control data accessed'); } });
    Object.defineProperty(el, 'textContent', { get() { throw new Error('displayed text accessed'); } });
    Object.defineProperty(el, 'innerText', { get() { throw new Error('displayed text accessed'); } });
    return el;
}
const style = new Proxy({ getPropertyValue: () => '' }, { get(target, prop) { return prop in target ? target[prop] : ''; } });
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
const source = element('select', ['tomselected', 'ts-hidden-accessible']);
source.options = options;
const wrapper = element('div', ['ts-wrapper']);
const control = element('div', ['ts-control']);
const dropdown = element('div', ['ts-dropdown']);
wrapper.querySelectorAll = (selector) => selector === '.ts-control' ? [control] : selector === '.ts-dropdown' ? [dropdown] : [];
source.tomselect = { wrapper };
const target = element('div', ['gform-theme--framework', 'srwf-registration-theme_wrapper']);
target.querySelectorAll = (selector) => {
    if (selector === 'input, select, textarea, button') return Array.from({ length: 100 }, (_, i) => i === 0 ? source : element('input', []));
    if (selector === 'select.tomselected, select.ts-hidden-accessible') return [source];
    return [];
};
target.contains = () => false;
const consumers = api.collectConsumers(target, { activeElement: null }, view);
assert.strictEqual(consumers.normalControls.length, api.BUDGETS.normalControls, 'normal control budget not enforced');
assert.strictEqual(consumers.normalControls[0].optionCount, 950, 'aggregate option count missing');
assert.strictEqual(consumers.enhancedSelects.length, 1, 'Tom Select collector starved after large select');
assert.strictEqual(consumers.enhancedSelects[0].associations.length, 1, 'Tom Select association not captured');
assert.strictEqual(consumers.enhancedSelects[0].associations[0].controls.length, 1, 'visible Tom Select control not captured');
assert.strictEqual(forbiddenOptionAccess, 0, 'option descendants were accessed');
assert.strictEqual(consumers.fileUploadProConsumer.state, 'NOT_PROVEN');
assert.strictEqual(consumers.persianGravityConsumer.state, 'NOT_PROVEN');
console.log('PASS: diagnostic v0.2 bounded/privacy-safe fixture');
