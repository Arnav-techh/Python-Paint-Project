from flask import Flask, request, render_template_string, jsonify
import base64
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def paint_app():
    if request.method == 'POST':
        data_url = request.form.get('image')
        if data_url:
            # Save painting (Python logic)
            filename = f"python_paint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(data_url.split(',')[1]))
            return jsonify({"status": "saved", "filename": filename})
    
    return render_template_string('''
<!DOCTYPE html>
<html><head>
<title>🎨 Python Paint - Flask</title>
<meta name="viewport" content="width=device-width">
<style>
* {margin:0;padding:0;box-sizing:border-box;}
body{font-family:system-ui;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:20px;}
.header{text-align:center;color:white;margin-bottom:30px;}
h1{font-size:2.5em;background:linear-gradient(135deg,#a855f7,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.toolbar{background:rgba(255,255,255,0.95);padding:20px;border-radius:20px;box-shadow:0 20px 40px rgba(0,0,0,0.1);display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:20px;max-width:900px;width:100%;}
.tool-btn{padding:12px 18px;border:none;border-radius:12px;cursor:pointer;font-weight:600;transition:all 0.3s;font-size:14px;}
.tool-btn:hover,.tool-btn.active{transform:translateY(-2px);box-shadow:0 10px 25px rgba(0,0,0,0.2);}
.primary{background:linear-gradient(135deg,#10b981,#059669);color:white;}
.secondary{background:#f3f4f6;color:#374151;}
#colorPicker{width:50px;height:50px;border:none;border-radius:12px;cursor:pointer;}
#brushSize{width:80px;padding:10px;border-radius:8px;border:2px solid #e5e7eb;}
#sizeDisplay{font-weight:600;color:#374151;min-width:70px;}
.canvas-container{background:white;border-radius:20px;box-shadow:0 25px 50px rgba(0,0,0,0.15);padding:20px;max-width:900px;width:100%;}
#canvas{border-radius:12px;cursor:crosshair;display:block;box-shadow:0 10px 30px rgba(0,0,0,0.1);}
.footer{margin-top:30px;text-align:center;color:rgba(255,255,255,0.9);font-size:14px;}
a{color:#a855f7;text-decoration:none;font-weight:600;}
.python-badge{background:#ffd43b;color:#ff6b35;padding:8px 16px;border-radius:20px;font-weight:bold;font-size:16px;box-shadow:0 4px 15px rgba(255,212,59,0.4);}
@media (max-width:768px){.toolbar{flex-direction:column;gap:12px;padding:15px;}h1{font-size:2em;}}
</style></head>
<body>
<div class="header">
<h1>🎨 Python Paint</h1>
<p>Arnav Kaneriya 👨🏻‍💻 | <span class="python-badge">🐍 Flask Backend</span></p>
</div>

<div class="toolbar">
<input type="color" id="colorPicker" value="#000000" title="Color">
<input type="range" id="brushSize" min="1" max="50" value="5" title="Brush Size">
<span id="sizeDisplay">5px</span>

<button class="tool-btn secondary active" onclick="setTool('pencil')">✏️ Pencil</button>
<button class="tool-btn secondary" onclick="setTool('line')">📏 Line</button>
<button class="tool-btn secondary" onclick="setTool('rectangle')">⬜ Rectangle</button>
<button class="tool-btn secondary" onclick="setTool('oval')">○ Oval</button>
<button class="tool-btn secondary" onclick="setTool('arc')">⭕ Arc</button>
<button class="tool-btn secondary" onclick="setTool('text')">🔤 Text</button>
<button class="tool-btn secondary" onclick="setTool('eraser')">🧽 Eraser</button>

<button class="tool-btn primary" onclick="clearCanvas()">🗑️ Clear</button>
<button class="tool-btn primary" onclick="saveImage()">💾 Save (Python)</button>
</div>

<div class="canvas-container">
<canvas id="canvas" width="900" height="600"></canvas>
</div>

<div class="footer">
<p>🐍 Powered by Python Flask | <a href="https://arnav-kaneriya-portfolio.vercel.app/">Portfolio</a></p>
</div>

<script>
const canvas=document.getElementById('canvas'),ctx=canvas.getContext('2d');
let isDrawing=false,currentTool='pencil',brushColor='#000000',brushWidth=5,startX,startY,textInput=null;

function resizeCanvas(){const rect=canvas.getBoundingClientRect();canvas.width=rect.width;canvas.height=rect.height;}
resizeCanvas();window.addEventListener('resize',resizeCanvas);

function setTool(tool){currentTool=tool;document.querySelectorAll('.tool-btn').forEach(btn=>btn.classList.remove('active'));event.target.classList.add('active');canvas.style.cursor=tool==='eraser'?'grab':'crosshair';}

function clearCanvas(){ctx.clearRect(0,0,canvas.width,canvas.height);}

async function saveImage(){
    const dataUrl=canvas.toDataURL('image/png');
    const response=await fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:`image=${dataUrl}`});
    const result=await response.json();
    alert('✅ Saved by Python! '+result.filename);
}

document.getElementById('colorPicker').onchange=e=>brushColor=e.target.value;
document.getElementById('brushSize').oninput=e=>{brushWidth=e.target.value;document.getElementById('sizeDisplay').textContent=`${brushWidth}px`;};

function getMousePos(e){const rect=canvas.getBoundingClientRect();return{x:e.clientX-rect.left,y:e.clientY-rect.top};}

function startDrawing(e){isDrawing=true;const pos=getMousePos(e);startX=pos.x;startY=pos.y;if(currentTool==='text'){if(!textInput){textInput=document.createElement('input');textInput.style.cssText='position:fixed;padding:8px;font:20px Helvetica;border:2px solid #a855f7;border-radius:8px;background:white;z-index:1000;';document.body.appendChild(textInput);textInput.focus();textInput.onblur=textInput.onkeypress=ev=>{if(ev.key==='Enter'||ev.type==='blur'){ctx.font='bold 20px Helvetica';ctx.fillStyle=brushColor;ctx.fillText(textInput.value||'Text',startX,startY+20);document.body.removeChild(textInput);textInput=null;}};}}else draw(e);}

function draw(e){if(!isDrawing)return;const pos=getMousePos(e);ctx.lineCap=ctx.lineJoin='round';ctx.lineWidth=brushWidth;if(currentTool==='eraser'){ctx.globalCompositeOperation='destination-out';ctx.strokeStyle='rgba(255,255,255,1)'}else{ctx.globalCompositeOperation='source-over';ctx.strokeStyle=brushColor;}if(currentTool==='pencil'){ctx.lineTo(pos.x,pos.y);ctx.stroke();ctx.beginPath();ctx.moveTo(pos.x,pos.y);}else if(currentTool==='line'){ctx.beginPath();ctx.moveTo(startX,startY);ctx.lineTo(pos.x,pos.y);ctx.stroke();}else{ctx.clearRect(0,0,canvas.width,canvas.height);ctx.drawImage(canvas,0,0);if(currentTool==='rectangle')ctx.strokeRect(startX,startY,pos.x-startX,pos.y-startY);else if(currentTool==='oval'){ctx.beginPath();ctx.ellipse((startX+pos.x)/2,(startY+pos.y)/2,Math.abs(pos.x-startX)/2,Math.abs(pos.y-startY)/2,0,0,2*Math.PI);ctx.stroke();}else if(currentTool==='arc'){ctx.beginPath();ctx.arc(startX,startY,Math.hypot(pos.x-startX,pos.y-startY)/2,0,Math.PI*0.75);ctx.stroke();}}}

function stopDrawing(){isDrawing=false;if(currentTool!=='pencil'&&currentTool!=='eraser'&&currentTool!=='text'){ctx.globalCompositeOperation='source-over';ctx.strokeStyle=brushColor;}}

canvas.addEventListener('mousedown',startDrawing);canvas.addEventListener('mousemove',draw);canvas.addEventListener('mouseup',stopDrawing);canvas.addEventListener('mouseout',stopDrawing);
canvas.addEventListener('touchstart',(e)=>{e.preventDefault();const touch=new MouseEvent('mousedown',{clientX:e.touches[0].clientX,clientY:e.touches[0].clientY});canvas.dispatchEvent(touch);});
canvas.addEventListener('touchmove',(e)=>{e.preventDefault();const touch=new MouseEvent('mousemove',{clientX:e.touches[0].clientX,clientY:e.touches[0].clientY});canvas.dispatchEvent(touch);});
canvas.addEventListener('touchend',(e)=>{e.preventDefault();canvas.dispatchEvent(new MouseEvent('mouseup',{}));});
</script></body></html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
