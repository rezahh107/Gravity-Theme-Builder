'use strict';
const assert = require('assert');
const api = require('../diagnostic/assets/binary-choice-geometry.js');

function classList(names) {
    const list = names.slice();
    list.contains = (name) => list.includes(name);
    return list;
}

function node(tag, classes, box) {
    const attributes = {};
    const value = {
        tagName: tag.toUpperCase(),
        id: '',
        classList: classList(classes || []),
        children: [],
        checked: false,
        getAttribute: (name) => Object.prototype.hasOwnProperty.call(attributes, name) ? attributes[name] : null,
        setAttribute: (name, attrValue) => { attributes[name] = String(attrValue); },
        getBoundingClientRect: () => box || ({ x: 0, y: 0, width: 0, height: 0 }),
        querySelector: () => null,
        querySelectorAll: () => []
    };
    Object.defineProperty(value, 'value', { get() { throw new Error('private form value accessed'); } });
    Object.defineProperty(value, 'textContent', { get() { throw new Error('displayed label text accessed'); } });
    Object.defineProperty(value, 'innerText', { get() { throw new Error('displayed label text accessed'); } });
    return value;
}

function choice(x, checked) {
    const wrapper = node('div', ['gchoice'], { x, y: 100, width: 194, height: 48 });
    const input = node('input', ['gfield-choice-input'], { x: x + 1, y: 101, width: 1, height: 1 });
    input.id = `choice_fixture_${x}`;
    input.checked = checked;
    const label = node('label', ['gform-field-label', 'gform-field-label--type-inline'], { x, y: 100, width: 194, height: 48 });
    label.setAttribute('for', input.id);
    wrapper.children = [input, label];
    wrapper.querySelector = (selector) => selector === '.gfield-choice-input[type="radio"]' ? input : null;
    return wrapper;
}

function roleField(id, y) {
    const field = node(
        'fieldset',
        ['gfield', 'gfield--type-radio', 'gfield--type-choice', 'gfield--input-type-radio', 'gfield--width-half', 'srwf-role-binary-choice', 'gfield--choice-align-vertical'],
        { x: 0, y, width: 400, height: 80 }
    );
    field.id = id;
    const first = choice(0, false);
    const second = choice(206, true);
    const container = node('div', ['gfield_radio'], { x: 0, y: 100, width: 400, height: 48 });
    container.querySelectorAll = (selector) => selector === '.gchoice' ? [first, second] : [];
    field.querySelector = (selector) => (
        selector === '.ginput_container_radio .gfield_radio' || selector === '.gfield_radio'
            ? container
            : null
    );
    return field;
}

const gender = roleField('field_11_92', 80);
const graduation = roleField('field_11_205', 180);
const ordinary = node('fieldset', ['gfield', 'gfield--type-radio', 'gfield--choice-align-vertical'], { x: 0, y: 280, width: 400, height: 120 });

const documentObject = {
    querySelectorAll(selector) {
        assert.strictEqual(selector, api.FIELD_SELECTOR, 'collector widened beyond the binary semantic role');
        return [gender, graduation];
    }
};

const view = {
    getComputedStyle(element) {
        if (element && element.classList && element.classList.contains('gfield_radio')) {
            return { display: 'flex', visibility: 'visible', flexDirection: 'row', gap: '12px', position: 'static', opacity: '1' };
        }
        if (element && element.classList && element.classList.contains('gfield-choice-input')) {
            return { display: 'block', visibility: 'visible', position: 'absolute', opacity: '0', flexDirection: '', gap: '' };
        }
        return { display: 'block', visibility: 'visible', position: 'static', opacity: '1', flexDirection: '', gap: '' };
    }
};

const report = api.collect(documentObject, view);
assert.strictEqual(report.diagnosticVersion, '0.3.3');
assert.strictEqual(report.role, 'srwf-role-binary-choice');
assert.strictEqual(report.fieldCount, 2);
assert.strictEqual(report.fields[0].fieldStructuralId, 'field_11_92');
assert.strictEqual(report.fields[1].fieldStructuralId, 'field_11_205');
for (const field of report.fields) {
    assert.strictEqual(field.choiceCount, 2);
    assert.strictEqual(field.container.display, 'flex');
    assert.strictEqual(field.container.flexDirection, 'row');
    assert.strictEqual(field.container.gap, '12px');
    assert.strictEqual(field.geometry.sameRow, true);
    assert.strictEqual(field.geometry.approximatelyEqualWidths, true);
    assert.strictEqual(field.geometry.widthDeltaPx, 0);
    assert.strictEqual(field.choices[0].labelAssociated, true);
    assert.strictEqual(field.choices[1].labelAssociated, true);
    assert.strictEqual(field.choices[0].checked, false);
    assert.strictEqual(field.choices[1].checked, true);
    assert.strictEqual(field.choices[1].inputPosition, 'absolute');
    assert.strictEqual(field.choices[1].inputOpacity, '0');
}
assert.ok(!report.fields.includes(ordinary), 'ordinary radio field leaked into binary geometry report');

console.log('PASS: binary-choice geometry diagnostic is bounded and privacy-safe');
