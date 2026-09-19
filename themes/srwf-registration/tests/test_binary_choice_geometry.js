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

function choice(x, width, checked) {
    const wrapper = node('div', ['gchoice'], { x, y: 100, width, height: 52 });
    const input = node('input', ['gfield-choice-input'], { x: x + 1, y: 101, width: 1, height: 1 });
    input.id = `choice_fixture_${x}_${width}`;
    input.checked = checked;
    const label = node('label', ['gform-field-label', 'gform-field-label--type-inline'], { x, y: 100, width, height: 52 });
    label.setAttribute('for', input.id);
    wrapper.children = [input, label];
    wrapper.querySelector = (selector) => selector === '.gfield-choice-input[type="radio"]' ? input : null;
    return wrapper;
}

function radioField(id, y, role) {
    const classes = ['gfield', 'gfield--type-radio', 'gfield--type-choice', 'gfield--input-type-radio', 'gfield--width-half'];
    if (role) classes.push(role);
    const field = node('fieldset', classes, { x: 0, y, width: 400, height: 84 });
    field.id = id;
    const first = choice(0, 194, false);
    const second = choice(206, 194, true);
    const container = node('div', ['gfield_radio'], { x: 0, y: 100, width: 400, height: 52 });
    container.querySelectorAll = (selector) => selector === '.gchoice' ? [first, second] : [];
    field.querySelector = (selector) => (
        selector === '.ginput_container_radio .gfield_radio' || selector === '.gfield_radio'
            ? container
            : null
    );
    return field;
}

const gender = radioField('field_11_92', 80, 'srwf-role-binary-choice');
const graduation = radioField('field_11_205', 180, 'srwf-role-binary-choice');
const ordinary = radioField('field_11_99', 280, null);
const hidden = radioField('field_11_300', 380, null);
hidden.getBoundingClientRect = () => ({ x: 0, y: 380, width: 0, height: 0 });

const documentObject = {
    querySelectorAll(selector) {
        assert.strictEqual(selector, api.FIELD_SELECTOR, 'collector must enumerate authentic SRWF Radio fields without semantic-role gating');
        return [gender, graduation, ordinary, hidden];
    }
};

const view = {
    getComputedStyle(element, pseudo) {
        if (pseudo === '::before') {
            return {
                display: 'block', visibility: 'visible', opacity: '1',
                width: '14px', height: '14px', borderTopWidth: '1.5px', borderTopColor: 'rgb(29, 78, 216)',
                backgroundColor: 'rgb(29, 78, 216)', boxShadow: 'rgb(237, 241, 252) 0px 0px 0px 3px inset', content: '""'
            };
        }
        if (element && element.classList && element.classList.contains('gfield_radio')) {
            return { display: 'flex', visibility: 'visible', flexDirection: 'row', flexWrap: 'wrap', gap: '12px', position: 'static', opacity: '1' };
        }
        if (element && element.classList && element.classList.contains('gfield-choice-input')) {
            return { display: 'block', visibility: 'visible', position: 'absolute', opacity: '0', flexDirection: '', flexWrap: '', gap: '' };
        }
        if (String(element && element.tagName || '').toLowerCase() === 'label') {
            return {
                display: 'flex', visibility: 'visible', position: 'static', opacity: '1', flexDirection: '', flexWrap: '', gap: '8px',
                borderTopWidth: element.parentElement && element.parentElement.checked ? '2px' : '1px',
                borderTopColor: 'rgb(134, 144, 161)', backgroundColor: 'rgb(255, 255, 255)', minHeight: '52px',
                outlineWidth: '0px', outlineOffset: '0px'
            };
        }
        return { display: 'block', visibility: 'visible', position: 'static', opacity: '1', flexDirection: '', flexWrap: '', gap: '' };
    }
};

const report = api.collect(documentObject, view);
assert.strictEqual(report.diagnosticVersion, '0.3.5');
assert.strictEqual(report.scope, 'all-authentic-radio-fields-in-admitted-srwf-registration');
assert.strictEqual(report.fieldCount, 4);
assert.strictEqual(report.fields[0].fieldStructuralId, 'field_11_92');
assert.strictEqual(report.fields[1].fieldStructuralId, 'field_11_205');
assert.strictEqual(report.fields[2].fieldStructuralId, 'field_11_99');
assert.strictEqual(report.fields[3].visible, false);
for (const field of report.fields.slice(0, 3)) {
    assert.strictEqual(field.choiceCount, 2);
    assert.strictEqual(field.container.display, 'flex');
    assert.strictEqual(field.container.flexWrap, 'wrap');
    assert.strictEqual(field.container.gap, '12px');
    assert.strictEqual(field.geometry.visibleChoiceCount, 2);
    assert.strictEqual(field.geometry.allVisibleLabelsFillChoices, true);
    assert.strictEqual(field.geometry.selectedChoiceCount, 1);
    assert.strictEqual(field.choices[0].labelAssociated, true);
    assert.strictEqual(field.choices[1].labelAssociated, true);
    assert.strictEqual(field.choices[0].labelFillsChoice, true);
    assert.strictEqual(field.choices[1].labelWidthDeltaPx, 0);
    assert.strictEqual(field.choices[0].checked, false);
    assert.strictEqual(field.choices[1].checked, true);
    assert.strictEqual(field.choices[1].inputPosition, 'absolute');
    assert.strictEqual(field.choices[1].inputOpacity, '0');
    assert.strictEqual(field.choices[1].selectedCue.width, '14px');
    assert.strictEqual(field.choices[1].selectedCue.backgroundColor, 'rgb(29, 78, 216)');
    assert.ok(field.choices[1].selectedCue.boxShadow.includes('inset'));
}
assert.ok(report.fields[2].fieldClasses.includes('gfield--type-radio'));
assert.ok(!report.fields[2].fieldClasses.includes('srwf-role-binary-choice'), 'ordinary Radio must be measured without a semantic role');

console.log('PASS: all-radio card geometry diagnostic measures visible labels, hidden groups, and authentic checked cue without reading private text/value');
