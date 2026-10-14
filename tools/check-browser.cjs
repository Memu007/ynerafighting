// Optional real-browser checks. Requires Playwright for development only.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
const {chromium}=require('playwright');
const root=path.join(__dirname,'..'),out=path.resolve(process.env.GAME_QA_OUTPUT||path.join(root,'browser-qa'));
fs.mkdirSync(out,{recursive:true});
const original=fs.readFileSync(path.join(root,'index.html'),'utf8');
// Expose fixture setup only in the HTTP test response, never the shipped HTML.
const instrumented=original.replace('  loop();',"  window.__test = expression => eval(expression);\n  loop();");
const server=http.createServer((req,res)=>{
 const rel=decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\//,'')||'index.html';
 const file=path.resolve(root,rel);
 if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
 if(rel==='index.html'){res.setHeader('Content-Type','text/html; charset=utf-8');res.end(instrumented);return;}
 try{res.setHeader('Content-Type',file.endsWith('.png')?'image/png':file.endsWith('.html')?'text/html; charset=utf-8':'text/plain');res.end(fs.readFileSync(file))}catch{res.writeHead(404);res.end()}
});
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 let options={headless:true};
 if(process.env.CHROMIUM_PROVIDER){const {default:provider}=await import(process.env.CHROMIUM_PROVIDER);options={...options,executablePath:await provider.executablePath(),args:provider.args.filter(arg=>arg!=='--single-process')};}
 else if(process.env.GAME_CHROMIUM_PATH)options.executablePath=process.env.GAME_CHROMIUM_PATH;
 const browser=await chromium.launch(options),base=`http://127.0.0.1:${server.address().port}`;
 const logs=[],errors=[];
 try{
  for(const viewport of [{width:1280,height:900,mobile:false},{width:360,height:800,mobile:true},{width:800,height:360,mobile:true}]){
   const context=await browser.newContext({viewport:{width:viewport.width,height:viewport.height},isMobile:viewport.mobile,hasTouch:viewport.mobile});
   const page=await context.newPage();page.setDefaultTimeout(10000);page.on('pageerror',e=>errors.push(e.message));
   await page.goto(base);await page.waitForFunction(()=>typeof window.__test==='function');
   const run=text=>page.evaluate(text=>window.__test(text),text);
   await page.locator('#guide-close').focus();await page.keyboard.press('Space');assert.equal(await page.locator('#guide').evaluate(e=>e.open),false);
   await page.locator('#game').click();await page.waitForFunction(()=>window.__test('gameState')==='INTRO_STORY');
   await run('currentFightIndex=1;gameState=STATE.BRIEF;saveProgress()');await page.locator('#scene-next').click();
   await page.waitForFunction(()=>window.__test('gameState')==='GYM');
   await page.locator('#gym-actions').waitFor({state:'visible'});
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1),false,'horizontal overflow '+viewport.width);
   await page.screenshot({path:path.join(out,`gym-${viewport.width}x${viewport.height}.png`),fullPage:true});
   await page.locator('#gym-actions button').first().focus();await page.keyboard.press('Enter');
   await page.waitForFunction(()=>window.__test('minigame.active'));
   assert.equal(await run('minigame.statTarget'),'fuerza');
   await run('minigame.cursor=50');await page.keyboard.press('KeyZ');assert.equal(await run('minigame.attempts'),1);
   // Fixture inventory makes checkbox and preview behavior available immediately.
   await run("minigame.active=false;gameState=STATE.GYM;playerStats.equipment.fuerza=true;playerStats.enhancedTraining=true;playerStats.trainsLeft=3;playerStats.money=500;playerStats.fatigue=40;panelSignature='';updatePanels()");
   const checkbox=page.locator('#training-mode input');await checkbox.focus();await page.keyboard.press('Space');
   await page.waitForFunction(()=>window.__test('playerStats.enhancedTraining')===false);assert.equal(await checkbox.isChecked(),false);
   await page.waitForFunction(()=>document.activeElement?.matches('#training-mode input'));
   await page.keyboard.press('Space');await page.waitForFunction(()=>window.__test('playerStats.enhancedTraining')===true);
   await page.locator('#buy-massage').click();assert.equal(await run('playerStats.money'),440);assert.equal(await run('playerStats.fatigue'),10);
   await run("playerStats.trainsLeft=0;panelSignature='';updatePanels()");
   assert.equal(await page.locator('#gym-actions button').count(),2);assert.equal(await page.locator('#market').isVisible(),false);
   await page.locator('#gym-actions button').nth(1).click();await page.waitForFunction(()=>!document.getElementById('market').hidden);
   await page.locator('#buy-food').click();assert.equal(await run('playerStats.money'),400);
   await page.locator('#gym-actions button').first().click();await page.waitForFunction(()=>window.__test('gameState')==='FIGHT');
   await page.waitForTimeout(80);
   if(viewport.mobile){const arena=await page.locator('#cabinet').boundingBox(),controls=await page.locator('#controls-bar').boundingBox();assert(arena.y>=-4&&controls.y+controls.height<=viewport.height+1,'arena and controls must fit viewport');}
   // Controls use real pointer/keyboard events against the running animation loop.
   if(viewport.mobile){
    const move=page.locator('[data-key=ArrowRight]'),box=await move.boundingBox();
    const session=await context.newCDPSession(page);
    await session.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:box.x+box.width/2,y:box.y+box.height/2,id:1}]});
    await page.waitForTimeout(180);assert.equal(await run('keys.ArrowRight'),true);
    await session.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await page.waitForTimeout(50);assert.equal(await run('keys.ArrowRight'),false);
    for(const el of await page.locator('.ctrl-btn').all()){const b=await el.boundingBox();assert(b.height>=44&&b.width>=44,'touch target too small');}
   }
   await page.screenshot({path:path.join(out,`fight-${viewport.width}x${viewport.height}.png`),fullPage:true});
   await run('gameState=STATE.GYM;playerStats.trainsLeft=1;saveProgress()');await page.reload();await page.locator('#game').click();
   await page.waitForFunction(()=>window.__test('gameState')==='GYM');assert.equal(await run('playerStats.trainsLeft'),1);
   logs.push({viewport:`${viewport.width}x${viewport.height}`,keyboard:true,shop:true,save:true,touch:viewport.mobile});
   await context.close();
  }
  if(process.env.GAME_PLAY_CAREER==='1'){
   const context=await browser.newContext({viewport:{width:1280,height:900}}),page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
   page.setDefaultTimeout(10000);const run=text=>page.evaluate(text=>window.__test(text),text);
   console.log('LIVE: introduction');await page.goto(base);await page.locator('#guide-close').click();await page.locator('#game').click();await page.keyboard.press('Space');await page.keyboard.press('Space');
   await page.waitForFunction(()=>window.__test('gameState')==='FIGHT');
   await page.waitForFunction(()=>window.__test('gameState')==='POST_ROBO',{},{timeout:30000});
   console.log('LIVE: after robbery');for(let i=0;i<5;i++)await page.locator('#scene-next').click();
   await page.locator('#gym-actions').waitFor({state:'visible'});
   const weeks=[['fuerza','aguante','tecnica'],['velocidad','fuerza','aguante'],['fuerza','aguante','tecnica']],results=[];
   const slot={fuerza:0,velocidad:1,aguante:2,tecnica:3};
   for(let week=0;week<3;week++){
    console.log('LIVE: training week '+(week+1));if(week===2){await page.locator('#market summary').click();await page.locator('#equipment-offers button').filter({hasText:'Banco y discos'}).click();}
    await page.locator('#buy-food').click();
    for(const stat of weeks[week]){
     console.log('LIVE: '+stat);await page.locator('#gym-actions button').nth(slot[stat]).click();await page.waitForFunction(()=>window.__test('minigame.active'));
     if(stat==='tecnica'){for(const key of ['KeyZ','KeyX','KeyZ','KeyZ','KeyX','KeyZ']){await page.keyboard.press(key);await page.waitForTimeout(190);}}
     else if(stat==='aguante'){for(let i=0;i<12;i++){await page.waitForFunction(()=>window.__test('minigame.frames%30>=8&&minigame.frames%30<=20&&minigame.frames-minigame.lastInput>=10'));await page.keyboard.press('KeyZ');await page.waitForTimeout(200);}}
     else{const n=stat==='velocidad'?5:3;for(let i=0;i<n;i++){await page.waitForFunction(()=>window.__test('minigame.cursor>=40&&minigame.cursor<=58&&minigame.frames-minigame.lastInput>=10&&(!minigame.jumped||minigame.statTarget!=="velocidad")'));await page.keyboard.press('KeyZ');}}
     await page.waitForFunction(()=>!window.__test('minigame.active'));
     for(let i=0;i<2&&await run('gameState')==='TRAIN_TRAVEL';i++)await page.locator('#scene-next').click();
     await page.locator('#gym-actions').waitFor({state:'visible'});
    }
    const before=await run('({rival:FIGHTS[currentFightIndex].name,stats:{...playerStats},life:playerMetrics().hp})');
    await page.locator('#gym-actions button').first().click();await page.waitForFunction(()=>window.__test('gameState')==='FIGHT');
    const begin=Date.now();let specials=0;
    while(await run('gameState')==='FIGHT'&&Date.now()-begin<110000){
     const snap=await run('({gap:Math.abs(player.x-enemy.x),dir:player.x<enemy.x,free:["idle","walk"].includes(player.state),windup:enemy.telegraph,energy:player.energy,dead:player.hp<=0||enemy.hp<=0})');
     if(snap.dead){await page.waitForTimeout(100);continue;}
     await page.keyboard.up('ArrowLeft');await page.keyboard.up('ArrowRight');
     if(snap.windup>0&&snap.gap<113)await page.keyboard.down('KeyC');
     else{await page.keyboard.up('KeyC');if(snap.gap>80)await page.keyboard.down(snap.dir?'ArrowRight':'ArrowLeft');if(snap.free&&snap.gap<=88){await page.keyboard.press(snap.energy>=100?'KeyV':'KeyX');if(snap.energy>=100)specials++;}}
     await page.waitForTimeout(70);
    }
    await page.keyboard.up('KeyC');await page.keyboard.up('ArrowRight');await page.keyboard.up('ArrowLeft');
    const result=await run('({state:gameState,result:weekResult,hp:player.hp,enemyHp:enemy.hp,money:playerStats.money})');
    results.push({...before,...result,seconds:+((Date.now()-begin)/1000).toFixed(1),specials});console.log('LIVE_RESULT '+JSON.stringify(results.at(-1)));
    assert.equal(result.state,'WEEK_RESULT');assert.equal(result.result.won,true,'trained tactical route must beat first three rivals');assert(specials>0);
    await page.locator('#scene-next').click();
    if(week===1)await page.locator('#career-choice button').nth(1).click();
    await page.locator('#scene-next').click();await page.locator('#gym-actions').waitFor({state:'visible'});
   }
   assert.equal(await run('playerStats.sponsor'),true);assert.equal(await run('playerStats.equipment.fuerza'),true);
   fs.writeFileSync(path.join(out,'career-results.json'),JSON.stringify(results,null,2));await context.close();
  }
  const portableContext=await browser.newContext(),portablePage=await portableContext.newPage();portablePage.on('pageerror',e=>errors.push(e.message));
  await portablePage.goto(base+'/conurbano-fighter.html');await portablePage.locator('#game').waitFor();
  assert.equal(await portablePage.evaluate(()=>typeof window.__test),'undefined');
  assert(await portablePage.locator('#game').evaluate(c=>c.toDataURL().length>10000));await portableContext.close();
  assert.deepEqual(errors,[]);fs.writeFileSync(path.join(out,'report.json'),JSON.stringify({logs,portable:true,errors},null,2));console.log(JSON.stringify({logs,portable:true,errors},null,2));
 }finally{await browser.close();server.close();}
})().catch(e=>{console.error(e);server.close();process.exitCode=1});
