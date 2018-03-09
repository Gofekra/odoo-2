odoo.define('cotong.website.editor', function (require) {
"use strict";


var Class = require('web.Class');
var ajax = require('web.ajax');
var core = require('web.core');
var Widget = require('web.Widget');
var editor = require('web_editor.editor');
var animation = require('web_editor.snippets.animation');
var options = require('web_editor.snippets.options');

var qweb = core.qweb;
var _t = core._t;

var web_editor = require('web_editor.snippet.editor');



web_editor.Class.include({

	make_snippet_draggable: function ($snippets) {
        var self = this;
        var $tumb = $snippets.find(".oe_snippet_thumbnail_img:first");
        var left = $tumb.outerWidth()/2;
        var top = $tumb.outerHeight()/2;
        var $toInsert, dropped, $snippet;

        $snippets.draggable({
            greedy: true,
            helper: 'clone',
            zIndex: '1000',
            appendTo: 'body',
            cursor: "move",
            handle: ".oe_snippet_thumbnail",
            distance: 30,
            cursorAt: {
                'left': left,
                'top': top
            },
            start: function () {
                dropped = false;
                // snippet_selectors => to get drop-near, drop-in
                $snippet = $(this);
                var $base_body = $snippet.find('.oe_snippet_body');
                var $selector_siblings = $();
                var $selector_children = $();
                var temp = self.templateOptions;
                for (var k in temp) {
                    if ($base_body.is(temp[k].base_selector)) {
                        if (temp[k]['drop-near']) {
                            if (!$selector_siblings) $selector_siblings = temp[k]['drop-near'].all();
                            else $selector_siblings = $selector_siblings.add(temp[k]['drop-near'].all());
                        }
                        if (temp[k]['drop-in']) {
                            if (!$selector_children) $selector_children = temp[k]['drop-in'].all();
                            else $selector_children = $selector_children.add(temp[k]['drop-in'].all());
                        }
                    }
                }

                $toInsert = $base_body.clone().data("name", $snippet.find(".oe_snippet_thumbnail_title").text());

                if (!$selector_siblings.length && !$selector_children.length) {
                    console.warn($snippet.find(".oe_snippet_thumbnail_title").text() + " have not insert action: data-drop-near or data-drop-in");
                    return;
                }

                self.make_active(false);
                self.activate_insertion_zones($selector_siblings, $selector_children);

                $('.oe_drop_zone').droppable({
                    over: function (event) {
                        dropped = true;
                        $(this).first().after($toInsert).addClass('hidden');

                    },
                    out: function () {
                        var prev = $toInsert.prev();
                        if(this === prev[0]) {
                            dropped = false;
                            $toInsert.detach();
                            $(this).removeClass('hidden');
                        }
                    },
                });

                 $('#footer').tooltip('show');
            },
            stop: function (ev, ui) {

                $('#footer').tooltip('destroy');
                
                $toInsert.removeClass('oe_snippet_body');

                if (! dropped && self.$editable.find('.oe_drop_zone') && ui.position.top > 3 && ui.position.left + 50 > self.$el.outerWidth()) {
                    var el = self.$editable.find('.oe_drop_zone').nearest({x: ui.position.left, y: ui.position.top}).first();
                    if (el.length) {
                        el.after($toInsert);
                        dropped = true;
                    }
                }

                self.$editable.find('.oe_drop_zone').droppable('destroy').remove();

                if (dropped) {

                    var prev = $toInsert.first()[0].previousSibling;
                    var next = $toInsert.last()[0].nextSibling;
                    var rte = self.getParent().rte;

                    if (prev) {
                        $toInsert.detach();
                        rte.historyRecordUndo($(prev));
                        $toInsert.insertAfter(prev);
                    } else if (next) {
                        $toInsert.detach();
                        rte.historyRecordUndo($(next));
                        $toInsert.insertBefore(next);
                    } else {
                        var $parent = $toInsert.parent();
                        $toInsert.detach();
                        rte.historyRecordUndo($parent);
                        $parent.prepend($toInsert);
                    }

                    $toInsert.closest(".o_editable").trigger("content_changed");

                    var $target = false;
                    $target = $toInsert;

                    setTimeout(function () {
                        self.$el.trigger('snippet-dropped', $target);

                        animation.start(true, $target);

                        self.call_for_all_snippets($target, function (editor, $snippet) {
                            _.defer(function () { editor.drop_and_build_snippet(); });
                        });
                        self.create_snippet_editor($target);
                        self.cover_target($target.data('overlay'), $target);
                        $target.closest(".o_editable").trigger("content_changed");

                        self.make_active($target);
                        $("[data-toggle='tooltip']:not(#footer)").tooltip();
                         $('#footer').tooltip('hide');

                    },0);
                } else {
                    $toInsert.remove();
                }
            },
        });
    },
})
});