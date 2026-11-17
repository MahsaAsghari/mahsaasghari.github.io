/* No libraries or network requests. Research content works without JavaScript. */
(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const nav = document.querySelector('#navigation');
  const menu = document.querySelector('.menu-button');
  if (nav && menu) {
    nav.classList.add('enhanced'); menu.hidden = false;
    const close = () => { nav.classList.remove('open'); menu.setAttribute('aria-expanded','false'); };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      nav.classList.toggle('open',open); menu.setAttribute('aria-expanded',String(open));
    });
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
    document.addEventListener('keydown',e => {if(e.key==='Escape' && nav.classList.contains('open')){close();menu.focus();}});
    matchMedia('(min-width: 721px)').addEventListener('change', close);
  }
  const filters = document.querySelector('.filters');
  const projects = Array.from(document.querySelectorAll('.project[data-category]'));
  function filterWork(value) {
    let count=0;
    projects.forEach(p => {p.hidden=value!=='all' && p.dataset.category!==value;if(!p.hidden)count++;});
    filters?.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===value)));
    const countEl=document.querySelector('.results-count');
    if(countEl)countEl.textContent=count+' published '+(count===1?'study':'studies');
  }
  if(filters){filters.hidden=false;filters.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>filterWork(b.dataset.filter)));}
  function openHash() {
    const target=document.getElementById(location.hash.slice(1));
    if(target?.matches('details.study-detail')){
      const card=target.closest('.project'); if(card?.hidden)filterWork('all');
      target.open=true;
      requestAnimationFrame(()=>target.scrollIntoView({block:'start',behavior:'auto'}));
    }
  }
  document.querySelectorAll('details.study-detail').forEach(d=>d.addEventListener('toggle',()=>{
    const label=d.querySelector('summary>span');
    if(label)label.textContent=d.open?'Close study':'Inside the experiment';
  }));
  addEventListener('hashchange',openHash);
  if(location.hash)openHash();
  const progress=document.querySelector('.reading-progress');
  let scrollQueued=false;
  function updateProgress(){
    const total=document.documentElement.scrollHeight-innerHeight;
    if(progress)progress.style.transform='scaleX('+(total>0?Math.max(0,Math.min(1,scrollY/total)):0)+')';
    scrollQueued=false;
  }
  addEventListener('scroll',()=>{if(!scrollQueued){scrollQueued=true;requestAnimationFrame(updateProgress);}},{passive:true});
  addEventListener('resize',updateProgress);updateProgress();

  // The download is embedded once, so index.html works by itself after upload.
  let portfolioURL;
  document.querySelectorAll('[data-portfolio]').forEach(link=>{
    link.addEventListener('click',()=>{
      try{
        if(!portfolioURL){
          const data=JSON.parse(document.getElementById('portfolio-data').textContent);
          const raw=atob(data.base64),bytes=new Uint8Array(raw.length);
          for(let i=0;i<raw.length;i++)bytes[i]=raw.charCodeAt(i);
          portfolioURL=URL.createObjectURL(new Blob([bytes],{type:'application/pdf'}));
        }
        link.href=portfolioURL;
      }catch(_){ /* The ordinary local PDF link remains the fallback. */ }
    });
  });

  document.querySelectorAll('.copy-email').forEach(button=>{
    button.hidden=false;
    button.addEventListener('click',async()=>{
      const status=button.parentElement.querySelector('.copy-status');
      try{
        if(!navigator.clipboard)throw new Error('Clipboard not supported');
        await navigator.clipboard.writeText(button.dataset.email);
        status.textContent='Email address copied.';
      }catch(_){status.textContent='Select and copy the email address above.';}
    });
  });

  const viewer=document.querySelector('#figure-viewer');
  if(viewer && typeof viewer.showModal==='function'){
    let lastTrigger;
    const img=viewer.querySelector('img'),stage=viewer.querySelector('.viewer-stage'),full=viewer.querySelector('[data-fullsize]');
    document.querySelectorAll('[data-enlarge]').forEach(button=>{
      button.hidden=false;button.addEventListener('click',()=>{
        lastTrigger=button;
        const source=button.parentElement.querySelector('img');
        img.src=source.src;img.alt=source.alt;
        viewer.querySelector('.viewer-caption').textContent=button.closest('figure').querySelector('figcaption').textContent.trim();
        stage.classList.remove('full-size');full.textContent='View full size';
        viewer.showModal();document.body.classList.add('viewer-open');
        viewer.querySelector('[data-close]').focus();
      });
    });
    full.addEventListener('click',()=>{const isFull=stage.classList.toggle('full-size');full.textContent=isFull?'Fit to screen':'View full size';});
    viewer.querySelector('[data-close]').addEventListener('click',()=>viewer.close());
    viewer.addEventListener('click',e=>{
      const r=viewer.getBoundingClientRect();
      if(e.target===viewer && (e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom))viewer.close();
    });
    viewer.addEventListener('close',()=>{document.body.classList.remove('viewer-open');lastTrigger?.focus();});
  }

  /* A shared, bounded animation loop for the four decorative light studies. */
  const motionButtons=Array.from(document.querySelectorAll('.motion-toggle'));
  const note=document.querySelector('.motion-note');
  if(note && motionButtons[0]){
    const duplicate=motionButtons[0].cloneNode(true);note.append(duplicate);motionButtons.push(duplicate);
  }
  let paused=reduced.matches,raf=0,previous=0,time=0;
  const scenes=[];
  const TAU=Math.PI*2;
  let seed=92831;
  const random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
  const particles=Array.from({length:1400},()=>({x:random(),y:random(),phase:random()*TAU,size:.3+random()*1.2}));
  const canvases=document.querySelectorAll('canvas[data-scene]');
  function wavefront(s,t){
    const {ctx:c,w,h}=s,cx=w*.5,cy=h*.55,r=Math.min(w*.37,h*.43);
    const a=t*.13+.42+s.pointer*.12,co=Math.cos(a),si=Math.sin(a);
    function project(x,y,z){const xx=x*co+z*si,zz=-x*si+z*co,k=1+zz*.17;return [cx+xx*r*k,cy+y*r*.88*k];}
    c.lineWidth=.7;
    for(let j=-7;j<=7;j++){
      const lat=j/8*Math.PI/2,rad=Math.cos(lat),yy=Math.sin(lat);
      c.beginPath();
      for(let k=0;k<=100;k++){const q=k/100*TAU,p=project(Math.cos(q)*rad,yy,Math.sin(q)*rad);if(!k)c.moveTo(...p);else c.lineTo(...p);}
      c.strokeStyle='rgba(196,236,146,'+(.11+.19*(1-Math.abs(j)/8))+')';c.stroke();
    }
    for(let j=0;j<16;j++){
      const lon=j/16*TAU;c.beginPath();
      for(let k=0;k<=60;k++){const lat=-Math.PI/2+k/60*Math.PI,p=project(Math.cos(lat)*Math.cos(lon),Math.sin(lat),Math.cos(lat)*Math.sin(lon));if(!k)c.moveTo(...p);else c.lineTo(...p);}
      c.strokeStyle='rgba(196,236,146,.18)';c.stroke();
    }
    const dot=project(Math.cos(t*.23)*.9,Math.sin(t*.23)*.3,Math.sin(t*.23)*.9);
    c.fillStyle='#d3f5a8';c.beginPath();c.arc(dot[0],dot[1],2,0,TAU);c.fill();
  }
  function interference(s,t){
    const {ctx:c,w,h}=s,phase=(t*6+s.pointer*10)%9;
    c.lineWidth=.65;
    for(let source=-1;source<=1;source+=2){
      const cx=w*.5+source*w*.12,cy=h*.56;
      for(let i=0;i<43;i++){
        const r=i*9+phase,alpha=.10+.12*Math.exp(-r/(w*.6));
        c.strokeStyle='rgba(196,236,146,'+alpha+')';c.beginPath();c.arc(cx,cy,r,0,TAU);c.stroke();
      }
      c.fillStyle='#d2f4a2';c.beginPath();c.arc(cx,cy,2.2,0,TAU);c.fill();
    }
  }
  function speckle(s,t){
    const {ctx:c,w,h}=s;
    for(const p of particles){
      const x=(p.x-.5)*2,y=(p.y-.52)*2;
      const envelope=Math.exp(-(x*x*2.2+y*y*2.7));
      const brightness=Math.pow(.5+.5*Math.sin(p.phase+t*.44+s.pointer*.2+Math.sin(x*8+t*.18)),2)*envelope;
      if(brightness<.07)continue;
      c.fillStyle='rgba(196,236,146,'+(brightness*.83)+')';
      c.beginPath();c.arc(p.x*w,p.y*h,p.size*(.5+brightness*.8),0,TAU);c.fill();
    }
    c.strokeStyle='rgba(196,236,146,.10)';c.lineWidth=.6;
    c.beginPath();c.ellipse(w*.5,h*.52,w*.34,h*.36,0,0,TAU);c.stroke();
  }
  function orbit(s,t){
    const {ctx:c,w,h}=s,cx=w*.76,cy=h*.46,rx=Math.min(w*.27,360),ry=Math.min(h*.4,260);
    c.lineWidth=.65;
    for(let j=0;j<8;j++){
      const f=1+j*.065;c.strokeStyle='rgba(177,220,129,'+(.11-j*.009)+')';
      c.beginPath();c.ellipse(cx,cy,rx*f,ry*f,-.3+Math.sin(t*.06)*.035,0,TAU);c.stroke();
    }
    const a=t*.10-1.5,x=cx+rx*1.39*Math.cos(a),y=cy+ry*1.39*Math.sin(a);
    c.fillStyle='rgba(205,242,157,.75)';c.beginPath();c.arc(x,y,2,0,TAU);c.fill();
    c.strokeStyle='rgba(177,220,129,.1)';c.beginPath();c.moveTo(cx-rx*1.8,cy);c.lineTo(cx+rx*1.6,cy);c.stroke();
  }
  const painters={wavefront,interference,speckle,orbit};
  function draw(s,t){if(!s.ctx||!s.w||!s.h)return;s.ctx.clearRect(0,0,s.w,s.h);painters[s.type]?.(s,t);}
  function resize(s){
    const box=s.canvas.getBoundingClientRect(),ratio=Math.min(devicePixelRatio||1,1.5);
    s.w=box.width;s.h=box.height;
    if(!s.w||!s.h)return;
    s.canvas.width=Math.round(s.w*ratio);s.canvas.height=Math.round(s.h*ratio);
    s.ctx?.setTransform(ratio,0,0,ratio,0,0);draw(s,time);
  }
  canvases.forEach(canvas=>{
    const ctx=canvas.getContext('2d');if(!ctx)return;
    const s={canvas,ctx,type:canvas.dataset.scene,w:0,h:0,visible:false,pointer:0};scenes.push(s);
    if('ResizeObserver' in window)new ResizeObserver(()=>resize(s)).observe(canvas);
    else{resize(s);addEventListener('resize',()=>resize(s));}
    canvas.parentElement.addEventListener('pointermove',e=>{
      if(paused||e.pointerType==='touch')return;
      const r=canvas.getBoundingClientRect();s.pointer=((e.clientX-r.left)/r.width-.5)*2;
    },{passive:true});
  });
  function loop(now){
    raf=0;if(paused||document.hidden)return;
    if(now-previous>32){
      time+=Math.min((now-previous)/1000,.05);previous=now;
      scenes.forEach(s=>{if(s.visible)draw(s,time);});
    }
    if(scenes.some(s=>s.visible))raf=requestAnimationFrame(loop);
  }
  function start(){if(!paused&&!document.hidden&&!raf&&scenes.some(s=>s.visible)){previous=performance.now();raf=requestAnimationFrame(loop);}}
  function syncMotion(){
    document.documentElement.classList.toggle('motion-paused',paused);
    motionButtons.forEach(b=>{b.hidden=false;b.setAttribute('aria-pressed',String(paused));b.querySelector('.motion-label').textContent=paused?'Resume motion':'Pause motion';b.querySelector('.motion-icon').textContent=paused?'▷':'Ⅱ';});
    if(paused){cancelAnimationFrame(raf);raf=0;scenes.forEach(s=>draw(s,time));}else start();
  }
  motionButtons.forEach(b=>b.addEventListener('click',()=>{paused=!paused;syncMotion();}));
  reduced.addEventListener('change',e=>{paused=e.matches;syncMotion();});
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>{
      entries.forEach(entry=>{const s=scenes.find(s=>s.canvas===entry.target);if(s){s.visible=entry.isIntersecting;if(s.visible)draw(s,time);}});
      start();
    },{rootMargin:'80px'});
    scenes.forEach(s=>observer.observe(s.canvas));
  }else scenes.forEach(s=>s.visible=true);
  document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(raf);raf=0;}else start();});
  syncMotion();
  const portrait=document.querySelector('.portrait-composition');
  if(portrait && matchMedia('(pointer:fine)').matches){
    portrait.addEventListener('pointermove',e=>{
      if(paused)return;
      const r=portrait.getBoundingClientRect();
      portrait.style.setProperty('--px',((e.clientX-r.left)/r.width-.5)*5+'px');
      portrait.style.setProperty('--py',((e.clientY-r.top)/r.height-.5)*5+'px');
    },{passive:true});
    portrait.addEventListener('pointerleave',()=>{portrait.style.setProperty('--px','0px');portrait.style.setProperty('--py','0px');});
  }
  if('IntersectionObserver' in window && !reduced.matches){
    const reveal=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(!entry.isIntersecting)return;
      if(entry.target.animate)entry.target.animate([{opacity:.4,transform:'translateY(18px)'},{opacity:1,transform:'translateY(0)'}],{duration:650,easing:'cubic-bezier(.2,.65,.3,1)'});
      reveal.unobserve(entry.target);
    }),{threshold:.12});
    document.querySelectorAll('.section-heading,.recognition').forEach(el=>{if(el.getBoundingClientRect().top>innerHeight)reveal.observe(el);});
  }
})();
