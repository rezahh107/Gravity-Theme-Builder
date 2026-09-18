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
function styleRule(selector = '.gform-theme--framework .gform_button') {
    return { selectorText: selector, style: ruleStyle };
}
function groupRule(constructorName, conditionText, cssRules) {
    const rule = { constructor: { name: constructorName }, cssRules };
    if (constructorName === 'CSSMediaRule') {
        rule.media = { mediaText: conditionText };
    } else if (conditionText !== null && conditionText !== undefined) {
        rule.conditionText = conditionText;
    }
    return rule;
}
function cascadeDocument(rules) {
    return {
        styleSheets: [{ ownerNode: { id: 'gravity_forms_theme_framework-css', href: 'https://example.test/gf.css' }, cssRules: rules }],
        baseURI: 'https://example.test/'
    };
}
const cascadeView = {
    getComputedStyle: () => style,
    matchMedia: (query) => ({ matches: query === '(min-width: 1px)' }),
    CSS: { supports: (condition) => condition === '(display: grid)' }
};

// Positive control: top-level selector-list splitting remains unchanged.
const unconditional = api.collectMatchedCascade(
    submit,
    cascadeDocument([styleRule('.other, .gform-theme--framework .gform_button')]),
    cascadeView
);
assert.strictEqual(unconditional.matchedRules.length, 1, 'unconditional matched cascade branch not captured');
assert.strictEqual(unconditional.matchedRules[0].selectorBranch, '.gform-theme--framework .gform_button', 'collector stored wrong selector branch');
assert.strictEqual(unconditional.matchedRules[0].declarations['inline-size'].declared, 'var(--gf-local-width)');
assert.deepStrictEqual(unconditional.matchedRules[0].applicabilityContext, [], 'top-level rule gained synthetic condition context');

// Definitely false media descendants must never look active merely because the selector matches.
const falseMedia = api.collectMatchedCascade(
    submit,
    cascadeDocument([groupRule('CSSMediaRule', '(max-width: 0px)', [styleRule()])]),
    cascadeView
);
assert.strictEqual(falseMedia.matchedRules.length, 0, 'inactive media descendant was promoted into matchedRules');
assert.strictEqual(falseMedia.conditionalContexts.length, 1, 'inactive media context not reported');
assert.strictEqual(falseMedia.conditionalContexts[0].state, 'INACTIVE');

// Definitely active media remains collectible and carries its proven applicability context.
const activeMedia = api.collectMatchedCascade(
    submit,
    cascadeDocument([groupRule('CSSMediaRule', '(min-width: 1px)', [styleRule()])]),
    cascadeView
);
assert.strictEqual(activeMedia.matchedRules.length, 1, 'active media descendant was incorrectly excluded');
assert.strictEqual(activeMedia.conditionalContexts[0].state, 'ACTIVE');
assert.strictEqual(activeMedia.matchedRules[0].applicabilityContext.length, 1, 'active media context was not preserved on matched evidence');
assert.strictEqual(activeMedia.matchedRules[0].applicabilityContext[0].kind, 'media');

// A safely evaluated false @supports-equivalent context is excluded.
const falseSupports = api.collectMatchedCascade(
    submit,
    cascadeDocument([groupRule('CSSSupportsRule', '(display: impossible-value)', [styleRule()])]),
    cascadeView
);
assert.strictEqual(falseSupports.matchedRules.length, 0, 'inactive supports descendant was promoted into matchedRules');
assert.strictEqual(falseSupports.conditionalContexts[0].state, 'INACTIVE');

// Unassessable applicability fails closed but remains explicit bounded evidence.
const unknownContainer = api.collectMatchedCascade(
    submit,
    cascadeDocument([groupRule('CSSContainerRule', '(width > 10px)', [styleRule()])]),
    cascadeView
);
assert.strictEqual(unknownContainer.matchedRules.length, 0, 'unknown container descendant was promoted into matchedRules');
assert.strictEqual(unknownContainer.conditionalContexts.length, 1, 'unknown conditional context was silently dropped');
assert.strictEqual(unknownContainer.conditionalContexts[0].state, 'UNKNOWN');
assert.strictEqual(unknownContainer.conditionalContexts[0].kind, 'container');
assert.ok(unknownContainer.conditionalContexts.length <= api.BUDGETS.conditionalContexts, 'conditional context evidence escaped budget');

// Nested applicability is conjunctive: one inactive or unknown ancestor is enough to fail closed.
const nestedInactive = api.collectMatchedCascade(
    submit,
    cascadeDocument([
        groupRule('CSSMediaRule', '(min-width: 1px)', [
            groupRule('CSSSupportsRule', '(display: impossible-value)', [styleRule()])
        ])
    ]),
    cascadeView
);
assert.strictEqual(nestedInactive.matchedRules.length, 0, 'nested inactive condition failed open');
assert.deepStrictEqual(nestedInactive.conditionalContexts.map((item) => item.state), ['ACTIVE', 'INACTIVE']);

const nestedUnknown = api.collectMatchedCascade(
    submit,
    cascadeDocument([
        groupRule('CSSMediaRule', '(min-width: 1px)', [
            groupRule('CSSScopeRule', null, [styleRule()])
        ])
    ]),
    cascadeView
);
assert.strictEqual(nestedUnknown.matchedRules.length, 0, 'nested unknown condition failed open');
assert.deepStrictEqual(nestedUnknown.conditionalContexts.map((item) => item.state), ['ACTIVE', 'UNKNOWN']);

// Unconditional grouping such as @layer remains transparent without losing active ancestors.
const layerGroup = api.collectMatchedCascade(
    submit,
    cascadeDocument([groupRule('CSSLayerBlockRule', null, [styleRule()])]),
    cascadeView
);
assert.strictEqual(layerGroup.matchedRules.length, 1, 'unconditional grouping was not traversed');
assert.strictEqual(layerGroup.conditionalContexts.length, 0, 'unconditional grouping was mislabeled as conditional evidence');

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
