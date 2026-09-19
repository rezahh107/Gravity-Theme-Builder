(function (root, factory) {
    'use strict';

    var api = factory();

    if (typeof module === 'object' && module.exports) {
        module.exports = api;
    }

    function installBrowserCollector() {
        if (!root || !root.document) {
            return;
        }

        var documentObject = root.document;
        var view = root;
        var button = documentObject.getElementById('gtb-srwf-download-report');

        function collectNow() {
            var geometry = api.collect(documentObject, view);
            root.GTB_SRWF_RADIO_CARD_GEOMETRY_V035 = geometry;
            root.GTB_SRWF_BINARY_CHOICE_GEOMETRY_V033 = geometry;
            return geometry;
        }

        function augmentExistingReport() {
            var geometry = collectNow();
            var report = root.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03;
            if (report && typeof report === 'object') {
                report.binaryChoiceGeometry = geometry;
                report.radioCardGeometry = geometry;
            }
        }

        root.GTB_SRWF_COLLECT_RADIO_CARD_GEOMETRY_V035 = collectNow;
        collectNow();

        if (button && typeof button.addEventListener === 'function') {
            button.addEventListener('pointerdown', augmentExistingReport);
            button.addEventListener('click', augmentExistingReport, true);
        }
    }

    if (root && root.document) {
        if (root.document.readyState === 'loading') {
            root.document.addEventListener('DOMContentLoaded', installBrowserCollector, { once: true });
        } else {
            installBrowserCollector();
        }
    }
}(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this), function () {
    'use strict';

    var VERSION = '0.3.5';
    var FIELD_SELECTOR = '.gform-theme--framework.srwf-registration-theme_wrapper .gfield.gfield--type-radio';
    var MAX_FIELDS = 12;
    var MAX_CHOICES = 12;

    function bounded(items, limit) {
        return Array.prototype.slice.call(items || [], 0, limit);
    }

    function structuralId(element) {
        var id = element && typeof element.id === 'string' ? element.id : '';
        return /^field_\d+_\d+$/.test(id) ? id : null;
    }

    function classes(element) {
        return bounded(element && element.classList ? element.classList : [], 48).map(String);
    }

    function rect(element) {
        if (!element || typeof element.getBoundingClientRect !== 'function') {
            return null;
        }
        var value = element.getBoundingClientRect();
        return {
            x: Number(value.x || 0),
            y: Number(value.y || 0),
            width: Number(value.width || 0),
            height: Number(value.height || 0)
        };
    }

    function style(element, view, pseudo) {
        if (!element || !view || typeof view.getComputedStyle !== 'function') {
            return null;
        }
        return view.getComputedStyle(element, pseudo || null);
    }

    function styleValue(element, view, property, pseudo) {
        var computed = style(element, view, pseudo);
        return String(computed && computed[property] || '');
    }

    function isVisible(element, view) {
        var value = rect(element);
        if (!value || value.width <= 0 || value.height <= 0) {
            return false;
        }
        return styleValue(element, view, 'display') !== 'none'
            && styleValue(element, view, 'visibility') !== 'hidden'
            && styleValue(element, view, 'opacity') !== '0';
    }

    function associatedLabel(choice, input) {
        if (!choice || !input || !input.id || !choice.children) {
            return null;
        }
        var children = bounded(choice.children, 12);
        for (var i = 0; i < children.length; i += 1) {
            var child = children[i];
            if (
                child && String(child.tagName || '').toLowerCase() === 'label' &&
                typeof child.getAttribute === 'function' && child.getAttribute('for') === input.id
            ) {
                return child;
            }
        }
        return null;
    }

    function selectedCueSnapshot(label, view) {
        if (!label) {
            return null;
        }
        return {
            width: styleValue(label, view, 'width', '::before'),
            height: styleValue(label, view, 'height', '::before'),
            borderWidth: styleValue(label, view, 'borderTopWidth', '::before'),
            borderColor: styleValue(label, view, 'borderTopColor', '::before'),
            backgroundColor: styleValue(label, view, 'backgroundColor', '::before'),
            boxShadow: styleValue(label, view, 'boxShadow', '::before'),
            content: styleValue(label, view, 'content', '::before')
        };
    }

    function choiceSnapshot(choice, view) {
        var input = choice && typeof choice.querySelector === 'function'
            ? choice.querySelector('.gfield-choice-input[type="radio"]')
            : null;
        var label = associatedLabel(choice, input);
        var choiceRect = rect(choice);
        var labelRect = rect(label);
        var fillDelta = choiceRect && labelRect ? Math.abs(choiceRect.width - labelRect.width) : null;
        return {
            choiceRect: choiceRect,
            labelRect: labelRect,
            visible: isVisible(choice, view),
            checked: Boolean(input && input.checked),
            labelAssociated: Boolean(label),
            labelFillsChoice: fillDelta === null ? null : fillDelta <= 1,
            labelWidthDeltaPx: fillDelta,
            labelComputed: label ? {
                borderWidth: styleValue(label, view, 'borderTopWidth'),
                borderColor: styleValue(label, view, 'borderTopColor'),
                backgroundColor: styleValue(label, view, 'backgroundColor'),
                minHeight: styleValue(label, view, 'minHeight'),
                outlineWidth: styleValue(label, view, 'outlineWidth'),
                outlineOffset: styleValue(label, view, 'outlineOffset')
            } : null,
            selectedCue: selectedCueSnapshot(label, view),
            inputVisibleGeometry: rect(input),
            inputPosition: styleValue(input, view, 'position'),
            inputOpacity: styleValue(input, view, 'opacity')
        };
    }

    function geometrySummary(choiceSnapshots) {
        var usable = choiceSnapshots.filter(function (item) {
            return item.visible && item.choiceRect && item.choiceRect.width > 0 && item.choiceRect.height > 0;
        });
        return {
            visibleChoiceCount: usable.length,
            allVisibleLabelsFillChoices: usable.length > 0 && usable.every(function (item) {
                return item.labelAssociated && item.labelFillsChoice === true;
            }),
            selectedChoiceCount: usable.filter(function (item) { return item.checked; }).length
        };
    }

    function fieldSnapshot(field, view) {
        var container = field && typeof field.querySelector === 'function'
            ? field.querySelector('.ginput_container_radio .gfield_radio') || field.querySelector('.gfield_radio')
            : null;
        var choices = container && typeof container.querySelectorAll === 'function'
            ? bounded(container.querySelectorAll('.gchoice'), MAX_CHOICES)
            : [];
        var snapshots = choices.map(function (choice) { return choiceSnapshot(choice, view); });
        var fieldRect = rect(field);
        return {
            fieldStructuralId: structuralId(field),
            fieldClasses: classes(field),
            visible: isVisible(field, view),
            fieldRect: fieldRect,
            choiceCount: choices.length,
            container: {
                rect: rect(container),
                display: styleValue(container, view, 'display'),
                flexDirection: styleValue(container, view, 'flexDirection'),
                flexWrap: styleValue(container, view, 'flexWrap'),
                gap: styleValue(container, view, 'gap')
            },
            choices: snapshots,
            geometry: geometrySummary(snapshots)
        };
    }

    function collect(documentObject, view) {
        var allFields = documentObject && typeof documentObject.querySelectorAll === 'function'
            ? documentObject.querySelectorAll(FIELD_SELECTOR)
            : [];
        var fields = bounded(allFields, MAX_FIELDS);
        return {
            diagnosticVersion: VERSION,
            scope: 'all-authentic-radio-fields-in-admitted-srwf-registration',
            fieldSelector: FIELD_SELECTOR,
            fieldCount: fields.length,
            fieldsTruncated: Number(allFields.length || 0) > MAX_FIELDS,
            fields: fields.map(function (field) { return fieldSnapshot(field, view); })
        };
    }

    return {
        VERSION: VERSION,
        FIELD_SELECTOR: FIELD_SELECTOR,
        MAX_FIELDS: MAX_FIELDS,
        MAX_CHOICES: MAX_CHOICES,
        collect: collect
    };
}));
