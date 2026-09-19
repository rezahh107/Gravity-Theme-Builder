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

function choice(x, width, checked, labelWidth) {
    const wrapper = node('div', ['gchoice'], { x, y: 100, width, height: 52 });
    const input = node('input', ['gfield-choice-input'], { x: x + 1, y: 101, width: 1, height: 1 });
    input.id = `choice_fixture_${x}_${width}`;
    input.checked = checked;
    const label = node('label', ['gform-field-label', 'gform-field-label--type-inline'], {
        x,
        y: 100,
        width: typeof labelWidth === 'number' ? labelWidth : width,
        height: 52
    });
    label.setAttribute('for', input.id);
    wrapper.children = [input, label];
    wrapper.querySelector = (selector) => selector === '.gfield-choice-input[type="radio"]' ? input : null;
    return wrapper;
}

function radioField(id, y, role, widths, selectedIndex) {
    const classes = ['gfield', 'gfield--type-radio', 'gfield--type-choice', 'gfield--input-type-radio', 'gfield--width-half'];
    if (role) classes.push(role);
    let visible = true;
    const field = node('fieldset', classes, { x: 0, y, width: 400, height: 84 });
    field.id = id;
    const resolvedWidths = widths || [194, 194];
    let x = 0;
    const choices = resolvedWidths.map((width, index) => {
        const item = choice(x, width, index === selectedIndex);
        x += width + 12;
        return item;
    });
    const container = node('div', ['gfield_radio'], { x: 0, y: 100, width: 400, height: 52 });
    container.querySelectorAll = (selector) => selector === '.gchoice' ? choices : [];
    field.querySelector = (selector) => (
        selector === '.ginput_container_radio .gfield_radio' || selector === '.gfield_radio'
            ? container
            : null
    );
    field.getBoundingClientRect = () => visible
        ? ({ x: 0, y, width: 400, height: 84 })
        : ({ x: 0, y, width: 0, height: 0 });
    field.setVisible = (next) => { visible = Boolean(next); };
    return field;
}

const gender = radioField('field_11_92', 80, 'srwf-role-binary-choice', [194, 194], 1);
const graduation = radioField('field_11_205', 180, 'srwf-role-binary-choice', [194, 194], 1);
const ordinary = radioField('field_11_99', 280, null, [70, 70, 70, 70, 72], 0);
const hidden = radioField('field_11_300', 380, null, [194, 194], 0);
hidden.setVisible(false);

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
                borderTopWidth: '1px', borderTopColor: 'rgb(134, 144, 161)', backgroundColor: 'rgb(255, 255, 255)', minHeight: '52px',
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
    assert.strictEqual(field.container.display, 'flex');
    assert.strictEqual(field.container.flexWrap, 'wrap');
    assert.strictEqual(field.container.gap, '12px');
    assert.strictEqual(field.geometry.allVisibleLabelsFillChoices, true);
    assert.ok(field.choices.every((item) => item.labelAssociated === true));
    assert.ok(field.choices.every((item) => item.labelFillsChoice === true));
    assert.ok(field.choices.every((item) => item.labelWidthDeltaPx === 0));
    assert.ok(field.choices.every((item) => item.inputPosition === 'absolute'));
    assert.ok(field.choices.every((item) => item.inputOpacity === '0'));
}

assert.strictEqual(report.fields[0].choiceCount, 2);
assert.strictEqual(report.fields[0].geometry.visibleChoiceCount, 2);
assert.strictEqual(report.fields[0].geometry.selectedChoiceCount, 1);
assert.strictEqual(report.fields[2].choiceCount, 5, 'ordinary multi-option Radio must be measured, not only binary groups');
assert.strictEqual(report.fields[2].geometry.visibleChoiceCount, 5);
assert.strictEqual(report.fields[2].geometry.selectedChoiceCount, 1);
assert.ok(report.fields[2].fieldClasses.includes('gfield--type-radio'));
assert.ok(!report.fields[2].fieldClasses.includes('srwf-role-binary-choice'), 'ordinary Radio must be measured without a semantic role');
assert.strictEqual(report.fields[0].choices[1].checked, true);
assert.strictEqual(report.fields[0].choices[1].selectedCue.width, '14px');
assert.strictEqual(report.fields[0].choices[1].selectedCue.backgroundColor, 'rgb(29, 78, 216)');
assert.ok(report.fields[0].choices[1].selectedCue.boxShadow.includes('inset'));

hidden.setVisible(true);
const revealedReport = api.collect(documentObject, view);
const revealed = revealedReport.fields[3];
assert.strictEqual(revealed.visible, true, 'conditional Radio field must become visible when host reveals it');
assert.strictEqual(revealed.choiceCount, 2);
assert.strictEqual(revealed.geometry.visibleChoiceCount, 2);
assert.strictEqual(revealed.geometry.allVisibleLabelsFillChoices, true, 'revealed conditional Radio cards must fill their assigned cells');
assert.ok(revealed.choices.every((item) => item.labelAssociated === true));

const underfilled = radioField('field_11_999', 480, null, [200, 188], 0);
const brokenFirst = underfilled.querySelector('.gfield_radio').querySelectorAll('.gchoice')[0];
brokenFirst.children[1].getBoundingClientRect = () => ({ x: 0, y: 100, width: 96, height: 52 });
const failureDocument = {
    querySelectorAll(selector) {
        assert.strictEqual(selector, api.FIELD_SELECTOR);
        return [underfilled];
    }
};
const failureReport = api.collect(failureDocument, view);
assert.strictEqual(failureReport.fields[0].choices[0].labelFillsChoice, false);
assert.strictEqual(failureReport.fields[0].geometry.allVisibleLabelsFillChoices, false, 'diagnostic must continue to reject a visibly underfilled card');
assert.strictEqual(failureReport.fields[0].choices[0].labelWidthDeltaPx, 104);

console.log('PASS: all-radio geometry diagnostic requires full-cell labels for binary, multi-option, and revealed conditional groups and still detects underfill');
