'use strict';

goog.provide('Blockly.Blocks.begin_end');

goog.require('Blockly.Blocks');

Blockly.Blocks['inicio_fin'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("inicio");
    this.appendStatementInput("main")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("fin");
    this.setColour(120);
    this.setTooltip('');
    this.setHelpUrl('https://blockly-demo.appspot.com/static/demos/blockfactory/index.html');
  }
};
