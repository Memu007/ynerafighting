// Optional static art inspection; requires @napi-rs/canvas, not needed to play.
const fs=require('fs'),path=require('path'),vm=require('vm');
const {createCanvas,Image,GlobalFonts}=require('@napi-rs/canvas');
const mono='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf';
if(fs.existsSync(mono))GlobalFonts.registerFromPath(mono,'GameMono');
const root=path.join(__dirname,'..'),out=path.resolve(process.argv[2]||path.join(root,'preview'));
fs.mkdirSync(out,{recursive:true});
const canvas=createCanvas(640,400);canvas.addEventListener=()=>{};
const dummy=()=>({innerHTML:'',style:{},addEventListener(){},append(){},appendChild(){},getContext:()=>createCanvas(48,48).getContext('2d')});
const elements=new Map();const doc={hidden:false,addEventListener(){},getElementById:id=>id==='game'?canvas:elements.get(id)||(()=>{let e=dummy();elements.set(id,e);return e})(),querySelectorAll:()=>[],createElement:tag=>tag==='canvas'?createCanvas(48,48):dummy()};
let source=fs.readFileSync(path.join(root,'index.html'),'utf8').split('<script>')[1].split('</script>')[0];
if(GlobalFonts.has('GameMono'))source=source.replaceAll('monospace','GameMono');
source=source.replace('let audioEnabled = true;','let audioEnabled = false;').replaceAll('initAudio();','').replace(/\n  loop\(\);/,'\n globalThis.inspect = text => eval(text);');
const previous=process.cwd();process.chdir(root);
const sandbox={document:doc,localStorage:{getItem:()=>null,setItem(){},removeItem(){}},window:{addEventListener(){}},Image,Math,Date,setInterval(){},clearInterval(){},setTimeout(){},requestAnimationFrame(){}};
vm.createContext(sandbox);vm.runInContext(source,sandbox);
(async()=>{await new Promise(resolve=>setTimeout(resolve,300));
 const views={title:"gameState=STATE.TITLE",brief:"currentFightIndex=3;gameState=STATE.BRIEF",fight:"currentFightIndex=2;Object.assign(playerStats,{fuerza:5,aguante:5,tecnica:3,velocidad:3});setupFight(2);gameState=STATE.FIGHT;player.x=270;enemy.x=357;player.state='kick';enemy.state='block';fightBannerTimer=0;fightTimer=74",special:"gameState=STATE.FIGHT;player.state='special';specialFx=25;specialOrigin=player.x;specialDirection=1",gym:"currentFightIndex=3;gameState=STATE.GYM;playerStats.trainsLeft=2",arrival:"gameState=STATE.TRAIN_TRAVEL;travelMode='enter';sceneFrame=60;playerStats.car=true",night:"gameState=STATE.TRAIN_TRAVEL;travelMode='exit';sceneFrame=40",mafia:"currentFightIndex=3;beginCareerEvent('mafia')",result:"gameState=STATE.WEEK_RESULT;weekResult={index:2,won:true,optional:false,rival:'EL RULO',prize:225};sceneFrame=140",final:"gameState=STATE.VICTORY_FINAL"};
 for(const [name,setup] of Object.entries(views)){sandbox.inspect(setup+';draw()');fs.writeFileSync(path.join(out,name+'.png'),canvas.toBuffer('image/png'));}
 process.chdir(previous);console.log('Rendered '+Object.keys(views).length+' canvas states to '+out);
})();
