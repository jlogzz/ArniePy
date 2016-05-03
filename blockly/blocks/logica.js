'use strict';

goog.provide('Blockly.Blocks.logic');

goog.require('Blockly.Blocks');

Blockly.Blocks['if'] = {
  init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("si");
    this.appendStatementInput("condicion")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("fin");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
