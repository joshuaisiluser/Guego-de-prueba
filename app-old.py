"""Apple Collector — Dark Edition | Streamlit Community Cloud."""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Apple Collector — Dark Edition",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      #MainMenu, footer, header {visibility: hidden;}
      .stApp {background: #090e19;}
      .block-container {
        max-width: 1240px;
        padding-top: .8rem;
        padding-bottom: 0;
      }
      div[data-testid="stHtml"] {margin: 0;}
      [data-testid="stAppViewContainer"] {background: #090e19;}
    </style>
    """,
    unsafe_allow_html=True,
)

# HTML5 Canvas runs on the client: no Streamlit reruns during gameplay.
GAME_HTML = r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root {color-scheme: dark; --bg:#090e19; --panel:#111b2c; --line:#283852;
      --text:#edf3ff; --muted:#9bacbf; --accent:#a1f2ba; --red:#ff6678;}
    * {box-sizing:border-box;}
    html, body {margin:0; padding:0; background:var(--bg); color:var(--text);
      font-family:Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;}
    body {overflow-x:hidden;}
    button {font:inherit; cursor:pointer;}
    .wrapper {max-width:1090px; margin:0 auto; padding:10px 12px 18px;}
    .header {display:flex; align-items:center; justify-content:space-between; gap:12px;
      margin:6px 1px 18px; flex-wrap:wrap;}
    .eyebrow {display:flex;align-items:center;gap:9px; color:#8db29f; font-size:11px;
      text-transform:uppercase;letter-spacing:2.1px;font-weight:800;margin-bottom:5px;}
    .dot {height:8px;width:8px;background:#87f3ab;border-radius:50%;box-shadow:0 0 13px #64ffa2;}
    h1 {margin:0;font-size:clamp(23px,3vw,32px);font-weight:850;letter-spacing:-1.2px;line-height:1.1;}
    h1 span {color:#93efae;}
    .sub {margin:6px 0 0;font-size:12px;color:var(--muted);}
    .header-right {display:flex;gap:8px;align-items:center;}
    .pill {border:1px solid #293b52;background:#121e30;border-radius:12px;
      padding:10px 13px; color:#c6d6e8;font-size:11px;letter-spacing:.5px;font-weight:700;}
    .stage {position:relative; width:100%;aspect-ratio:16/9;border-radius:16px;
      border:1px solid #354560; overflow:hidden;box-shadow:0 21px 70px #0008, 0 0 0 5px #111c2c;
      background:#0a1424; isolation:isolate;}
    canvas {display:block;width:100%;height:100%;outline:none;image-rendering:auto;}
    canvas:focus-visible {outline:2px solid #9fdfbd;outline-offset:-4px;}
    .hud {position:absolute;pointer-events:none;z-index:3;top:17px;left:18px;right:18px;
      display:flex;align-items:flex-start;justify-content:space-between;gap:12px;}
    .hud-card {background:#0c1524df;border:1px solid #31445b;border-radius:11px;
      padding:10px 13px;backdrop-filter:blur(8px);box-shadow:0 8px 22px #0004;}
    .hud-label {font-size:10px;letter-spacing:1.3px;color:#b7c7d8;font-weight:800;}
    .apple-pips {display:flex;gap:7px;margin-top:7px;}
    .pip {width:13px;height:13px;border-radius:50%;background:#33445a;border:1px solid #536072;
      transform:rotate(-15deg);transition:background .17s,box-shadow .17s;}
    .pip.got {background:#ff566e;border-color:#ff98a5;box-shadow:0 0 13px #ff44588c;}
    .stats {text-align:right;min-width:118px;}
    .score {font-size:18px;font-weight:900;letter-spacing:.4px;margin:2px 0 0;}
    .overlay {position:absolute;inset:0;z-index:5;display:grid;place-items:center;
      background:linear-gradient(180deg,#07111eb5,#070e1be8);backdrop-filter:blur(3px);
      transition:opacity .2s; padding:18px;}
    .overlay.hidden {opacity:0;pointer-events:none;visibility:hidden;}
    .modal {text-align:center;max-width:420px;width:100%;padding:28px 24px;
      background:#101c2ceF;border:1px solid #3b5168;border-radius:20px;
      box-shadow:0 22px 75px #0009;}
    .modal-art {font-size:46px;margin:0 auto 10px;filter:drop-shadow(0 0 13px #e9ae455e);}
    .modal-kicker {font-size:11px;letter-spacing:2.2px;text-transform:uppercase;
      color:#9bdda9;font-weight:800;margin-bottom:8px;}
    .modal h2 {font-size:clamp(25px,4vw,39px);letter-spacing:-1px;margin:0 0 9px;}
    .modal p {font-size:13px;line-height:1.65;color:#b8c5d7;margin:0 0 20px;}
    .primary {border:0;border-radius:11px;padding:13px 24px;min-width:185px;
      font-size:12px;font-weight:900;letter-spacing:1.1px;color:#0b1b19;
      background:linear-gradient(135deg,#b9ffbb,#79e4b5);
      box-shadow:0 7px 26px #5cddad42;transition:transform .15s,filter .15s;}
    .primary:hover {transform:translateY(-2px);filter:brightness(1.06);}
    .primary:active {transform:translateY(0);}
    .info {display:flex;justify-content:space-between;align-items:center;gap:16px;
      flex-wrap:wrap;padding:17px 4px 0;}
    .controls {display:flex;flex-wrap:wrap;gap:15px;align-items:center;font-size:12px;color:#a4b5c9;}
    .controls b {color:#eaf3ff;font-weight:700;}
    kbd {display:inline-grid;place-items:center;min-width:25px;height:25px;
      border:1px solid #40516b;border-bottom:3px solid #354760;background:#172337;
      padding:0 6px;margin-right:3px;border-radius:5px;color:#d9e5f5;font-size:11px;font-weight:800;}
    .again {background:#152237;border:1px solid #364a64;border-radius:10px;
      padding:10px 14px;color:#dce8f7;font-weight:800;font-size:12px;
      transition:background .15s;}
    .again:hover {background:#223752;}
    .footer {color:#708299;font-size:11px;margin:14px 4px 0;line-height:1.5;}
    @media(max-width:600px) {
      .wrapper {padding:8px 9px 14px;}
      .header {margin-bottom:13px;}
      .header-right {display:none;}
      .stage {border-radius:10px;}
      .hud {top:8px;left:8px;right:8px;}
      .hud-card {padding:5px 7px;border-radius:7px;}
      .hud-label {font-size:8px;}
      .apple-pips {gap:3px;margin-top:4px;}
      .pip {width:8px;height:8px;}
      .score {font-size:12px;}
      .stats {min-width:70px;}
      .modal {padding:15px 14px;}
      .modal-art {font-size:26px;margin-bottom:0;}
      .modal-kicker {font-size:9px;margin-bottom:4px;}
      .modal h2 {font-size:20px;margin-bottom:4px;}
      .modal p {font-size:10px;margin-bottom:10px;}
      .primary {padding:9px 14px; min-width:124px;font-size:10px;}
    }
  </style>
</head>
<body>
  <main class="wrapper">
    <header class="header">
      <div>
        <div class="eyebrow"><span class="dot"></span> PIXEL ARCADE &nbsp;/&nbsp; NIVEL 01</div>
        <h1>APPLE <span>COLLECTOR</span> <span style="color:#788ba4;font-weight:600">— DARK EDITION</span></h1>
        <p class="sub">Cinco manzanas. Un héroe diminuto. Cuidado con las espinas.</p>
      </div>
      <div class="header-right"><div class="pill">✦ DESAFÍO · 5 MANZANAS</div></div>
    </header>

    <section class="stage" id="stage" aria-label="Videojuego Apple Collector">
      <canvas id="game" width="960" height="540" tabindex="0" aria-label="Campo del juego. Haz clic y usa A y D para moverte, y espacio para saltar."></canvas>
      <div class="hud" aria-live="polite">
        <div class="hud-card">
          <div class="hud-label" id="appleText">🍎 MANZANAS &nbsp; 0 / 5</div>
          <div class="apple-pips" id="pips"><span class="pip"></span><span class="pip"></span><span class="pip"></span><span class="pip"></span><span class="pip"></span></div>
        </div>
        <div class="hud-card stats">
          <div class="hud-label">TIEMPO</div>
          <div class="score" id="timeText">00:00</div>
        </div>
      </div>
      <div class="overlay" id="overlay">
        <div class="modal">
          <div class="modal-art" id="modalArt">🍎</div>
          <div class="modal-kicker" id="modalKicker">UNA PEQUEÑA AVENTURA</div>
          <h2 id="modalTitle">¿LISTO PARA JUGAR?</h2>
          <p id="modalDescription">Recoge las <strong>5 manzanas</strong> del bosque nocturno. Usa <strong>A / D</strong> o las flechas para caminar y <strong>ESPACIO</strong> para saltar. ¡No toques las espinas rojas!</p>
          <button type="button" class="primary" id="playButton">▶ JUGAR AHORA</button>
        </div>
      </div>
    </section>

    <div class="info">
      <div class="controls">
        <span><kbd>A</kbd><kbd>D</kbd> o <kbd>←</kbd><kbd>→</kbd> <b>Mover</b></span>
        <span><kbd>W</kbd><kbd>↑</kbd><kbd>ESP</kbd> <b>Saltar</b></span>
        <span><kbd>R</kbd> <b>Reiniciar</b></span>
      </div>
      <button type="button" class="again" id="restartButton">↻ &nbsp; REINICIAR</button>
    </div>
    <p class="footer">Consejo: haz clic dentro del juego si el teclado deja de responder. Las plataformas son sólidas y puedes aterrizar sobre ellas.</p>
  </main>

<script>
(() => {
  'use strict';
  const canvas = document.getElementById('game');
  const ctx = canvas.getContext('2d');
  const overlay = document.getElementById('overlay');
  const playButton = document.getElementById('playButton');
  const restartButton = document.getElementById('restartButton');
  const appleText = document.getElementById('appleText');
  const pips = Array.from(document.querySelectorAll('.pip'));
  const timeText = document.getElementById('timeText');
  const W = 960, H = 540, GROUND = 493;
  const GRAVITY = 1710, JUMP = -690, SPEED = 280;
  const ACCEL = 2600, FRICTION = 3200;
  const PLAYER_W = 30, PLAYER_H = 36;
  const platforms = [
    {x:220,y:412,w:166,h:18},
    {x:424,y:322,w:164,h:18},
    {x:641,y:381,w:157,h:18},
  ];
  const spikes = [
    {x:177, y:GROUND, w:48, h:26},
    {x:391, y:GROUND, w:61, h:26},
    {x:579, y:GROUND, w:65, h:26},
    {x:813, y:GROUND, w:64, h:26},
  ];
  const appleLocations = [
    {x:133,y:448},
    {x:297,y:378},
    {x:501,y:287},
    {x:705,y:347},
    {x:910,y:450},
  ];
  const keys = new Set();
  let state = 'start', player, apples, count = 0, elapsed = 0;
  let particles = [], stepTime = 0, cameraShake = 0;
  let lastFrame = 0, accumulator = 0;

  function reset(autoStart = true) {
    player = {x:58,y:GROUND-PLAYER_H,w:PLAYER_W,h:PLAYER_H,
      vx:0,vy:0,grounded:true,coyote:0.10,jumpBuffer:0,facing:1};
    apples = appleLocations.map(a => ({...a, collected:false, phase:(a.x*0.017)%6.28}));
    count = 0; elapsed = 0; stepTime = 0; cameraShake = 0; particles = [];
    keys.clear();
    updateHUD();
    state = autoStart ? 'playing' : 'start';
    if (autoStart) {overlay.classList.add('hidden'); canvas.focus({preventScroll:true});}
    else {showOverlay('🍎','UNA PEQUEÑA AVENTURA','¿LISTO PARA JUGAR?',
      'Recoge las <strong>5 manzanas</strong> del bosque nocturno. Usa <strong>A / D</strong> o las flechas para caminar y <strong>ESPACIO</strong> para saltar. ¡No toques las espinas rojas!', '▶ JUGAR AHORA');}
  }

  function showOverlay(art, kicker, title, description, buttonLabel) {
    document.getElementById('modalArt').textContent = art;
    document.getElementById('modalKicker').textContent = kicker;
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalDescription').innerHTML = description;
    playButton.textContent = buttonLabel;
    overlay.classList.remove('hidden');
  }

  function updateHUD() {
    appleText.textContent = `🍎 MANZANAS   ${count} / 5`;
    for (let i=0; i<pips.length; i++) pips[i].classList.toggle('got',i<count);
    const m = Math.floor(elapsed / 60).toString().padStart(2,'0');
    const s = Math.floor(elapsed % 60).toString().padStart(2,'0');
    timeText.textContent = `${m}:${s}`;
  }

  function restart() { reset(true); }
  playButton.addEventListener('click',restart);
  restartButton.addEventListener('click',restart);
  canvas.addEventListener('pointerdown',() => canvas.focus({preventScroll:true}));

  const handled = new Set(['ArrowLeft','ArrowRight','ArrowUp','Space','KeyA','KeyD','KeyW','KeyR']);
  document.addEventListener('keydown',e => {
    if (!handled.has(e.code)) return;
    e.preventDefault();
    if (e.code === 'KeyR' && !e.repeat) {restart();return;}
    if (state === 'start' && (e.code === 'Space' || e.code === 'Enter')) {restart(); return;}
    if (state !== 'playing') return;
    keys.add(e.code);
    if ((e.code === 'Space' || e.code === 'KeyW' || e.code === 'ArrowUp') && !e.repeat) {
      player.jumpBuffer = 0.13;
    }
  },{passive:false});
  document.addEventListener('keyup',e => {keys.delete(e.code);});
  window.addEventListener('blur',() => keys.clear());
  document.addEventListener('visibilitychange',() => {if(document.hidden)keys.clear();});

  const leftPressed = () => keys.has('KeyA') || keys.has('ArrowLeft');
  const rightPressed = () => keys.has('KeyD') || keys.has('ArrowRight');
  function overlaps(a,b) {
    return a.x < b.x+b.w && a.x+a.w > b.x && a.y < b.y+b.h && a.y+a.h > b.y;
  }
  function approach(n, target, maxDelta) {
    return n < target ? Math.min(n+maxDelta,target) : Math.max(n-maxDelta,target);
  }

  // Separating Axis Theorem: rectangle vs. the actual triangle of each spike.
  function triangleHitsRect(rect, tri) {
    const polygon = [
      {x:tri.x,y:tri.y},{x:tri.x+tri.w/2,y:tri.y-tri.h},{x:tri.x+tri.w,y:tri.y}
    ];
    const corners = [
      {x:rect.x+3,y:rect.y+2},{x:rect.x+rect.w-3,y:rect.y+2},
      {x:rect.x+rect.w-3,y:rect.y+rect.h-2},{x:rect.x+3,y:rect.y+rect.h-2}
    ];
    const axes = [{x:1,y:0},{x:0,y:1}];
    for (let i=0;i<3;i++) {
      const p=polygon[i],q=polygon[(i+1)%3];
      axes.push({x:-(q.y-p.y),y:q.x-p.x});
    }
    for (const axis of axes) {
      const values1=polygon.map(p=>p.x*axis.x+p.y*axis.y);
      const values2=corners.map(p=>p.x*axis.x+p.y*axis.y);
      if(Math.max(...values1)<=Math.min(...values2) || Math.max(...values2)<=Math.min(...values1)) return false;
    }
    return true;
  }
  function hitSpikes() {
    for (const group of spikes) {
      const n=Math.ceil(group.w/16), triW=group.w/n;
      for (let i=0;i<n;i++) {
        if (triangleHitsRect(player,{x:group.x+i*triW,y:group.y,w:triW,h:group.h})) return true;
      }
    }
    return false;
  }
  function touchingApple(a) {
    const nearestX=Math.max(player.x,Math.min(a.x,player.x+player.w));
    const nearestY=Math.max(player.y,Math.min(a.y,player.y+player.h));
    return (nearestX-a.x)**2+(nearestY-a.y)**2 < 15**2;
  }
  function addParticles(x,y,color,n=12) {
    for(let i=0;i<n;i++){
      const angle=(i/n)*Math.PI*2 + Math.sin(i*5.7)*0.3;
      const speed=40+Math.random()*140;
      particles.push({x,y,vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed-45,
        life:.35+Math.random()*.4,maxLife:.75,color,size:2+Math.random()*3});
    }
  }
  function gameOver() {
    if (state!=='playing') return;
    state='dead';keys.clear();cameraShake=12;
    addParticles(player.x+15,player.y+17,'#ff5872',24);
    showOverlay('💀','FIN DEL INTENTO','GAME OVER',
      `Las espinas te atraparon. Recolectaste <strong>${count} de 5 manzanas</strong>.<br>¡Vuelve a intentarlo!`, '↻ INTENTAR OTRA VEZ');
  }
  function victory() {
    if (state!=='playing') return;
    state='won';keys.clear();
    for(let i=0;i<7;i++) addParticles(130+i*115,90+Math.random()*180,
      ['#ff7182','#a4f7bf','#ffda7e'][i%3],11);
    showOverlay('🏆','MISIÓN COMPLETADA','¡GANASTE!',
      `¡Conseguiste las <strong>5 manzanas</strong> sin rendirte!<br>Tiempo de aventura: <strong>${timeText.textContent}</strong>.`,
      '↻ JUGAR DE NUEVO');
  }

  function tick(dt) {
    stepTime += dt;
    if (cameraShake>0) cameraShake=Math.max(0,cameraShake-45*dt);
    for(const p of particles) {
      p.x += p.vx*dt;p.y += p.vy*dt;p.vy+=200*dt;p.life-=dt;
    }
    particles=particles.filter(p=>p.life>0);
    if(state!=='playing') return;
    elapsed+=dt;
    player.jumpBuffer=Math.max(0,player.jumpBuffer-dt);
    if (player.grounded) player.coyote=.11;
    else player.coyote=Math.max(0,player.coyote-dt);

    const dir=Number(rightPressed())-Number(leftPressed());
    if(dir!==0) {
      player.vx=approach(player.vx,dir*SPEED,ACCEL*dt);
      player.facing=dir;
    } else player.vx=approach(player.vx,0,FRICTION*dt);

    if(player.jumpBuffer>0 && player.coyote>0) {
      player.vy=JUMP;player.grounded=false;player.coyote=0;player.jumpBuffer=0;
      addParticles(player.x+15,player.y+player.h,'#93e9b5',5);
    }

    // First resolve horizontal collision with solid platforms.
    const prevX=player.x;
    player.x+=player.vx*dt;
    player.x=Math.max(0,Math.min(W-player.w,player.x));
    for(const p of platforms) {
      if(!overlaps(player,p))continue;
      if(prevX+player.w<=p.x+1 && player.vx>0) player.x=p.x-player.w;
      else if(prevX>=p.x+p.w-1 && player.vx<0) player.x=p.x+p.w;
      player.vx=0;
    }

    // Then resolve vertical collision, including solid platform undersides.
    const prevY=player.y;
    player.vy=Math.min(player.vy+GRAVITY*dt,950);
    player.y+=player.vy*dt;
    player.grounded=false;
    for(const p of platforms) {
      if(!overlaps(player,p))continue;
      if(prevY+player.h<=p.y+2 && player.vy>=0) {
        player.y=p.y-player.h;player.vy=0;player.grounded=true;
      } else if(prevY>=p.y+p.h-2 && player.vy<0) {
        player.y=p.y+p.h;player.vy=0;
      } else {
        // Defensive correction prevents tunneling at high speeds.
        if(player.vy>=0){player.y=p.y-player.h;player.grounded=true;}
        else player.y=p.y+p.h;
        player.vy=0;
      }
    }
    if(player.y+player.h>=GROUND){
      player.y=GROUND-player.h;player.vy=0;player.grounded=true;
    }

    if (hitSpikes()) {gameOver();return;}
    for(const a of apples) {
      if(!a.collected && touchingApple(a)) {
        a.collected=true;count++;
        addParticles(a.x,a.y,'#ff6d84',14);
        updateHUD();
        if(count===5){victory();return;}
      }
    }
    updateHUD();
  }

  function roundRect(x,y,w,h,r,fill,stroke=null) {
    ctx.beginPath();ctx.roundRect(x,y,w,h,r);
    if(fill){ctx.fillStyle=fill;ctx.fill();}
    if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=1;ctx.stroke();}
  }
  function pseudoRandom(n) {return ((Math.sin(n*127.1+78.233)*43758.5453)%1+1)%1;}

  function background() {
    const gradient=ctx.createLinearGradient(0,0,0,H);
    gradient.addColorStop(0,'#101b31');gradient.addColorStop(.61,'#142239');gradient.addColorStop(1,'#0a1624');
    ctx.fillStyle=gradient;ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#1b2f47';ctx.beginPath();ctx.arc(777,110,39,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#d9e9cb';ctx.shadowColor='#b3f4c0';ctx.shadowBlur=24;
    ctx.beginPath();ctx.arc(777,110,30,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    // Faint night sky stars.
    for(let i=0;i<90;i++){
      const x=pseudoRandom(i+1)*W,y=22+pseudoRandom(i+410)*360;
      const twinkle=(Math.sin(stepTime*1.8+i*1.7)+1)/2;
      ctx.globalAlpha=.15+twinkle*.45;
      ctx.fillStyle='#dbeaff';ctx.fillRect(x,y,i%7===0?2:1,i%7===0?2:1);
    }
    ctx.globalAlpha=1;
    // Atmospheric hills and distant trees.
    ctx.fillStyle='#101f30';
    ctx.beginPath();ctx.moveTo(0,400);
    for(let x=0;x<=W;x+=30) ctx.lineTo(x,382+Math.sin(x*.013)*22+Math.sin(x*.034)*12);
    ctx.lineTo(W,GROUND);ctx.lineTo(0,GROUND);ctx.fill();
    ctx.fillStyle='#0d1b2b';
    for(let i=0;i<17;i++){
      const x=22+i*61,h=34+pseudoRandom(i+100)*75;
      ctx.fillRect(x,GROUND-h,8,h);
      ctx.beginPath();ctx.moveTo(x-19,GROUND-h+21);ctx.lineTo(x+4,GROUND-h-21);
      ctx.lineTo(x+27,GROUND-h+21);ctx.closePath();ctx.fill();
    }
    ctx.strokeStyle='#25364b';ctx.lineWidth=1;ctx.globalAlpha=.25;
    for(let x=0;x<W;x+=32){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}
    for(let y=0;y<H;y+=32){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
    ctx.globalAlpha=1;
    // Ground tiles.
    ctx.fillStyle='#1b293b';ctx.fillRect(0,GROUND,W,H-GROUND);
    ctx.fillStyle='#557b77';ctx.fillRect(0,GROUND,W,5);
    ctx.fillStyle='#304c4d';ctx.fillRect(0,GROUND+5,W,3);
    ctx.fillStyle='#243348';
    for(let x=0;x<W;x+=35){ctx.fillRect(x+4,GROUND+18,23,2);ctx.fillRect(x+18,GROUND+33,20,2);}
  }

  function drawPlatforms() {
    for(const p of platforms){
      ctx.shadowColor='#08131f';ctx.shadowBlur=14;ctx.shadowOffsetY=10;
      roundRect(p.x,p.y,p.w,p.h,4,'#36465b','#5a687b');
      ctx.shadowBlur=0;ctx.shadowOffsetY=0;
      roundRect(p.x+2,p.y+1,p.w-4,5,2,'#7b9f96');
      ctx.fillStyle='#27354a';
      for(let x=p.x+19;x<p.x+p.w-13;x+=30) ctx.fillRect(x,p.y+10,16,2);
      // Small moss tufts.
      ctx.fillStyle='#8abe9f';ctx.fillRect(p.x+13,p.y-3,3,4);
      ctx.fillRect(p.x+p.w-25,p.y-3,4,4);
    }
  }
  function drawSpikes() {
    for(const group of spikes){
      const n=Math.ceil(group.w/16),tw=group.w/n;
      ctx.fillStyle='#541f38';ctx.fillRect(group.x,group.y-3,group.w,7);
      for(let i=0;i<n;i++){
        const x=group.x+i*tw;
        ctx.beginPath();ctx.moveTo(x,group.y);ctx.lineTo(x+tw/2,group.y-group.h);
        ctx.lineTo(x+tw,group.y);ctx.closePath();
        ctx.fillStyle='#ff607a';ctx.shadowColor='#ff406b';ctx.shadowBlur=8;
        ctx.fill();ctx.shadowBlur=0;
        ctx.beginPath();ctx.moveTo(x+tw/2,group.y-group.h+4);
        ctx.lineTo(x+tw*.27,group.y-6);
        ctx.strokeStyle='#ffb1bc';ctx.lineWidth=2;ctx.stroke();
      }
    }
  }
  function drawApple(a){
    if(a.collected)return;
    const bob=Math.sin(stepTime*3+a.phase)*3;
    ctx.save();ctx.translate(a.x,a.y+bob);
    ctx.fillStyle='#ed465c';ctx.shadowColor='#ff5069';ctx.shadowBlur=17;
    ctx.beginPath();ctx.arc(-6,3,9,0,Math.PI*2);ctx.arc(5,3,9,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(0,7,11,10,0,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;
    ctx.strokeStyle='#864c30';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(0,-4);ctx.lineTo(2,-12);ctx.stroke();
    ctx.fillStyle='#99e6a5';ctx.beginPath();ctx.ellipse(8,-10,7,3,-.55,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#ffb4b8';ctx.beginPath();ctx.ellipse(-6,-1,2,4,-.4,0,Math.PI*2);ctx.fill();
    ctx.restore();
  }
  function drawCharacter(){
    ctx.save();
    const run=Math.abs(player.vx)>30 && player.grounded;
    const bob=run?Math.sin(stepTime*19)*1.7:(player.grounded?Math.sin(stepTime*3.1)*.8:0);
    const x=Math.round(player.x),y=Math.round(player.y+bob);
    // Feet and shadow.
    ctx.fillStyle='#07111d99';ctx.beginPath();ctx.ellipse(x+15,y+player.h+3,19,5,0,0,Math.PI*2);ctx.fill();
    const footShift=run?Math.sin(stepTime*19)*4:0;
    roundRect(x+4,y+29+Math.max(0,footShift),10,8,2,'#16283e');
    roundRect(x+17,y+29+Math.max(0,-footShift),10,8,2,'#16283e');
    // Small glowing scout with a striped scarf.
    ctx.shadowColor='#7df2bd';ctx.shadowBlur=12;
    roundRect(x+2,y+2,26,29,7,'#96eac0','#bafcdf');ctx.shadowBlur=0;
    roundRect(x+5,y+6,20,17,5,'#17283b');
    const eyeDx=player.facing>0?2:-2;
    roundRect(x+10+eyeDx,y+11,4,7,1,'#edfbff');
    roundRect(x+18+eyeDx,y+11,4,7,1,'#edfbff');
    ctx.fillStyle='#4dc8ff';ctx.fillRect(x+12+eyeDx,y+14,2,3);
    ctx.fillRect(x+20+eyeDx,y+14,2,3);
    ctx.fillStyle='#ff9eac';ctx.fillRect(x+2,y+23,26,5);
    ctx.fillStyle='#f46b83';ctx.fillRect(x+(player.facing>0?1:22),y+25,7,11);
    // Little antenna.
    ctx.strokeStyle='#91ffcf';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(x+15,y+2);ctx.lineTo(x+16,y-3);ctx.stroke();
    ctx.fillStyle='#ddffab';ctx.beginPath();ctx.arc(x+16,y-5,3,0,Math.PI*2);ctx.fill();
    ctx.restore();
  }
  function drawParticles(){
    for(const p of particles){
      ctx.globalAlpha=Math.min(1,p.life/p.maxLife*2);
      ctx.fillStyle=p.color;ctx.fillRect(p.x,p.y,p.size,p.size);
    }
    ctx.globalAlpha=1;
  }
  function draw(){
    ctx.clearRect(0,0,W,H);
    ctx.save();
    if(cameraShake>0)ctx.translate((Math.random()-.5)*cameraShake,(Math.random()-.5)*cameraShake);
    background();drawPlatforms();drawSpikes();
    for(const a of apples)drawApple(a);
    drawCharacter();drawParticles();
    // Discreet map decorations.
    ctx.fillStyle='#9cb4cd8a';ctx.font='11px system-ui';
    ctx.fillText('✦ BOSQUE NOCTURNO',26,GROUND-52);
    ctx.restore();
  }
  const FIXED_STEP=1/120;
  function frame(ts){
    if(!lastFrame)lastFrame=ts;
    let dt=Math.min((ts-lastFrame)/1000,.05);
    lastFrame=ts;
    accumulator+=dt;
    while(accumulator>=FIXED_STEP){tick(FIXED_STEP);accumulator-=FIXED_STEP;}
    draw();
    requestAnimationFrame(frame);
  }
  reset(false);
  requestAnimationFrame(frame);
  // Exposes read-only diagnostics for automated local checks; not used by gameplay.
  window.__appleCollectorDebug = {snapshot:()=>({state,count,elapsed,x:player.x,y:player.y,apples:apples.map(a=>a.collected)})};
})();
</script>
</body>
</html>"""

components.html(GAME_HTML, height=830, scrolling=False)
