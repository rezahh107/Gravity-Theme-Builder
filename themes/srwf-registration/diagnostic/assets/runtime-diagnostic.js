(function (root, factory) {
    'use strict';

    var api = factory();

    if (typeof module === 'object' && module.exports) {
        module.exports = api;
    }

    if (root && root.document) {
        var start = function () {
            api.install(root.document, root);
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
    var DIAGNOSTIC_VERSION = '0.3.0';
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
        fileUploadProRoots: 8,
        fileUploadProDropAreasPerRoot: 4,
        fieldSignatures: 80,
        fieldShallowChildren: 8,
        stylesheetLinks: 128,
        titleConsumers: 8,
        sectionConsumers: 24,
        submitAncestorDepth: 8,
        cssRuleVisits: 4000,
        matchedCascadeRules: 96,
        themeForwardCssRuleVisits: 2000,
        isolationForms: 16
    });

    var STYLE_PROPERTIES = [
        'display', 'position', 'width', 'height', 'inlineSize',
        'minWidth', 'maxWidth', 'minInlineSize', 'maxInlineSize',
        'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
        'marginTop', 'marginRight', 'marginBottom', 'marginLeft',
        'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth',
        'borderTopStyle', 'borderRightStyle', 'borderBottomStyle', 'borderLeftStyle',
        'borderTopColor', 'borderRightColor', 'borderBottomColor', 'borderLeftColor',
        'borderRadius', 'backgroundColor', 'color', 'fontFamily', 'fontSize',
        'fontWeight', 'lineHeight', 'direction', 'boxSizing', 'zIndex',
        'visibility', 'opacity', 'flex', 'flexBasis', 'flexGrow', 'flexShrink',
        'justifyContent', 'alignItems', 'alignSelf', 'justifySelf',
        'gridTemplateColumns', 'gridColumn', 'gridColumnStart', 'gridColumnEnd'
    ];

    var CASCADE_PROPERTIES = [
        'display', 'width', 'inline-size', 'min-width', 'max-width',
        'min-inline-size', 'max-inline-size', 'flex', 'flex-basis',
        'flex-grow', 'flex-shrink', 'align-self', 'justify-self'
    ];

    var CASCADE_CUSTOM_PROPERTIES = [
        '--gf-local-display', '--gf-local-width', '--gf-local-min-width', '--gf-local-max-width'
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

    function stylesheetDescriptor(sheet, index, documentObject) {
        var owner = sheet && sheet.ownerNode ? sheet.ownerNode : null;
        var href = sheet && typeof sheet.href === 'string' ? sheet.href : (owner && typeof owner.href === 'string' ? owner.href : '');
        var pathName = '';
        try {
            pathName = href ? new URL(href, String(documentObject && documentObject.baseURI || 'http://invalid.local/')).pathname : '';
        } catch (error) {
            pathName = '';
        }
        var ownerId = owner && typeof owner.id === 'string' && /^(?:gravity|gform|srwf|gpp)[-_]/i.test(owner.id) ? owner.id : null;
        return { index: index, id: ownerId, path: pathName };
    }

    function relevantDeclarations(style) {
        var result = {};
        if (!style || typeof style.getPropertyValue !== 'function') {
            return result;
        }
        for (var i = 0; i < CASCADE_PROPERTIES.length; i += 1) {
            var property = CASCADE_PROPERTIES[i];
            var raw = String(style.getPropertyValue(property) || '').trim();
            if (raw) {
                result[property] = {
                    value: raw,
                    priority: typeof style.getPropertyPriority === 'function' ? String(style.getPropertyPriority(property) || '') : ''
                };
            }
        }
        return result;
    }

    function selectorMatches(element, selector) {
        if (!element || typeof element.matches !== 'function' || !selector) {
            return false;
        }
        try {
            return element.matches(selector);
        } catch (error) {
            return false;
        }
    }

    function scanRules(rules, element, descriptor, state, limit) {
        var list = rules || [];
        for (var i = 0; i < list.length && state.visitedRules < limit; i += 1) {
            var rule = list[i];
            state.visitedRules += 1;
            state.sourceOrder += 1;

            if (rule && typeof rule.selectorText === 'string' && rule.style && selectorMatches(element, rule.selectorText)) {
                var declarations = relevantDeclarations(rule.style);
                if (Object.keys(declarations).length && state.matchedRules.length < BUDGETS.matchedCascadeRules) {
                    state.matchedRules.push({
                        stylesheet: descriptor,
                        sourceOrder: state.sourceOrder,
                        selector: rule.selectorText,
                        declarations: declarations
                    });
                }
            }

            if (rule && rule.cssRules && state.visitedRules < limit) {
                scanRules(rule.cssRules, element, descriptor, state, limit);
            }
        }
    }

    function scanStylesheets(documentObject, element, onlyId, visitLimit) {
        var state = {
            matchedRules: [],
            visitedRules: 0,
            sourceOrder: 0,
            inaccessibleStylesheets: []
        };
        var sheets = bounded(documentObject && documentObject.styleSheets ? documentObject.styleSheets : [], BUDGETS.stylesheetLinks);

        for (var i = 0; i < sheets.length && state.visitedRules < visitLimit; i += 1) {
            var sheet = sheets[i];
            var descriptor = stylesheetDescriptor(sheet, i, documentObject);
            if (onlyId && descriptor.id !== onlyId) {
                continue;
            }
            try {
                scanRules(sheet.cssRules, element, descriptor, state, visitLimit);
            } catch (error) {
                state.inaccessibleStylesheets.push(descriptor);
            }
        }

        return state;
    }

    function resolvedCascadeCustomProperties(element, view) {
        var result = {};
        if (!element || !view || typeof view.getComputedStyle !== 'function') {
            return result;
        }
        var style = view.getComputedStyle(element);
        for (var i = 0; i < CASCADE_CUSTOM_PROPERTIES.length; i += 1) {
            var property = CASCADE_CUSTOM_PROPERTIES[i];
            result[property] = String(style.getPropertyValue(property) || '').trim();
        }
        return result;
    }

    function collectMatchedCascade(documentObject, element, view) {
        var all = scanStylesheets(documentObject, element, null, BUDGETS.cssRuleVisits);
        var theme = scanStylesheets(documentObject, element, 'srwf-registration-theme-css', BUDGETS.themeForwardCssRuleVisits);
        var themeSheet = null;
        var links = collectStylesheetOrder(documentObject);
        for (var i = 0; i < links.length; i += 1) {
            if (links[i].id === 'srwf-registration-theme-css') {
                themeSheet = links[i];
                break;
            }
        }
        return {
            inlineDeclarations: relevantDeclarations(element && element.style ? element.style : null),
            matchedRules: all.matchedRules,
            visitedRules: all.visitedRules,
            inaccessibleStylesheets: all.inaccessibleStylesheets,
            resolvedCustomProperties: resolvedCascadeCustomProperties(element, view),
            themeForward: {
                themeStylesheetFound: Boolean(themeSheet),
                themeStylesheet: themeSheet,
                matchedRules: theme.matchedRules,
                visitedRules: theme.visitedRules,
                inaccessibleStylesheets: theme.inaccessibleStylesheets
            }
        };
    }

    function collectSubmitLayout(target, documentObject, view) {
        return boundedQuery(
            target,
            'button[type="submit"].gform_button, input[type="submit"].gform_button',
            BUDGETS.submitControls
        ).map(function (submit) {
            var footer = typeof submit.closest === 'function' ? submit.closest('.gform-footer, .gform_footer') : null;
            var ancestors = [];
            var cursor = submit.parentElement;
            while (cursor && ancestors.length < BUDGETS.submitAncestorDepth) {
                ancestors.push(elementSnapshot(cursor, view));
                if (cursor === target) {
                    break;
                }
                cursor = cursor.parentElement;
            }
            return {
                submit: elementSnapshot(submit, view),
                footer: footer ? elementSnapshot(footer, view) : null,
                ancestorChain: ancestors,
                matchedCascade: collectMatchedCascade(documentObject, submit, view)
            };
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

    function collectFileUploadPro(target, view) {
        var roots = boundedQuery(target, '.gpfup', BUDGETS.fileUploadProRoots).map(function (root) {
            return {
                root: elementSnapshot(root, view),
                strictMode: Boolean(root.classList && root.classList.contains('gpfup--strict')),
                imageMode: Boolean(root.classList && root.classList.contains('gpfup--images-only')),
                dropAreas: boundedQuery(root, '.gpfup__droparea', BUDGETS.fileUploadProDropAreasPerRoot).map(function (dropArea) {
                    return elementSnapshot(dropArea, view);
                })
            };
        });
        return {
            state: roots.length ? 'RUNTIME_PROVEN' : 'NOT_OBSERVED',
            roots: roots
        };
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

    function safeCollect(name, collector, fallback, failures) {
        try {
            return collector();
        } catch (error) {
            failures.push({ collector: name, state: 'COLLECTOR_FAILED' });
            return fallback;
        }
    }

    function collectConsumers(target, documentObject, view) {
        var failures = [];
        var fileUploadPro = safeCollect('fileUploadProConsumer', function () {
            return collectFileUploadPro(target, view);
        }, { state: 'COLLECTOR_FAILED', roots: [] }, failures);

        return {
            normalControls: safeCollect('normalControls', function () {
                return collectNormalControls(target, view);
            }, [], failures),
            submitControls: safeCollect('submitControls', function () {
                return collectSubmitControls(target, view);
            }, [], failures),
            submitLayout: safeCollect('submitLayout', function () {
                return collectSubmitLayout(target, documentObject, view);
            }, [], failures),
            validationAndFocus: safeCollect('validationAndFocus', function () {
                return collectValidation(target, documentObject, view);
            }, { states: [], focusOwner: null }, failures),
            enhancedSelects: safeCollect('enhancedSelects', function () {
                return collectEnhancedSelects(target, view);
            }, [], failures),
            uploads: safeCollect('uploads', function () {
                return collectUploads(target, view);
            }, [], failures),
            titleConsumers: safeCollect('titleConsumers', function () {
                return boundedQuery(target, '.gform_title', BUDGETS.titleConsumers).map(function (element) {
                    return elementSnapshot(element, view);
                });
            }, [], failures),
            sectionConsumers: safeCollect('sectionConsumers', function () {
                return boundedQuery(target, '.gfield--type-section .gsection_title', BUDGETS.sectionConsumers).map(function (element) {
                    return elementSnapshot(element, view);
                });
            }, [], failures),
            fieldSignatures: safeCollect('fieldSignatures', function () {
                return collectFieldSignatures(target);
            }, [], failures),
            fileUploadProConsumer: fileUploadPro,
            persianGravityConsumer: { state: 'NOT_PROVEN' },
            collectorFailures: failures
        };
    }

    function collectIsolationEvidence(documentObject, targets) {
        var targetList = targets || [];
        var others = boundedQuery(documentObject, '.gform-theme--framework.gform_wrapper', BUDGETS.isolationForms).filter(function (wrapper) {
            return targetList.indexOf(wrapper) === -1;
        }).map(function (wrapper) {
            return {
                structuralId: safeStructuralId(wrapper),
                classes: safeClasses(wrapper)
            };
        });
        return {
            targetCount: targetList.length,
            unrelatedFrameworkFormCount: others.length,
            unrelatedFrameworkForms: others
        };
    }

    function run(documentObject, view) {
        var topFailures = [];
        var targets = safeCollect('targets', function () {
            return boundedQuery(documentObject, TARGET_SELECTOR, BUDGETS.targets);
        }, [], topFailures);
        var stylesheetOrder = safeCollect('stylesheetOrder', function () {
            return collectStylesheetOrder(documentObject);
        }, [], topFailures);
        var isolation = safeCollect('isolationEvidence', function () {
            return collectIsolationEvidence(documentObject, targets);
        }, { targetCount: targets.length, unrelatedFrameworkFormCount: 0, unrelatedFrameworkForms: [] }, topFailures);

        return {
            schemaVersion: SCHEMA_VERSION,
            diagnosticVersion: DIAGNOSTIC_VERSION,
            diagnosticMode: 'admin-gated-read-only-local-download',
            budgets: BUDGETS,
            stylesheetOrder: stylesheetOrder,
            isolationEvidence: isolation,
            collectorFailures: topFailures,
            targets: targets.map(function (target) {
                var targetFailures = [];
                var form = safeCollect('targetForm', function () {
                    return typeof target.querySelector === 'function' ? target.querySelector('form.srwf-registration-theme, form') : null;
                }, null, targetFailures);
                return {
                    wrapper: safeCollect('targetWrapper', function () {
                        return elementSnapshot(target, view);
                    }, null, targetFailures),
                    form: form ? safeCollect('targetFormSnapshot', function () {
                        return elementSnapshot(form, view);
                    }, null, targetFailures) : null,
                    canonicalProperties: safeCollect('canonicalProperties', function () {
                        return canonicalProperties(target, view);
                    }, {}, targetFailures),
                    consumers: collectConsumers(target, documentObject, view),
                    collectorFailures: targetFailures
                };
            })
        };
    }

    function downloadJson(documentObject, view, result) {
        if (!documentObject || !view || typeof documentObject.createElement !== 'function' ||
            typeof view.Blob !== 'function' || !view.URL || typeof view.URL.createObjectURL !== 'function') {
            return false;
        }
        var blob = new view.Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
        var url = view.URL.createObjectURL(blob);
        var link = documentObject.createElement('a');
        link.href = url;
        link.download = 'gtb-srwf-runtime-diagnostic-v0.3.0.json';
        link.setAttribute('aria-hidden', 'true');
        if (link.style) {
            link.style.display = 'none';
        }
        var host = documentObject.body || documentObject.documentElement;
        if (host && typeof host.appendChild === 'function') {
            host.appendChild(link);
        }
        if (typeof link.click === 'function') {
            link.click();
        }
        if (link.parentNode && typeof link.parentNode.removeChild === 'function') {
            link.parentNode.removeChild(link);
        }
        if (typeof view.URL.revokeObjectURL === 'function') {
            view.URL.revokeObjectURL(url);
        }
        return true;
    }

    function install(documentObject, view) {
        if (!documentObject || typeof documentObject.createElement !== 'function') {
            return null;
        }
        var existing = typeof documentObject.getElementById === 'function' ? documentObject.getElementById('gtb-srwf-runtime-diagnostic-download') : null;
        if (existing) {
            return existing;
        }

        var button = documentObject.createElement('button');
        button.id = 'gtb-srwf-runtime-diagnostic-download';
        button.type = 'button';
        button.setAttribute('dir', 'rtl');
        button.setAttribute('aria-label', 'دانلود گزارش GTB');
        if (typeof documentObject.createTextNode === 'function' && typeof button.appendChild === 'function') {
            button.appendChild(documentObject.createTextNode('دانلود گزارش GTB'));
        }
        if (button.style) {
            button.style.cssText = 'position:fixed;left:12px;bottom:12px;z-index:2147483646;min-height:36px;padding:8px 12px;border:0;border-radius:6px;background:#172033;color:#fff;font:600 12px/1.4 sans-serif;cursor:pointer';
        }

        var host = documentObject.body || documentObject.documentElement;
        if (host && typeof host.appendChild === 'function') {
            host.appendChild(button);
        }

        if (typeof button.addEventListener === 'function') {
            button.addEventListener('click', function () {
                var result;
                try {
                    result = run(documentObject, view);
                } catch (error) {
                    result = {
                        schemaVersion: SCHEMA_VERSION,
                        diagnosticVersion: DIAGNOSTIC_VERSION,
                        diagnosticMode: 'admin-gated-read-only-local-download',
                        collectorFailures: [{ collector: 'run', state: 'COLLECTOR_FAILED' }],
                        targets: []
                    };
                }
                if (view) {
                    view.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03 = result;
                }
                downloadJson(documentObject, view, result);
                if (view && view.console && typeof view.console.info === 'function') {
                    view.console.info('GTB SRWF runtime diagnostic v0.3', result);
                }
            });
        }

        return button;
    }

    return {
        SCHEMA_VERSION: SCHEMA_VERSION,
        DIAGNOSTIC_VERSION: DIAGNOSTIC_VERSION,
        BUDGETS: BUDGETS,
        selectSnapshot: selectSnapshot,
        collectNormalControls: collectNormalControls,
        collectEnhancedSelects: collectEnhancedSelects,
        collectFileUploadPro: collectFileUploadPro,
        collectSubmitLayout: collectSubmitLayout,
        collectConsumers: collectConsumers,
        shallowStructure: shallowStructure,
        downloadJson: downloadJson,
        install: install,
        run: run
    };
}));
