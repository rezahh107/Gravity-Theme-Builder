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
            root.GTB_SRWF_BINARY_CHOICE_GEOMETRY_V033 = geometry;
            return geometry;
        }

        function augmentExistingReport() {
            var geometry = collectNow();
            var report = root.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03;
            if (report && typeof report === 'object') {
                report.binaryChoiceGeometry = geometry;
            }
        }

        collectNow();

        if (button && typeof button.addEventListener === 'function') {
            // runtime-diagnostic.js registers first and captures on pointerdown. This
            // later handler augments that same report object before the subsequent click download.
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

    var VERSION = '0.3.3';
    var FIELD_SELECTOR = '.gform-theme--framework.srwf-registration-theme_wrapper .gfield.srwf-role-binary-choice';
    var MAX_FIELDS = 4;
    var MAX_CHOICES = 4;

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

    function styleValue(element, view, property) {
        if (!element || !view || typeof view.getComputedStyle !== 'function') {
            return '';
        }
        var style = view.getComputedStyle(element);
        return String(style && style[property] || '');
    }

    function associatedLabel(choice, input) {
        if (!choice || !input || !input.id || !choice.children) {
            return null;
        }
        var children = bounded(choice.children, 8);
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

    function choiceSnapshot(choice, view) {
        var input = choice && typeof choice.querySelector === 'function'
            ? choice.querySelector('.gfield-choice-input[type="radio"]')
            : null;
        var label = associatedLabel(choice, input);
        return {
            choiceRect: rect(choice),
            labelRect: rect(label),
            checked: Boolean(input && input.checked),
            labelAssociated: Boolean(label),
            inputVisibleGeometry: rect(input),
            inputPosition: styleValue(input, view, 'position'),
            inputOpacity: styleValue(input, view, 'opacity')
        };
    }

    function geometrySummary(choiceSnapshots) {
        var usable = choiceSnapshots.filter(function (item) {
            return item.choiceRect && item.choiceRect.width > 0 && item.choiceRect.height > 0;
        });
        if (usable.length < 2) {
            return { sameRow: null, widthDeltaPx: null, approximatelyEqualWidths: null };
        }
        var firstY = usable[0].choiceRect.y;
        var sameRow = usable.every(function (item) {
            return Math.abs(item.choiceRect.y - firstY) <= 1;
        });
        var widths = usable.map(function (item) { return item.choiceRect.width; });
        var widthDelta = Math.max.apply(Math, widths) - Math.min.apply(Math, widths);
        return {
            sameRow: sameRow,
            widthDeltaPx: widthDelta,
            approximatelyEqualWidths: widthDelta <= 2
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
        var display = styleValue(field, view, 'display');
        var visibility = styleValue(field, view, 'visibility');
        return {
            fieldStructuralId: structuralId(field),
            fieldClasses: classes(field),
            visible: Boolean(fieldRect && fieldRect.width > 0 && fieldRect.height > 0 && display !== 'none' && visibility !== 'hidden'),
            fieldRect: fieldRect,
            choiceCount: choices.length,
            container: {
                rect: rect(container),
                display: styleValue(container, view, 'display'),
                flexDirection: styleValue(container, view, 'flexDirection'),
                gap: styleValue(container, view, 'gap')
            },
            choices: snapshots,
            geometry: geometrySummary(snapshots)
        };
    }

    function collect(documentObject, view) {
        var fields = documentObject && typeof documentObject.querySelectorAll === 'function'
            ? bounded(documentObject.querySelectorAll(FIELD_SELECTOR), MAX_FIELDS)
            : [];
        return {
            diagnosticVersion: VERSION,
            role: 'srwf-role-binary-choice',
            fieldCount: fields.length,
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
