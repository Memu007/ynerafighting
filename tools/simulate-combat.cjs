const fs=require('fs'),vm=require('vm'),path=require('path');
const source=fs.readFileSync(path.join(__dirname,'check-game.cjs'),'utf8').split('const g=boot(),r=g.run;')[0]+'\nmodule.exports={boot};';
const harness={require,module:{exports:{}},__dirname,console};vm.runInNewContext(source,harness);const {boot}=harness.module.exports;
const results=[];
for(const policy of ['attack-only','tactical']){
 const g=boot(),r=g.run;
 for(let index=1;index<=11;index++){
  // Three successful basic sessions each week, distributed strength/endurance/technique or speed.
  const force=1+index*2,endurance=1+index*2,technique=1+Math.ceil(index/2)*2,speed=1+Math.floor(index/2)*2;
  r(`currentFightIndex=${index};Object.assign(playerStats,{fuerza:${force},aguante:${endurance},tecnica:${technique},velocidad:${speed},fatigue:20});setupFight(${index});gameState=STATE.FIGHT;`);
  const result=r(`(()=>{let frames=0,specials=0;while(player.hp>0&&enemy.hp>0&&frames<6000){
   const gap=Math.abs(player.x-enemy.x);keys.KeyC=false;keys.ArrowLeft=false;keys.ArrowRight=false;
   if(gap>74)keys[player.x<enemy.x?'ArrowRight':'ArrowLeft']=true;
   const free=['idle','walk'].includes(player.state);
   if('${policy}'==='tactical' && enemy.telegraph>0 && enemy.telegraph<=5 && gap<113){keys.KeyC=true;}
   else if(free && gap<=88){if(player.energy>=100){handleActionPress('KeyV');specials++;}else handleActionPress('${policy}'==='tactical'&&enemy.state==='block'?'KeyX':(frames%3===0?'KeyZ':'KeyX'));}
   update();frames++;
  }return {index:currentFightIndex,style:FIGHTS[currentFightIndex].style,seconds:+(frames/60).toFixed(1),hp:player.hp,maxHp:player.maxHp,enemyHp:enemy.hp,specials};})()`);
  results.push({policy,...result});
 }
}
console.log(JSON.stringify(results,null,2));
