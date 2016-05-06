var blocklyArea = document.getElementById('blocklyArea');
var blocklyDiv = document.getElementById('blocklyDiv');
var workspace = Blockly.inject('blocklyDiv',
    {media: 'media/',
     toolbox: document.getElementById('toolbox'),
     zoom:
     {controls: true,
      wheel: true,
      startScale: 1.0,
      maxScale: 3,
      minScale: 0.3,
      scaleSpeed: 1.2},
 trashcan: true});
 Blockly.Xml.domToWorkspace(workspace,
     document.getElementById('blocksInicio'));

     document.getElementById('compilar').addEventListener('click', compilar);

var onresize = function(e) {
 // Compute the absolute coordinates and dimensions of blocklyArea.
 var element = blocklyArea;
 var x = 0;
 var y = 0;
 do {
   x += element.offsetLeft;
   y += element.offsetTop;
   element = element.offsetParent;
 } while (element);
 // Position blocklyDiv over blocklyArea.
 blocklyDiv.style.left = x + 'px';
 blocklyDiv.style.top = y + 'px';
 blocklyDiv.style.width = blocklyArea.offsetWidth + 'px';
 blocklyDiv.style.height = blocklyArea.offsetHeight + 'px';
};

function myUpdateFunction(event) {
  var xml = Blockly.Xml.workspaceToDom(workspace);
  var xml_text = Blockly.Xml.domToText(xml);
 var code = Blockly.JavaScript.workspaceToCode(workspace);
 document.getElementById('text').value = code; //=xml_text para sacar el codigo de blocques
}

function insertToConsole(text){
  text = text.split('\n');
  var consoleB = document.getElementById('console-body');
  for (line in text){
    var li = document.createElement('li');
    li.innerHTML = text[line];
    consoleB.appendChild(li);
  }
  
  consoleB.scrollTop = consoleB.scrollHeight;
}

function compilar(){
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "../parser.py?filename=codigo.txt", true);
  xhr.onload = function(e) {
    alert("si");
    var client = new XMLHttpRequest();
    client.open('GET', '../output.txt');
    client.onload = function() {
      insertToConsole(client.responseText);
    }
    client.send();
  }
  xhr.send();
}

(function () {
  var textFile = null,
    makeTextFile = function (text) {
      var textoSplit = text.split('\n');
      var arreglo = [];
      for(var i = 0;i < textoSplit.length;i++){
        arreglo.push(textoSplit[i]+"\r\n");
       }
      var data = new Blob(arreglo, {type: 'text/plain'});

      // If we are replacing a previously generated file we need to
      // manually revoke the object URL to avoid memory leaks.
      if (textFile !== null) {
        window.URL.revokeObjectURL(textFile);
      }

      textFile = window.URL.createObjectURL(data);//saveAs(blob, "archivo_codigo.txt", true);

      return textFile;
    };


    var create = document.getElementById('crear'),
      textbox = document.getElementById('text');

    create.addEventListener('click', function () {
      var link = document.getElementById('linkDescarga');
      link.href = makeTextFile(textbox.value);
      link.style.display = 'inline';
    }, false);
  })();

//cuidado con las dos lineas de abajo
window.LoopTrap = 1000;
Blockly.JavaScript.INFINITE_LOOP_TRAP = 'if(--window.LoopTrap == 0) throw "Infinite loop.";\n';
workspace.addChangeListener(myUpdateFunction);
window.addEventListener('resize', onresize, false);
onresize();
