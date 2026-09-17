(function (root, factory) {
    'use strict';

    var api = factory();

    if (typeof module === 'object' && module.exports) {
        module.exports = api;
    }

    if (root && root.document) {
        var start = function () {
            var result = api.run(root.document, root);
            root.GTB_SRWF_RUNTIME_DIAGNOSTIC_V02 = result;
            if (root.console && typeof root.console.info === 'function') {
                root.console.info('GTB SRWF runtime diagnostic v0.2', result);
            }
        };

        if (root.document.readyState === 'loading') {
            root.document.addEventListener('DOMContentLoaded', start, { once: true });
        } else {
            start();
        }
    }
}(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this), function () {
    'use strict';

    var SCHEMA_VERSION = 'v0.2';
    var TARGET_SELECTOR = '.gform-theme--framework.srwf-registration-theme_wrapper';
    var BUDGETS = Object.freeze({
        targets: 4,
        normalControls: 64,
        submitControls: 8,
        validationNodes: 32,
        enhancedSelectSources: 12,
        tomSelectAssociationsPerSource: 4,
        uploadRoots: 16,
        uploadShallowNodesPerRoot: 24,
        fieldSignatures: 80,
        fieldShallowChildren: 8,
        stylesheetLinks: 128,
        titleConsumers: 8,
        sectionConsumers: 24
    });

    var STYLE_PROPERTIES = [
        'display', 'position', 'width', 'height', 'minWidth', 'maxWidth',
        'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
        'marginTop', 'marginRight', 'marginBottom', 'marginLeft',
        'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth',
        'borderTopStyle', 'borderRightStyle', 'borderBottomStyle', 'borderLeftStyle',
        'borderTopColor', 'borderRightColor', 'borderBottomColor', 'borderLeftColor',
        'borderRadius', 'backgroundColor', 'color', 'fontFamily', 'fontSize',
        'fontWeight', 'lineHeight', 'direction', 'boxSizing', 'zIndex',
        'visibility', 'opacity'
    ];

    var CANONICAL_PROPERTIES = [
        '--gf-font-family-base',
        '--gf-color-primary',
        '--gf-color-danger',
        '--gf-color-success',
        '--gf-ctrl-bg-color',
        '--gf-ctrl-color',
        '--gf-ctrl-border-color',
        '--gf-ctrl-border-color-focus',
        '--gf-ctrl-border-color-error',
        '--gf-ctrl-radius',
        '--gf-ctrl-size',
        '--gf-ctrl-font-size',
        '--gf-ctrl-font-weight',
        '--gf-ctrl-label-color-primary',
        '--gf-ctrl-label-font-size-primary',
        '--gf-ctrl-label-font-weight-primary',
        '--gf-ctrl-desc-color',
        '--gf-ctrl-desc-color-error',
        '--gf-ctrl-btn-bg-color-primary',
        '--gf-ctrl-btn-bg-color-hover-primary',
        '--gf-ctrl-btn-bg-color-focus-primary',
        '--gf-ctrl-btn-color-primary',
        '--gf-ctrl-btn-radius',
        '--gf-ctrl-btn-size',
        '--gf-ctrl-btn-font-size',
        '--gf-ctrl-btn-font-weight',
        '--gf-ctrl-file-zone-radius',
        '--gf-field-section-border-color',
        '--gf-form-validation-heading-color'
    ];

    var SAFE_ID_PATTERNS = [
        /^gform_wrapper_\d+$/,
        /^gform_\d+$/,
        /^gform_submit_button_\d+$/,
        /^field_\d+_\d+$/,
        /^input_\d+_\d+(?:_\d+)?$/,
        /^gform_multifile_upload_\d+_\d+$/
    ];

    function bounded(items, limit) {
        return Array.prototype.slice.call(items || [], 0, limit);
    }

    function safeClasses(element) {
        return bounded(element && element.classList ? element.classList : [], 48).map(String);
    }

    function safeStructuralId(element) {
        var id = element && typeof element.id === 'string' ? element.id : '';
        for (var i = 0; i < SAFE_ID_PATTERNS.length; i += 1) {
            if (SAFE_ID_PATTERNS[i].test(id)) {
                return id;
            }
        }
        return null;
    }

    function safeStateAttributes(element) {
        var result = {};
        var names = [
            'role', 'type', 'dir', 'aria-invalid', 'aria-expanded',
            'aria-hidden', 'aria-disabled', 'data-form-index'
        ];
        for (var i = 0; i < names.length; i += 1) {
            var name = names[i];
            if (element && typeof element.hasAttribute === 'function' && element.hasAttribute(name)) {
                result[name] = String(element.getAttribute(name));
            }
        }
        if (element) {
            result.multiple = Boolean(element.multiple);
            result.disabled = Boolean(element.disabled);
            result.required = Boolean(element.required);
        }
        return result;
    }

    function safeRect(element) {
        if (!element || typeof element.getBoundingClientRect !== 'function') {
            return null;
        }
        var rect = element.getBoundingClientRect();
        return {
            x: Number(rect.x || 0),
            y: Number(rect.y || 0),
            width: Number(rect.width || 0),
            height: Number(rect.height || 0)
        };
    }

    function computedPresentation(element, view) {
        if (!element || !view || typeof view.getComputedStyle !== 'function') {
            return {};
        }
        var style = view.getComputedStyle(element);
        var result = {};
        for (var i = 0; i < STYLE_PROPERTIES.length; i += 1) {
            var property = STYLE_PROPERTIES[i];
            result[property] = String(style[property] || '');
        }
        return result;
    }

    function canonicalProperties(element, view) {
        if (!element || !view || typeof view.getComputedStyle !== 'function') {
            return {};
        }
        var style = view.getComputedStyle(element);
        var result = {};
        for (var i = 0; i < CANONICAL_PROPERTIES.length; i += 1) {
            var property = CANONICAL_PROPERTIES[i];
            result[property] = String(style.getPropertyValue(property) || '').trim();
        }
        return result;
    }

    function elementSnapshot(element, view) {
        var rect = safeRect(element);
        var presentation = computedPresentation(element, view);
        var visible = Boolean(
            rect &&
            rect.width > 0 &&
            rect.height > 0 &&
            presentation.display !== 'none' &&
            presentation.visibility !== 'hidden' &&
            presentation.opacity !== '0'
        );
        return {
            tag: element && element.tagName ? String(element.tagName).toLowerCase() : '',
            structuralId: safeStructuralId(element),
            classes: safeClasses(element),
            state: safeStateAttributes(element),
            rect: rect,
            visible: visible,
            computed: presentation
        };
    }

    function selectSnapshot(select, view) {
        var snapshot = elementSnapshot(select, view);
        snapshot.optionCount = select && select.options ? Number(select.options.length || 0) : 0;
        snapshot.mode = select && select.multiple ? 'multiple' : 'single';
        snapshot.tomSelectEvidence = safeClasses(select).filter(function (name) {
            return name === 'tomselected' || name === 'ts-hidden-accessible';
        });
        return snapshot;
    }

    function boundedQuery(root, selector, limit) {
        if (!root || typeof root.querySelectorAll !== 'function') {
            return [];
        }
        return bounded(root.querySelectorAll(selector), limit);
    }

    function collectStylesheetOrder(documentObject) {
        return boundedQuery(documentObject, 'link[rel="stylesheet"]', BUDGETS.stylesheetLinks).map(function (link, index) {
            var path = '';
            try {
                var parsed = new URL(String(link.href || ''), String(documentObject.baseURI || 'http://invalid.local/'));
                path = parsed.pathname;
            } catch (error) {
                path = '';
            }
            return {
                index: index,
                id: safeStructuralId(link) || (typeof link.id === 'string' && /^(?:gravity|gform|srwf|gpp)[-_]/i.test(link.id) ? link.id : null),
                path: path,
                media: typeof link.media === 'string' ? link.media : ''
            };
        });
    }

    function collectNormalControls(target, view) {
        return boundedQuery(target, 'input, select, textarea, button', BUDGETS.normalControls).map(function (element) {
            if (element && String(element.tagName || '').toLowerCase() === 'select') {
                return selectSnapshot(element, view);
            }
            return elementSnapshot(element, view);
        });
    }

    function collectSubmitControls(target, view) {
        return boundedQuery(
            target,
            'button[type="submit"].gform_button, input[type="submit"].gform_button',
            BUDGETS.submitControls
        ).map(function (element) {
            return elementSnapshot(element, view);
        });
    }

    function collectValidation(target, documentObject, view) {
        var states = boundedQuery(
            target,
            '.gform_validation_errors, .gfield_error, [aria-invalid="true"]',
            BUDGETS.validationNodes
        ).map(function (element) {
            return elementSnapshot(element, view);
        });

        var focus = null;
        var active = documentObject ? documentObject.activeElement : null;
        if (active && target && typeof target.contains === 'function' && target.contains(active)) {
            focus = elementSnapshot(active, view);
        }

        return { states: states, focusOwner: focus };
    }

    function directChildrenWithClass(parent, className, limit) {
        if (!parent || !parent.children) {
            return [];
        }
        return bounded(parent.children, limit).filter(function (child) {
            return child && child.classList && typeof child.classList.contains === 'function' && child.classList.contains(className);
        });
    }

    function discoverTomSelect(source) {
        var found = [];
        function add(element, method) {
            if (!element || found.some(function (item) { return item.element === element; })) {
                return;
            }
            found.push({ element: element, method: method });
        }

        if (source && source.tomselect && source.tomselect.wrapper) {
            add(source.tomselect.wrapper, 'source.tomselect.wrapper');
        }
        if (source && source.nextElementSibling && source.nextElementSibling.classList && source.nextElementSibling.classList.contains('ts-wrapper')) {
            add(source.nextElementSibling, 'next-sibling.ts-wrapper');
        }
        directChildrenWithClass(source ? source.parentElement : null, 'ts-wrapper', 16).forEach(function (element) {
            add(element, 'parent-child.ts-wrapper');
        });
        if (source && typeof source.closest === 'function') {
            var field = source.closest('.gfield');
            var fieldMatches = boundedQuery(field, '.ts-wrapper', BUDGETS.tomSelectAssociationsPerSource);
            if (fieldMatches.length === 1) {
                add(fieldMatches[0], 'single-field.ts-wrapper');
            }
        }

        return bounded(found, BUDGETS.tomSelectAssociationsPerSource);
    }

    function collectEnhancedSelects(target, view) {
        return boundedQuery(
            target,
            'select.tomselected, select.ts-hidden-accessible',
            BUDGETS.enhancedSelectSources
        ).map(function (source) {
            var associations = discoverTomSelect(source).map(function (association) {
                var wrapper = association.element;
                return {
                    associationMethod: association.method,
                    wrapper: elementSnapshot(wrapper, view),
                    controls: boundedQuery(wrapper, '.ts-control', 2).map(function (element) {
                        return elementSnapshot(element, view);
                    }),
                    dropdowns: boundedQuery(wrapper, '.ts-dropdown', 2).map(function (element) {
                        return elementSnapshot(element, view);
                    })
                };
            });
            return {
                source: selectSnapshot(source, view),
                associations: associations
            };
        });
    }

    function shallowStructure(root, maxNodes) {
        var result = [];
        var queue = [{ element: root, depth: 0 }];
        while (queue.length && result.length < maxNodes) {
            var current = queue.shift();
            var element = current.element;
            if (!element) {
                continue;
            }
            var tag = String(element.tagName || '').toLowerCase();
            if (tag !== 'option') {
                result.push({
                    depth: current.depth,
                    tag: tag,
                    structuralId: safeStructuralId(element),
                    classes: safeClasses(element),
                    state: safeStateAttributes(element)
                });
            }
            if (current.depth >= 2 || tag === 'select' || !element.children) {
                continue;
            }
            bounded(element.children, maxNodes - result.length).forEach(function (child) {
                if (String(child.tagName || '').toLowerCase() !== 'option') {
                    queue.push({ element: child, depth: current.depth + 1 });
                }
            });
        }
        return result;
    }

    function collectUploads(target, view) {
        return boundedQuery(
            target,
            '.gform_fileupload_multifile, .ginput_container_fileupload, .gform_drop_area',
            BUDGETS.uploadRoots
        ).map(function (root) {
            return {
                root: elementSnapshot(root, view),
                shallowStructure: shallowStructure(root, BUDGETS.uploadShallowNodesPerRoot)
            };
        });
    }

    function collectFieldSignatures(target) {
        return boundedQuery(target, '.gfield', BUDGETS.fieldSignatures).map(function (field) {
            return {
                structuralId: safeStructuralId(field),
                classes: safeClasses(field),
                children: bounded(field.children || [], BUDGETS.fieldShallowChildren).map(function (child) {
                    return {
                        tag: String(child.tagName || '').toLowerCase(),
                        structuralId: safeStructuralId(child),
                        classes: safeClasses(child)
                    };
                })
            };
        });
    }

    function collectConsumers(target, documentObject, view) {
        return {
            normalControls: collectNormalControls(target, view),
            submitControls: collectSubmitControls(target, view),
            validationAndFocus: collectValidation(target, documentObject, view),
            enhancedSelects: collectEnhancedSelects(target, view),
            uploads: collectUploads(target, view),
            titleConsumers: boundedQuery(target, '.gform_title', BUDGETS.titleConsumers).map(function (element) {
                return elementSnapshot(element, view);
            }),
            sectionConsumers: boundedQuery(target, '.gfield--type-section .gsection_title', BUDGETS.sectionConsumers).map(function (element) {
                return elementSnapshot(element, view);
            }),
            fieldSignatures: collectFieldSignatures(target),
            fileUploadProConsumer: { state: 'NOT_PROVEN' },
            persianGravityConsumer: { state: 'NOT_PROVEN' }
        };
    }

    function run(documentObject, view) {
        var targets = boundedQuery(documentObject, TARGET_SELECTOR, BUDGETS.targets);
        return {
            schemaVersion: SCHEMA_VERSION,
            diagnosticMode: 'admin-gated-read-only',
            budgets: BUDGETS,
            stylesheetOrder: collectStylesheetOrder(documentObject),
            targets: targets.map(function (target) {
                var form = typeof target.querySelector === 'function' ? target.querySelector('form.srwf-registration-theme, form') : null;
                return {
                    wrapper: elementSnapshot(target, view),
                    form: form ? elementSnapshot(form, view) : null,
                    canonicalProperties: canonicalProperties(target, view),
                    consumers: collectConsumers(target, documentObject, view)
                };
            })
        };
    }

    return {
        SCHEMA_VERSION: SCHEMA_VERSION,
        BUDGETS: BUDGETS,
        selectSnapshot: selectSnapshot,
        collectNormalControls: collectNormalControls,
        collectEnhancedSelects: collectEnhancedSelects,
        collectConsumers: collectConsumers,
        shallowStructure: shallowStructure,
        run: run
    };
}));
